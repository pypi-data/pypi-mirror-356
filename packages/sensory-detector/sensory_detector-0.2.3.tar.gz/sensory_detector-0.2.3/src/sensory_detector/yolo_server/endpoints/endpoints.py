# yolo_server/endpoints.py
# Содержимое файла: src/sensory_detector/yolo_server/endpoints/endpoints.py
import os
from fastapi import APIRouter, HTTPException, Path as FastAPIPath, Request 
from fastapi.responses import JSONResponse
from typing import Optional, List, Annotated, Dict
import logging
from pathlib import Path
from flask import jsonify
# Импортируем унифицированные Pydantic-модели
from sensory_detector.models.models import FilesResponse, ModelsResponse, CacheStatsResponse, UnloadModelResponse, TaskType
# Импортируем основной конфиг приложения
from sensory_detector.yolo_server.app.appconfig import config
# Импортируем менеджер кэша моделей
from sensory_detector.yolo_server.app.model_cache import model_cache

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["general", "model management"])

def get_available_models_from_config() -> Dict[TaskType, List[str]]:
    """
    Scans configured directories and provides predefined lists of models
    available for each task type.
    """
    available: Dict[TaskType, List[str]] = {
        TaskType.DETECTION: [],
        TaskType.OCR: [],
        TaskType.EMBEDDING: []
    }

    # 1. YOLO Models (from WEIGHTS_DIR)
    yolo_models = []
    weights_dir = config.WEIGHTS_DIR
    if weights_dir.exists():
        try:
            # Используем list comprehension для эффективности
            yolo_models = [
                f.stem for f in weights_dir.iterdir()
                if f.is_file() and f.suffix == ".pt"
            ]
            logger.debug(f"Found {len(yolo_models)} YOLO model files in {weights_dir}")
        except Exception as e:
            logger.error(f"Error scanning weights directory {weights_dir}: {e}", exc_info=True)
    else:
        logger.warning(f"YOLO Weights directory not found: {weights_dir}. No YOLO models will be listed.")

    available[TaskType.DETECTION] = sorted(yolo_models)
    # 2. OCR Models (Predefined list, as EasyOCR/Tesseract are usually installed/downloaded by the library itself)
    available[TaskType.OCR] = sorted(["easyocr", "tess"]) 
    # 3. Embedding Models (Predefined list for OpenCLIP)
    available[TaskType.EMBEDDING] = sorted(["clip-base"]) # Example OpenCLIP models

    return available

@router.get("/available_models", response_model=ModelsResponse, summary="Получить список доступных моделей")
async def available_models_endpoint():
    """
    Возвращает список имен моделей, файлы которых (.pt) найдены
    в сконфигурированном каталоге весов (WEIGHTS_DIR), а также предопределенные
    модели для OCR и эмбеддингов.
    """
    logger.info("Request received for available_models")
    return ModelsResponse(
        available_models=get_available_models_from_config(),
        default_model=config.DEFAULT_MODEL_NAME,
        message="Выберите модель по имени. Если имя не указано в запросе, будет использована модель по умолчанию."
    )

@router.get("/loaded_models", response_model=List[CacheStatsResponse], summary="Получить статус загруженных моделей")
async def loaded_models_endpoint():
    """
    Возвращает текущий статус кэша моделей: какие модели загружены,
    сколько секунд простаивают, сколько раз использовались,
    и примерную занимаемую память (VRAM/RAM).
    """
    logger.info("Request received for loaded_models (cache status)")
    return await model_cache.stats()

@router.delete("/unload_model/{model_name}", response_model=UnloadModelResponse, summary="Выгрузить модель из кэша")
async def unload_model_endpoint(
    model_name: Annotated[
        str, FastAPIPath(..., description="Имя модели, которую нужно выгрузить из кэша")
    ]
):
    """
    Принудительно выгружает указанную модель из кэша.
    Полезно для освобождения памяти или при обновлении файла весов.
    """
    logger.info(f"Request received to unload model: {model_name}")

    # Здесь мы напрямую работаем с внутренним словарем кэша, т.к. публичного метода .pop нет
    # В идеале, ModelCache должен предоставить публичный async метод `unload_model(name)`
    unloaded = await model_cache.unload_model(model_name)
    if not unloaded:
        logger.warning(f"Unload requested for model '{model_name}', but it was not found in cache.")
        raise HTTPException(status_code=404, detail=f"Model '{model_name}' not found in cache.")
    
    logger.info(f"Successfully unloaded model: {model_name}")
    return UnloadModelResponse(detail=f"Model '{model_name}' was unloaded from cache.") # Возвращаем Pydantic модель

@router.route("/cache/stats", methods=["GET"])
async def cache_stats():
    return jsonify(await model_cache.stats())


@router.get(
    "/files",
    response_model=FilesResponse,
    summary="List available files on the server's FILES_PATH",
    description="Returns a list of files accessible via path-based requests, relative to the configured FILES_PATH."
)
async def get_available_files_endpoint():
    """
    Retrieves a list of files available for processing via the 'path' parameter.
    Files are listed relative to the server's configured FILES_PATH.
    """
    logger.info("Request received for available_files")

    if not config.FILES_PATH:
        detail = "Server's FILES_PATH is not configured. Path-based file access is disabled."
        logger.warning(detail)
        raise HTTPException(status_code=403, detail=detail)

    if not config.FILES_PATH.exists():
        detail = f"Configured FILES_PATH '{config.FILES_PATH}' does not exist on the server."
        logger.warning(detail)
        raise HTTPException(status_code=404, detail=detail)

    if not config.FILES_PATH.is_dir():
        detail = f"Configured FILES_PATH '{config.FILES_PATH}' is not a directory."
        logger.warning(detail)
        raise HTTPException(status_code=400, detail=detail)


    available_files: List[str] = []
    try:
        # Рекурсивный поиск файлов в FILES_PATH и его поддиректориях
        # Если нужно только на верхнем уровне, используйте config.FILES_PATH.iterdir()
        # Если нужна рекурсия: for item in config.FILES_PATH.rglob('*'):
        for item in config.FILES_PATH.iterdir():
            if item.is_file():
                # Получаем относительный путь для клиента
                relative_path = str(item.relative_to(config.FILES_PATH))
                available_files.append(relative_path)
        logger.info(f"Found {len(available_files)} files in {config.FILES_PATH}.")
    except Exception as e:
        logger.error(f"Error scanning FILES_PATH {config.FILES_PATH}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to scan files directory: {e}")

    return FilesResponse(
        files=sorted(available_files), # Отсортируем для предсказуемости
        base_path=str(config.FILES_PATH),
        message=f"Successfully retrieved list of files from {config.FILES_PATH}"
    )