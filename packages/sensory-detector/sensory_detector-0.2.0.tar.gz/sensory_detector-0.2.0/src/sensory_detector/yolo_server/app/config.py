
# project_root/yolo_server/config.py
import os
from pathlib import Path
# from dotenv import load_dotenv # Pydantic BaseSettings can handle this
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, PositiveInt, DirectoryPath, model_validator
from typing import Optional
import logging

log = logging.getLogger(__name__)

class Config(BaseSettings):
    
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    LOG_LEVEL: str = Field("DEBUG", description="Change debug mode.")

    HOST: str = Field("0.0.0.0", description="Host address for the FastAPI server.")
    PORT: int = Field(8000, description="Port for the FastAPI server.")

    PROJECT_ROOT: Path = Field(
        default_factory=lambda: Path(__file__).resolve().parent.parent,
        description="Корень проекта",
    )
    WEIGHTS_DIR: Path = Field(
        default="weights",
        description="Каталог с .pt-весами моделей",
    )
    

    MODEL_CACHE_TIMEOUT_SEC: PositiveInt = Field(
            default=30,
            description="Через сколько секунд простоя выгружать модель из памяти GPU",
    )
    MODEL_CACHE_MAX_MODELS: PositiveInt = Field(10, description="Максимальное количество моделей в кэше.")

    FILES_PATH: Optional[DirectoryPath] = Field(
        default=None,
        description="Каталог, из которого разрешается анализ по видео",
    )
    DEFAULT_MODEL_NAME: str = Field("yolov8s", description="Default model to use if none is specified in the request.")

    DEFAULT_MODEL_PATH: Path | None = None 
    
    EASYOCR_CACHE_DIR: Optional[Path] = Field(None, description="Directory for EasyOCR models cache. If None, EasyOCR uses its default (~/.EasyOCR/model).")
    TESSDATA_PREFIX: Optional[Path] = Field(None, description="Directory containing Tesseract language data (tessdata). If None, Tesseract searches system paths.")
    CLIP_CACHE_DIR: Optional[Path] = Field(None, description="Directory for OpenCLIP models cache. If None, OpenCLIP uses its default (~/.cache/clip).")

    
    

    # каталоги с весами (для YOLO/CLIP и т. д.)
    @model_validator(mode='after')
    def _post_init_config(self) -> 'Config':
        """
        Post-initialization hook to resolve paths and set environment variables.
        This runs after initial Pydantic validation and assignment from env vars.
        """
        #load_dotenv() # Load .env file again to ensure it's loaded for all fields
        
        # Resolve WEIGHTS_DIR relative to PROJECT_ROOT
        self.WEIGHTS_DIR = (self.PROJECT_ROOT / self.WEIGHTS_DIR).resolve()
        self.WEIGHTS_DIR.mkdir(parents=True, exist_ok=True)
        log.info(f"Weights directory set to: {self.WEIGHTS_DIR}")

        # Resolve FILES_PATH if set
        if self.FILES_PATH:
            self.FILES_PATH = self.FILES_PATH.resolve()
            self.FILES_PATH.mkdir(parents=True, exist_ok=True) # Ensure it exists for path-based access
            log.info(f"Path-based file access root set to: {self.FILES_PATH}")
        else:
            log.warning("FILES_PATH is not set. Path-based file access will be disabled for security.")

        # Resolve and set environment variables for other model caches
        if self.EASYOCR_CACHE_DIR:
            self.EASYOCR_CACHE_DIR = self.EASYOCR_CACHE_DIR.resolve()
            self.EASYOCR_CACHE_DIR.mkdir(parents=True, exist_ok=True)
            # EasyOCR uses this env variable for custom model paths
            os.environ['EASYOCR_PATH'] = str(self.EASYOCR_CACHE_DIR)
            log.info(f"EasyOCR models cache directory set to: {self.EASYOCR_CACHE_DIR}")
        else:
            log.info("EASYOCR_CACHE_DIR not set. EasyOCR will use its default model cache location (~/.EasyOCR/model).")

        if self.TESSDATA_PREFIX:
            self.TESSDATA_PREFIX = self.TESSDATA_PREFIX.resolve()
            # Tesseract usually expects a 'tessdata' subdirectory within this prefix
            # We'll set the env var, and wrappers will pass this to TesseractConfig
            os.environ['TESSDATA_PREFIX'] = str(self.TESSDATA_PREFIX)
            log.info(f"Tessdata prefix for Tesseract set to: {self.TESSDATA_PREFIX}")
        else:
            log.info("TESSDATA_PREFIX not set. Tesseract will search for tessdata in system paths.")

        if self.CLIP_CACHE_DIR:
            self.CLIP_CACHE_DIR = self.CLIP_CACHE_DIR.resolve()
            self.CLIP_CACHE_DIR.mkdir(parents=True, exist_ok=True)
            # OpenCLIP uses its own mechanism for cache_dir, pass it directly
            # No direct env var for OpenCLIP, usually passed as argument.
            log.info(f"OpenCLIP models cache directory set to: {self.CLIP_CACHE_DIR}")
        else:
            log.info("CLIP_CACHE_DIR not set. OpenCLIP will use its default model cache location (~/.cache/clip).")

        return self

config = Config()
