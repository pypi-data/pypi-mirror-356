# main.py
# Содержимое файла: main.py
import logging

import os
import uvicorn 

import sys
from fastapi import FastAPI, Request, status, HTTPException # Добавлен HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware # Для CORS
from sensory_detector.yolo_server.app.appconfig import config # Предполагается, что это основной конфиг
#from src.sensory_detector.yolo_server.app.model_cache import model_cache
from sensory_detector.yolo_server.app.model_cache import ModelCache
# Импортируем роутеры для различных секций API
from sensory_detector.yolo_server.endpoints.endpoints import router as general_api_router
from sensory_detector.yolo_server.endpoints.objects import router as objects_router
from sensory_detector.yolo_server.endpoints.texts import router as texts_router
from sensory_detector.yolo_server.endpoints.embeddings import router as embeddings_router
from sensory_detector.yolo_server.endpoints.ws_endpoints import ws_router as websocket_router

from typing import Dict # Для healthz response_model
from contextlib import asynccontextmanager

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, # Устанавливаем общий уровень логирования на DEBUG
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout) # Выводим логи в стандартный вывод
    ]
)
logger.info("Starting FastAPI application setup...")

if not logger.handlers:
    logging.getLogger("ultralytics").setLevel(config.LOG_LEVEL)
    logging.getLogger("av").setLevel(config.LOG_LEVEL)
    logger.info(f"{config.LOG_LEVEL}")
    
# Настройка Rate Limiting (пример, требует установки slowapi)
# limiter = Limiter(key_func=get_remote_address)
# app = FastAPI(title="YOLO Detection Service", description="Async microservice for image and video analysis with YOLO.", docs_url="/docs", redoc_url="/redoc", lifespan=lifespan) # Или использовать lifespan context manager
# app = FastAPI(title="YOLO Detection Service", description="Async microservice for image and video analysis with YOLO.", docs_url="/docs", redoc_url="/redoc") # Если не используем lifespan
# app.state.limiter = limiter # Добавить состояние для slowapi

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Контекстный менеджер для событий старта и остановки приложения."""
    logger.info("Application startup event triggered.")

    # Создаем экземпляр ModelCache и сохраняем его в состоянии приложения
    app.state.model_cache = ModelCache(
        ttl_sec=config.MODEL_CACHE_TIMEOUT_SEC,
        max_models=config.MODEL_CACHE_MAX_MODELS
    )
    # Запускаем фоновую задачу кэша
    await app.state.model_cache.start()
    logger.info("Model cache reaper started.")

    # Опционально прелоадим дефолтную модель
    if config.DEFAULT_MODEL_NAME:
        try:
            logger.info(f"Preloading default model: {config.DEFAULT_MODEL_NAME}...")
            # Импорт здесь, чтобы избежать циклических зависимостей при старте
            from sensory_detector.yolo_server.detectors.detector_interface import ModelTaskType
            from sensory_detector.yolo_server.app.model_utils import get_wrapper
            # Используем get_wrapper, передавая app.state.model_cache явно
            # await get_wrapper(
            #     app.state.model_cache, # Передаем state, так как request недоступен здесь напрямую
            #     task_type=ModelTaskType.DETECTION,
            #     model_name=config.DEFAULT_MODEL_NAME
            # )
            logger.info(f"Default model '{config.DEFAULT_MODEL_NAME}' preloaded successfully.")
        except Exception as e:
            logger.error(f"Failed to preload default model '{config.DEFAULT_MODEL_NAME}': {e}", exc_info=True)

    logger.info("Startup sequence finished.")
    #app.state.heavy_pool = concurrent.futures.ThreadPoolExecutor(
    #    max_workers=max(4, multiprocessing.cpu_count()*2),
    #    thread_name_prefix="heavytask",
    #)
    yield
    #app.state.heavy_pool.shutdown(wait=True)
    logger.info("Application shutdown event triggered.")

    # Останавливаем кэш
    if hasattr(app.state, 'model_cache') and app.state.model_cache is not None:
        await app.state.model_cache.shutdown()
        logger.info("Model cache shutdown complete.")
    logger.info("Shutdown sequence finished.")


# Инициализация FastAPI приложения с метаданными и lifespan
app = FastAPI(
    title="Sensory Detector API",
    description="Scalable Microservice for Computer Vision/Machine Learning tasks: Object Detection, OCR, and Embeddings.",
    version="0.2.0", # Можно брать из pyproject.toml или другого места
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json", # Явно указываем путь
    lifespan=lifespan # Подключаем lifespan
)

# --- Мидлвары (Middlewares) ---

# CORS Middleware (P1 #8)
# Настроить allow_origins под ваш фронтенд или список разрешенных доменов
# allow_credentials=True, allow_methods=["*"], allow_headers=["*"] - очень либеральные настройки,
# для продакшена стоит ограничить allow_methods и allow_headers

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Заменить на список разрешенных origin'ов в проде
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Exception handler for HTTPException to return consistent JSON errors
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTPException: {exc.status_code} - {exc.detail}", exc_info=exc)
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

# Rate Limiting Middleware (P1 #8) - Пример
# try:
#     # Попытка импорта slowapi и подключения мидлвари
#     from slowapi import Limiter, _rate_limit_exts
#     from slowapi.util import get_remote_address
#     limiter = Limiter(key_func=get_remote_address)
#     app.state.limiter = limiter # Добавляем лимитер в state приложения
#     app.add_middleware(_rate_limit_exts.RateLimitMiddleware, limiter=limiter)
#     logger.info("RateLimiting middleware added.")
# except ImportError:
#     logger.warning("slowapi not installed. Rate Limiting middleware skipped.")
# except Exception as e:
#      logger.error(f"Error adding RateLimiting middleware: {e}", exc_info=True)


# --- Подключение роутеров ---
app.include_router(general_api_router) # For /api/available_models, /api/loaded_models, /api/unload_model
app.include_router(objects_router) # For /api/objects
app.include_router(texts_router) # For /api/texts
app.include_router(embeddings_router) # For /api/embeddings
app.include_router(websocket_router) # For /ws/analyze_stream


# --- Health Check Endpoint (P3 #13 - liveness/readiness) ---
# Добавляем базовый эндпоинт для проверки состояния

@app.get("/healthz", summary="Health check endpoint", response_model=Dict[str, str])
async def healthz(request: Request): # Request now explicitly includes `Request` to access `app.state`
    """
    Basic endpoint to check if the service is alive and model cache is accessible.
    Attempts to access the default model to verify cache and model loading.
    """
    try:
        # Access model_cache from app.state
        # `model_cache` - это наш экземпляр ModelCache
        model_cache_instance: ModelCache = request.app.state.model_cache
        detector = await model_cache_instance.get(
            name=config.DEFAULT_MODEL_NAME, # Pass name
            loader=lambda name: None # dummy loader, as we only need to check if it's already in cache or can be loaded
        )
        status_info = {"status": "ok", "model_cache": "accessible"}
        if detector:
            status_info["default_model"] = detector.model_name
        else:
            status_info["default_model"] = "not_loaded_or_configured"
        return JSONResponse(status_code=status.HTTP_200_OK, content=status_info)
    except Exception as e:
        logger.error(f"Health check failed while accessing model cache: {e}", exc_info=True)
        status_info = {"status": "error", "model_cache": "failed", "detail": str(e)}
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=status_info)
    
    # Для локального запуска: uvicorn main:app --reload

def run_server():
    """
    Точка входа для запуска FastAPI-сервера через `sensory-detector-server` скрипт.
    Использует Uvicorn напрямую.
    """
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    
    logger.info(f"Starting Uvicorn server on {host}:{port} with log level {config.LOG_LEVEL}.")
    uvicorn.run(
        app,
        host=host,
        port=port,
        reload=True if config.LOG_LEVEL == "DEBUG" else None, # Используем флаг DEBUG_MODE из конфига
        log_level=config.LOG_LEVEL.lower() # Uvicorn ожидает lowercase
    )

if __name__ == "__main__":
    # Если main.py запущен напрямую (e.g., `python main.py`)
    run_server()