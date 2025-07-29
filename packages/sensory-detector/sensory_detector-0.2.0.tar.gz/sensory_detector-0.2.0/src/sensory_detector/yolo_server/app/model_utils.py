"""
Вспомогательные функции для выбора модели/враппера и работы с кэшем.
"""
from __future__ import annotations
import asyncio, logging
from typing import Any, Callable, Dict
from functools import lru_cache

from sensory_detector.yolo_server.detectors.yolo_wrapper import YOLOv8Wrapper
from sensory_detector.yolo_server.detectors.easyocr_wrapper import EasyOCRWrapper
from sensory_detector.yolo_server.detectors.tesseract_ocr_wrapper import TesseractOCRWrapper
from sensory_detector.yolo_server.detectors.clip_wrapper import CLIPWrapper
from sensory_detector.yolo_server.detectors.detector_interface import Detector, ModelTaskType
from fastapi import HTTPException, Request

log = logging.getLogger(__name__)

MODEL_WRAPPERS = {
    "yolov8s": YOLOv8Wrapper,
    "clip-base": CLIPWrapper,
    "easyocr": EasyOCRWrapper,
    "tess": TesseractOCRWrapper,
    # ...
}

# Карта "task -> загрузчик по умолчанию"
_MODEL_WRAPPERS: Dict[ModelTaskType, Callable[..., Detector]] = {
    ModelTaskType.DETECTION: YOLOv8Wrapper,
    # Для OCR используется _ocr_loader, так как выбор между EasyOCR и Tesseract сложнее.
    # Поэтому ModelTaskType.OCR не мапится напрямую на класс здесь.
    ModelTaskType.EMBEDDING: CLIPWrapper,
}


def _ocr_loader(name: str, **kwargs) -> Detector:
    """
    Выбор OCR-обёртки по имени модели.
    Простая эвристика:
        - 'tess' / 'tesseract*' → Tesseract
        - иначе EasyOCR
    """
    low = name.lower() if name else ""
    if low.startswith("tess"):
        return TesseractOCRWrapper(model_name=name, **kwargs)  # type: ignore[arg-type]
    return EasyOCRWrapper(model_name=name, **kwargs)           # type: ignore[arg-type]


async def get_wrapper(
    model_cache_instance, # ModelCache instance is passed here
    task_type: ModelTaskType,
    model_name: str | None = None,
    **init_kwargs,
) -> Detector:
    """
    Возвращает загруженный (или вновь созданный) враппер.
    """        
    log.info(f"*******************Successfully got wrapper for model {model_name} '{model_cache_instance}' (task: {task_type}) from cache.")

    # Определяем правильный загрузчик (функцию-фабрику) на основе типа задачи.
    # Эта loader_func будет передана в model_cache_instance.get() и вызвана, если модель нужно загрузить.
    loader_func: Callable[[str], Detector]

    if task_type == ModelTaskType.DETECTION:
        # Используем MODEL_WRAPPERS
        loader_func = lambda n: _MODEL_WRAPPERS[ModelTaskType.DETECTION](model_name=n)
    elif task_type == ModelTaskType.EMBEDDING:
        # CLIPWrapper может требовать специфические аргументы (openclip_model_name/pretrained),
        # которые должны быть переданы через init_kwargs. Lambda-функция корректно их перенаправляет.
        # Используем MODEL_WRAPPERS
        loader_func = lambda n: _MODEL_WRAPPERS[ModelTaskType.EMBEDDING](model_name=n, **init_kwargs)
    elif task_type == ModelTaskType.OCR:
        # OCR использует свою специфическую функцию-загрузчик
        loader_func = lambda n: _ocr_loader(n, **init_kwargs)
    else:
        # Этот случай должен быть перехвачен валидацией OpenAPI/Pydantic на уровне API.
        raise HTTPException(422, detail=f"Unsupported task type: {task_type.value}")

    try:
        wrapper = await model_cache_instance.get(name=model_name, loader=loader_func)

        log.debug(f"Successfully got wrapper for model '{model_name or 'default'}' (task: {task_type.value}) from cache.")
        return wrapper

    except FileNotFoundError as e:
        log.error(f"Model file not found error from cache. Model: {model_name} (task: {task_type.value}). Error: {e}", exc_info=True)
        raise HTTPException(404, detail=f"Model '{model_name or 'default'}' weights not found. Details: {e}") from e

    except RuntimeError as e:
        log.error(f"Model loading RuntimeError from cache. Model: {model_name} (task: {task_type.value}). Error: {e}", exc_info=True)
        original_error = e.__cause__ or e.__context__
        error_detail = str(original_error) if original_error else str(e)

        api_message = f"Error loading model '{model_name or 'default'}' for task '{task_type.value}'. Details: {error_detail}"
        if "AttributeError: bn" in error_detail: # Specific hint for a known Ultralytics/PyTorch issue
             api_message += " (Likely version incompatibility issue between ultralytics and torch. Check logs for details.)"

        raise HTTPException(500, detail=api_message) from e

    except HTTPException: # Re-raise FastAPI HTTPExceptions directly
        raise

    except Exception as e: # Catch any other unexpected errors
        log.error(f"An unexpected error occurred while getting model wrapper from cache: {e}", exc_info=True)
        raise HTTPException(500, detail=f"An unexpected internal error occurred while getting model '{model_name or 'default'}'.") from e