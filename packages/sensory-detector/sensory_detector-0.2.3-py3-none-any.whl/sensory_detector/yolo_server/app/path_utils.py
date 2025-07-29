# src/sensory_detector/path_utils.py
from __future__ import annotations
import os
from pathlib import Path
from importlib import resources

# Determine the package root. This works correctly for pip installs and local development.
# For local dev: /path/to/Yolo/src/sensory_detector
# For pip install: /path/to/site-packages/sensory_detector
try:
    # This tries to find the installed package directory
    # For local development, if run as a script directly from src/sensory_detector/,
    # it might require `python -m src.sensory_detector.yolo_server.main` or similar.
    # If it fails, we fall back to assuming typical project structure.
    PKG_ROOT = Path(resources.files("sensory_detector"))
except ImportError:
    # Fallback for local development when `sensory_detector` is not installed as a package
    # and we are running from the project root.
    # Adjust as needed if your run command or entry point is different.
    _current_file_path = Path(__file__).resolve()
    # Assuming path_utils.py is at src/sensory_detector/path_utils.py
    # So, go up 2 levels (sensory_detector, src) to reach project root (Yolo)
    # Then append src/sensory_detector to find the logical package root.
    PKG_ROOT = _current_file_path.parent


def _inside_pkg_weights(sub_path: str) -> Path | None:
    """
    Вернёт путь к весу, если он запакован внутрь wheel.
    Args:
        sub_path: Относительный путь внутри директории `weights/` (например, "yolo/", "tessdata/").
    """
    # Предполагаем, что веса будут в <PKG_ROOT>/weights/
    p = PKG_ROOT / "weights" / sub_path
    return p if p.exists() else None

def get_weights_root() -> Path:
    """
    Определяет корневую директорию для всех ML весов.
    Порядок приоритета:
    1. Переменная окружения WEIGHTS_DIR.
    2. Веса, упакованные внутри Python-пакета (если установлены).
    3. Директория кэша пользователя (~/.cache/sensory-detector/weights).
    """
    # 1. Проверяем переменную окружения WEIGHTS_DIR
    env_var = os.getenv("WEIGHTS_DIR")
    if env_var:
        resolved_path = Path(env_var).expanduser().resolve()
        resolved_path.mkdir(parents=True, exist_ok=True) # Убеждаемся, что директория существует
        return resolved_path

    # 2. Проверяем, упакованы ли веса внутри пакета (например, для "толстых" wheel-файлов)
    pkg_weights_root = _inside_pkg_weights("")
    if pkg_weights_root:
        return pkg_weights_root

    # 3. Возвращаемся к домашнему каталогу кэша пользователя
    home_cache = Path.home() / ".cache" / "sensory-detector" / "weights"
    home_cache.mkdir(parents=True, exist_ok=True)
    return home_cache

# Специализированные резолверы для различных типов весов/библиотек
# Они все используют `get_weights_root()` как базу
def get_yolo_weights_path(model_name: str = "yolov8s") -> Path:
    """Возвращает полный путь к файлу весов модели YOLO."""
    return get_weights_root() / "yolo" / f"{model_name}.pt"

def get_clip_cache_dir() -> Path:
    """Возвращает директорию для кэша моделей CLIP."""
    # CLIP_CACHE_DIR env var может переопределить дефолт внутри WEIGHTS_DIR
    env_var = os.getenv("CLIP_CACHE_DIR")
    if env_var:
        resolved_path = Path(env_var).expanduser().resolve()
        resolved_path.mkdir(parents=True, exist_ok=True)
        return resolved_path
    return get_weights_root() / "clip"

def get_yolo_cache_dir() -> Path:
    """Возвращает директорию для кэша моделей CLIP."""
    # CLIP_CACHE_DIR env var может переопределить дефолт внутри WEIGHTS_DIR
    env_var = os.getenv("YOLO_CACHE_DIR")
    if env_var:
        resolved_path = Path(env_var).expanduser().resolve()
        resolved_path.mkdir(parents=True, exist_ok=True)
        return resolved_path
    return get_weights_root() / "yolo"

def get_easyocr_cache_dir() -> Path:
    """Возвращает директорию для моделей EasyOCR."""
    # EASYOCR_CACHE_DIR env var может переопределить дефолт внутри WEIGHTS_DIR
    env_var = os.getenv("EASYOCR_CACHE_DIR")
    if env_var:
        resolved_path = Path(env_var).expanduser().resolve()
        resolved_path.mkdir(parents=True, exist_ok=True)
        return resolved_path
    return get_weights_root() / "easy"

def get_tessdata_prefix() -> Path:
    """Возвращает директорию для языковых данных Tesseract (tessdata)."""
    # TESSDATA_PREFIX env var может переопределить дефолт внутри WEIGHTS_DIR
    env_var = os.getenv("TESSDATA_PREFIX")
    if env_var:
        resolved_path = Path(env_var).expanduser().resolve()
        resolved_path.mkdir(parents=True, exist_ok=True)
        return resolved_path
    return get_weights_root() / "tessdata"

def get_tesseract_lib_path() -> Path:
    """Возвращает директорию, содержащую нативную библиотеку Tesseract C API (libtesseract.so.X)."""
    # TESSERACT_LIB_PATH env var может переопределить дефолт внутри WEIGHTS_DIR
    env_var = os.getenv("TESSERACT_LIB_PATH")
    if env_var:
        resolved_path = Path(env_var).expanduser().resolve()
        resolved_path.mkdir(parents=True, exist_ok=True)
        return resolved_path
    # По умолчанию ищем в подпапке 'tesseract' внутри WEIGHTS_DIR
    return get_weights_root() / "tesseract"