
# project_root/yolo_server/config.py
import os
from pathlib import Path
# from dotenv import load_dotenv # Pydantic BaseSettings can handle this
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, PositiveInt, DirectoryPath, model_validator
from typing import Optional
import logging
from importlib import resources
from sensory_detector.yolo_server.app.path_utils import (
    get_weights_root,
    get_tesseract_lib_path,
    get_tessdata_prefix,
    get_easyocr_cache_dir,
    get_clip_cache_dir,
    get_yolo_cache_dir
)

log = logging.getLogger(__name__)
PKG_ROOT = Path(resources.files("sensory_detector"))

def _inside_pkg(sub: str) -> Path:
    """Вернёт путь к весу, если он запакован внутрь wheel."""
    p = PKG_ROOT / "weights" / sub
    return p if p.exists() else None

def get_weights_root() -> Path:
    # 1) ENV               2) .env через Config()    3) упаковка
    env = os.getenv("WEIGHTS_DIR")
    if env:
        return Path(env).expanduser().resolve()

    # fallback – пакетные веса (если wheel собран с --include-package-data)
    pkg = _inside_pkg("")
    if pkg:
        return pkg

    # 4) последний вариант – ~/.cache/sensory-detector/weights
    home = Path.home() / ".cache" / "sensory-detector" / "weights"
    home.mkdir(parents=True, exist_ok=True)
    return home

# Специализированные резолверы
def yolo_weights(model_name: str) -> Path:
    return get_weights_root() / "yolo" / f"{model_name}.pt"

class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    LOG_LEVEL: str = Field("DEBUG", description="Change debug mode.")
    HOST: str = Field("0.0.0.0", description="Host address for the FastAPI server.")
    PORT: int = Field(8000, description="Port for the FastAPI server.")

    # Используем `default_factory` для PROJECT_ROOT, чтобы она динамически определялась
    # Если config.py находится в src/sensory_detector/yolo_server/app/config.py
    # то для корня проекта (Yolo/) нужно подняться на 4 уровня вверх.
    PROJECT_ROOT: Path = Field(
        default_factory=lambda: Path(__file__).resolve().parent.parent.parent.parent,
        description="Корень проекта (обычно директория `Yolo/`). Используется для внутренних путей, не для внешних ресурсов."
    )

    # Основная переменная для директории весов. Если не задана, path_utils решит.
    WEIGHTS_DIR: Optional[Path] = Field(
        default=None,
        description="Корневой каталог для всех весов моделей (YOLO, CLIP, EasyOCR, Tesseract data/lib). "
                    "Если не задан, используется внутренний путь пакета или ~/.cache/sensory-detector/weights."
    )

    MODEL_CACHE_TIMEOUT_SEC: PositiveInt = Field(300, description="Время жизни модели в кэше без использования (сек).")
    MODEL_CACHE_MAX_MODELS: PositiveInt = Field(10, description="Максимальное количество моделей в кэше.")

    FILES_PATH: Optional[DirectoryPath] = Field(
        default=None,
        description="Абсолютный путь к каталогу, из которого разрешается анализ файлов по пути. "
                    "Если не задан, path-based доступ будет отключен."
    )
    DEFAULT_MODEL_NAME: str = Field("yolov8s", description="Имя модели по умолчанию для предварительной загрузки.")

    # Явные переменные для Tesseract/EasyOCR/CLIP, которые могут быть переопределены извне.
    # Эти поля будут заполнены Pydantic из env vars в первую очередь.
    # Если они не заданы, _post_init_config установит их через path_utils.
    TESSERACT_LIB_PATH: Optional[Path] = Field(
        default=None, description="Путь к нативной библиотеке Tesseract C API (e.g., libtesseract.so.4)."
    )
    TESSDATA_PREFIX: Optional[Path] = Field(
        default=None, description="Путь к директории с языковыми данными Tesseract (tessdata)."
    )
    EASYOCR_CACHE_DIR: Optional[Path] = Field(
        default=None, description="Директория для кэша моделей EasyOCR."
    )
    CLIP_CACHE_DIR: Optional[Path] = Field(
        default=None, description="Директория для кэша моделей OpenCLIP."
    )
    YOLO_CACHE_DIR: Optional[Path] = Field(
        default=None, description="Директория для кэша моделей YOLO."
    )


    # Переменные окружения, которые используются некоторыми библиотеками,
    # но не являются "путями к кэшу", а скорее "путями для конфигов"
    # YOLO_CONFIG_DIR: str = Field("/tmp", description="Каталог для сохранения конфигов YOLO. В Docker обычно /tmp.")

    @model_validator(mode='after')
    def _post_init_config(self) -> 'Config':
        """
        Пост-инициализация: разрешает пути и устанавливает переменные окружения,
        чтобы другие библиотеки и Pydantic-модели могли их найти.
        """
        # 1. Разрешаем и устанавливаем WEIGHTS_DIR как переменную окружения
        # Это гарантирует, что path_utils.get_weights_root() будет использовать
        # сконфигурированный путь или его надежный дефолт.
        resolved_weights_dir = self.WEIGHTS_DIR if self.WEIGHTS_DIR else get_weights_root()
        os.environ.setdefault("WEIGHTS_DIR", str(resolved_weights_dir))
        self.WEIGHTS_DIR = resolved_weights_dir # Обновляем поле экземпляра конфига
        log.info(f"Resolved base WEIGHTS_DIR: {self.WEIGHTS_DIR}")

        # 2. Устанавливаем специфичные пути кэша/библиотек как переменные окружения,
        # используя path_utils. Это CRUCIAL для Pydantic Settings в TesseractConfig
        # и для других библиотек, которые читают эти ENV.
        # `setdefault` важен: он устанавливает переменную только если её ещё нет.
        os.environ.setdefault("TESSERACT_LIB_PATH",
                              str(self.TESSERACT_LIB_PATH if self.TESSERACT_LIB_PATH else get_tesseract_lib_path()))
        os.environ.setdefault("TESSDATA_PREFIX",
                              str(self.TESSDATA_PREFIX if self.TESSDATA_PREFIX else get_tessdata_prefix()))
        os.environ.setdefault("EASYOCR_MODULE_PATH",
                              str(self.EASYOCR_CACHE_DIR if self.EASYOCR_CACHE_DIR else get_easyocr_cache_dir()))
        os.environ.setdefault("EASYOCR_CACHE_DIR",
                              str(self.EASYOCR_CACHE_DIR if self.EASYOCR_CACHE_DIR else get_easyocr_cache_dir()))
        os.environ.setdefault("CLIP_CACHE_DIR",
                              str(self.CLIP_CACHE_DIR if self.CLIP_CACHE_DIR else get_clip_cache_dir()))
        os.environ.setdefault("YOLO_CACHE_DIR",
                              str(self.YOLO_CACHE_DIR if self.YOLO_CACHE_DIR else get_yolo_cache_dir()))

        # 3. Разрешаем FILES_PATH
        if self.FILES_PATH:
            self.FILES_PATH = self.FILES_PATH.resolve()
            self.FILES_PATH.mkdir(parents=True, exist_ok=True) # Убеждаемся, что директория существует
            log.info(f"Path-based file access root set to: {self.FILES_PATH}")
        else:
            log.warning("FILES_PATH is not set. Path-based file access will be disabled for security.")
            self.FILES_PATH = None # Явно устанавливаем None для последующих проверок

        log.debug("Все переменные окружения для путей установлены/инициализированы.")

        return self

config = Config()