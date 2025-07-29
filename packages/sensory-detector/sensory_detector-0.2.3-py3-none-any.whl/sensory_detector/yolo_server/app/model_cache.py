
import asyncio, logging, psutil, gc
from dataclasses import dataclass
from pydantic import  Field
from datetime import datetime, timedelta
from typing import Dict, Callable, TypeVar, Generic, List, Any
from contextlib import suppress
import os
from sensory_detector.yolo_server.app.appconfig import config
from sensory_detector.yolo_server.detectors.detector_interface import Detector
from sensory_detector.yolo_server.app.model_utils import MODEL_WRAPPERS
from sensory_detector.models.models import CacheStatsResponse 
try:
    import torch
    _torch_available = True
except ImportError:
    _torch_available = False
    
log = logging.getLogger(__name__)
T = TypeVar("T", bound=Detector)


# ──────────────────────────────────────────────────────────────────────────
# DATA CLASSES
# ──────────────────────────────────────────────────────────────────────────
@dataclass
class _CacheItem(Generic[T]):
    """Internal representation of a cached model."""
    wrapper: T
    last_used: datetime
    hits: int
    loaded_at: datetime = Field(default_factory=datetime.now) # Added loaded_at timestamp

    def __repr__(self):
        return (
            f"_CacheItem(wrapper={self.wrapper.model_name} ({self.wrapper.__class__.__name__}), "
            f"last_used={self.last_used.strftime('%Y-%m-%d %H:%M:%S')}, hits={self.hits})"
        )

# ──────────────────────────────────────────────────────────────────────────
# MAIN CACHE
# ──────────────────────────────────────────────────────────────────────────
class ModelCache(Generic[T]):
    """LRU-кэш для детекторов"""

    def __init__(self, ttl_sec: int = 40, max_models: int = 10):
        self.ttl = timedelta(seconds=ttl_sec)
        self.max_models = max_models
        self._cache: Dict[str, _CacheItem[T]] = {}
        self._lock = asyncio.Lock()
        self._reaper_task: asyncio.Task | None = None
        log.info(f"ModelCache initialized with TTL={ttl_sec}s, max_models={max_models}.")

    # public ────────────────────────────────────────────────────────────
    async def start(self):
        if not self._reaper_task:
            self._reaper_task = asyncio.create_task(self._reaper())

    async def shutdown(self):
        if self._reaper_task:
            self._reaper_task.cancel()
            with suppress(asyncio.CancelledError):
                await self._reaper_task
        async with self._lock:
            for item in self._cache.values():
                item.wrapper.unload()
            self._cache.clear()
            gc.collect()
            if _torch_available and torch.cuda.is_available():
                try:
                    torch.cuda.empty_cache()
                    log.debug("torch.cuda.empty_cache() called during shutdown.")
                except Exception as e:
                    log.warning(f"Error calling torch.cuda.empty_cache() during shutdown: {e}")


    async def get(
        self,
        name: str | None = None,
        loader: Callable[[str], T] | None = None,
    ) -> T:
        """
        Возвращает детектор из кэша или загружает его.
        Обновляет метки использования.

        Args:
            name: Имя модели, которое нужно получить. Если None, используется config.DEFAULT_MODEL_NAME.
            loader: Функция-фабрика, которая принимает имя модели (str) и возвращает экземпляр Detector (T).
                    Эта функция будет вызвана, если модель не найдена в кэше и ее нужно загрузить.
        """
        model_key = name if name is not None else config.DEFAULT_MODEL_NAME

        if not model_key:
            log.info(f"Model name must be provided '{model_key}'. ...")
            # Если ни имя не предоставлено, ни значение по умолчанию в конфиге, то это ошибка.
            raise ValueError("Model name must be provided or DEFAULT_MODEL_NAME must be set in config.")

        if loader is None:
            loader = loader if not loader else MODEL_WRAPPERS.get(model_key, None)
            # loader должен быть всегда предоставлен из model_utils.get_wrapper
            #raise ValueError(f"Loader function must be provided for model '{model_key}'.")

        async with self._lock:
            # ─ hit ────────────────────────────────────────────────────────
            if model_key in self._cache:
                item = self._cache[model_key]
                item.last_used = datetime.now()
                item.hits += 1
                log.debug(f"Cache HIT for model '{model_key}'. Hits: {item.hits}")
                return item.wrapper

            # ─ miss ───────────────────────────────────────────────────────
            log.info(f"Cache MISS for model '{name}'. Loading...")
            if len(self._cache) >= self.max_models:
                log.warning(f"Cache is full ({len(self._cache)} models). Evicting oldest...")
                await self._evict_one_locked()

            try:
                # Загрузка модели может быть долгой и/или CPU-bound, выполняем в отдельном потоке
                wrapper = await asyncio.to_thread(loader, model_key)
                self._cache[model_key] = _CacheItem(
                    wrapper=wrapper, last_used=datetime.now(), hits=1, loaded_at=datetime.now()
                )
                log.info(f"Model '{model_key}' loaded and added to cache. Current cache size: {len(self._cache)}")
                return wrapper
            except FileNotFoundError as e:
                 log.error(f"Model file not found for '{model_key}': {e}")
                 raise FileNotFoundError(f"Model '{model_key}' not found. Ensure '{model_key}.pt' is in {config.WEIGHTS_DIR}") from e
            except Exception as e:
                log.error(f"Failed to load model '{model_key}': {e}", exc_info=True)
                raise RuntimeError(f"Failed to load model '{model_key}'. See logs for details.") from e



    async def stats(self) -> List[CacheStatsResponse]:
        async with self._lock:
            now = datetime.now()
            data = []
            for name, item in self._cache.items():
                data.append(
                    CacheStatsResponse(
                        model_name=name,
                        task_type=item.wrapper.task_type(),
                        wrapper_class=item.wrapper.__class__.__name__,
                        loaded_at=item.loaded_at.isoformat(),
                        last_used=item.last_used.isoformat(),
                        idle_seconds=round((now - item.last_used).total_seconds(), 1),
                        use_count=item.hits,
                        estimated_mem_bytes=self._mem_estimate(item.wrapper),
                    )
                )
            return data

    # internal ─────────────────────────────────────────────────────────
    async def _reaper(self):
        """Фоновая задача для выгрузки старых моделей."""
        while True:
            await asyncio.sleep(self.ttl.total_seconds())
            log.debug("Cache reaper running...")
            cutoff = datetime.now() - self.ttl
            async with self._lock:
                names_to_evict = [
                    name for name, item in self._cache.items()
                    if item.last_used < cutoff
                ]
                if names_to_evict:
                    log.info(f"Reaper evicting {len(names_to_evict)} models due to timeout.")
                for name in names_to_evict:
                    item = self._cache.pop(name)
                    try:
                        item.wrapper.unload()
                        log.info("Model '%s' evicted after idle timeout (%s secs).", name, self.ttl.total_seconds())
                    except Exception as e:
                        log.error(f"Error unloading model '{name}' during reaper: {e}", exc_info=True)



    async def _evict_one_locked(self):
        """Выгружает одну модель (наименее недавно использовавшуюся). Требует, чтобы lock был уже взят."""
        if not self._cache:
            log.warning("Eviction requested, but cache is empty.")
            return # Ничего делать, если кэш пуст

        # LRU: ищем самый старый last_used
        oldest_name = min(self._cache, key=lambda k: self._cache[k].last_used)
        item = self._cache.pop(oldest_name)
        try:
            item.wrapper.unload()
            log.info("Model '%s' evicted because cache is full (%s/%s models).",
                     oldest_name, len(self._cache)+1, self.max_models)
        except Exception as e:
             log.error(f"Error unloading model '{oldest_name}' during eviction: {e}", exc_info=True)


    # static helpers ──────────────────────────────────────────────────
    @staticmethod
    def _mem_estimate(wrapper: Detector) -> int:
        """
        Универсальная оценка VRAM/RAM, занимаемой оберткой детектора.
        1. wrapper.mem_bytes()          – если детектор сам умеет считать (приоритет)
        2. torch.cuda.memory_allocated  – когда под капотом PyTorch/CUDA
        3. psutil RSS                   – как последний резерв (RSS всего процесса)
        Возвращает байты.
        """
        # 1. user-defined hook (если обертка предоставляет свой метод)
        if hasattr(wrapper, "mem_bytes") and callable(wrapper.mem_bytes):
            try:
                mem = wrapper.mem_bytes()
                if isinstance(mem, (int, float)):
                     return int(mem)
                log.warning(f"wrapper.mem_bytes() returned non-numeric value: {mem}")
            except Exception as e:
                log.warning(f"Error calling wrapper.mem_bytes(): {e}", exc_info=True)

        # 2. PyTorch / CUDA (если обертка содержит torch модель на CUDA)
        if _torch_available:
            try:
                # Attempt to find a PyTorch model within the wrapper
                # Common patterns: wrapper.model, wrapper._model, wrapper.detector
                model_attr_names = ['model', '_model', 'detector', '_detector', 'reader', '_reader', 'core', '_core']
                for attr_name in model_attr_names:
                    mdl = getattr(wrapper, attr_name, None)
                    if mdl is not None and hasattr(mdl, 'parameters'):
                        # If DataParallel is used, get the underlying module
                        if isinstance(mdl, torch.nn.DataParallel):
                            mdl = mdl.module
                        if hasattr(mdl, 'device') and mdl.device.type == "cuda":
                            # Calculate memory of this specific PyTorch model on CUDA
                            total_params_mem = sum(p.numel() * p.element_size() for p in mdl.parameters() if p.is_cuda)
                            total_buffers_mem = sum(b.numel() * b.element_size() for b in mdl.buffers() if b.is_cuda)
                            # Add some overhead for model code itself, optimizer states, etc.
                            # This is still a rough estimate.
                            estimated_mem = total_params_mem + total_buffers_mem
                            return int(estimated_mem)
            except Exception as e:
                log.warning(f"Error estimating torch CUDA memory for {wrapper.model_name}: {e}", exc_info=True)

        # 3. RSS процесса (fallback)
        try:
            return psutil.Process(os.getpid()).memory_info().rss
        except Exception as e:
             log.warning(f"Error estimating process RSS: {e}", exc_info=True)
             return 0 # Не удалось оценить память

    async def _async_update_activity(self, name: str):
        """Обновляет метку last_used для модели в кэше."""
        # Этот метод предназначен для вызова из async контекста или через run_coroutine_threadsafe
        async with self._lock:
            if name in self._cache:
                self._cache[name].last_used = datetime.now()
                # log.debug(f"Activity updated for model '{name}'.") # Может быть слишком много логов
            else:
                # Это может случиться, если модель была выгружена другим способом
                log.debug(f"Activity update requested for model '{name}', but it's not in cache.")
    # NEW ✦  Публичный метод для ручной выгрузки
    # ────────────────────────────────────────────────────────────────
    async def unload_model(self, name: str) -> bool:
        """
        Удаляет и выгружает модель из кэша по имени.

        Returns:
            True, если модель была найдена и выгружена, иначе False.
        """
        async with self._lock:
            item = self._cache.pop(name, None)
            if item:
                try:
                    item.wrapper.unload()
                    log.info("Model '%s' explicitly unloaded.", name)
                    return True
                except Exception as e:
                    log.error(f"Error unloading model '{name}' manually: {e}", exc_info=True)
                    # Хотя модель удалена из кэша, сообщаем об ошибке выгрузки
                    # Можно вернуть False или рейзить, в зависимости от политики ошибок
                    return False # Возвращаем False при ошибке выгрузки, хотя модель убрана из кэша
            return False # Модель не найдена в кэше

# глобальный синглтон кэша
model_cache: ModelCache[Detector] = ModelCache(
    ttl_sec=int(config.MODEL_CACHE_TIMEOUT_SEC)
    if hasattr(config, "MODEL_CACHE_TIMEOUT_SEC")
    else 30,
    max_models=int(10)
    if hasattr(config, "MODEL_CACHE_MAX")
    else 10,
)