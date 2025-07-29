
import os,sys
from pydantic import BaseModel, Field, model_validator, ConfigDict # Импортируем model_validator
from typing import Optional, Tuple, Literal # Импортируем Literal
from dotenv import load_dotenv
from enum import Enum #

load_dotenv(override=True)

print("--- Loading .env file ---")
dotenv_path = load_dotenv(override=True)
if dotenv_path:
    print(f".env file loaded from: {dotenv_path}")
    # Добавляем вывод содержимого os.environ после загрузки .env
    print("\n--- Environment variables after loading .env ---")
    for key, value in os.environ.items():
        # Выводим только переменные, которые могли бы относиться к Tesseract или путям
        if "TESSERACT" in key.upper() or "PATH" in key.upper() or "LIB" in key.upper():
             print(f"{key}={value}")
    print("--- End of relevant environment variables ---")
else:
    print(".env file not found.")
print("-------------------------\n")


# Дефолтный whitelist - можно вынести в constants.py
DEFAULT_WHITELIST = (
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    "0123456789"
)

class OCRImageProcessingConfig(BaseModel):
    """Конфигурация для предобработки изображений перед OCR."""
    enabled: bool = Field(False, description="Включена ли предобработка OCR изображений.")

    # Параметры ресайза
    resize_enabled: bool = Field(False, description="Включен ли ресайз изображения.")
    resize_mode: Literal["target_dim", "scale_factor"] = Field(
        "target_dim",
        description="Режим ресайза: 'target_dim' (по самой длинной стороне) или 'scale_factor' (умножение размеров на фактор)."
    )
    beckbin: bool = Field(False, description="Включена ли бинаризация изображения для изъятия двойного фона.")
    # Используется, если resize_mode='target_dim'
    resize_target_dim: Optional[int] = Field(
        None,
        gt=0,
        description="Целевая размерность (большая сторона) для ресайза, если resize_mode='target_dim'. Если None или <=0, ресайз не выполняется в этом режиме."
    )

    # Используется, если resize_mode='scale_factor'
    resize_scale_factor: Optional[float] = Field(
        None,
        gt=0,
        description="Скалирующий фактор для ресайза, если resize_mode='scale_factor'. Если None или <=0, ресайз не выполняется в этом режиме."
    )

    resize_filter: str = Field(
        "LANCZOS", # Хороший фильтр для увеличения
        description="Фильтр ресайза (PIL filter name, e.g., LANCZOS, BICUBIC, BILINEAR)."
    )

    # Grayscale
    grayscale_enabled: bool = Field(False, description="Convert image to grayscale.")

    # Denoising
    denoising_enabled: bool = Field(False, description="Apply denoising filter.")
    denoising_strength: Optional[int] = Field(
        10, ge=0, le=20, description="Strength of denoising filter (0-20)."
    )

    # Thresholding
    thresholding_enabled: bool = Field(False, description="Apply adaptive thresholding.")
    thresholding_block_size: Optional[int] = Field(
        11, gt=1, description="Block size for adaptive thresholding (must be odd)."
    )
    thresholding_constant: Optional[int] = Field(
        2, description="Constant subtracted from the mean for thresholding."
    )

    # Sharpening
    sharpening_enabled: bool = Field(False, description="Apply image sharpening.")
    sharpening_alpha: Optional[float] = Field(
        1.0, ge=0.0, description="Sharpening strength."
    )
    
    # Параметры бордеров
    borders_enabled: bool = Field(False, description="Включено ли добавление бордеров.")
    border_size: int = Field(
        10,
        ge=0,
        description="Размер бордера в пикселях, добавляемого по всем сторонам."
    )
    border_color: Tuple[int, int, int] = Field(
        (255, 255, 255), # Белый цвет
        description="Цвет бордера в формате RGB."
    )

    # Параметры обработки фона и инверсии
    background_processing_enabled: bool = Field(
        False,
        description="Включена ли автоматическая обработка фона (инверсия и B&W)."
    )
    # Порог для определения светлого/темного фона (средняя яркость пикселей фона)
    background_lightness_threshold: int = Field(
        128, # 0-255
        ge=0,
        le=255,
        description="Порог средней яркости (0-255) для определения светлого (>порога) или темного (<=порога) фона."
    )
    # Порог для конвертации в ЧБ после потенциальной инверсии
    bw_threshold: int = Field(
        128, # 0-255
        ge=0,
        le=255,
        description="Порог яркости (0-255) для преобразования в чистое черно-белое изображение (<= порога - черный, > порога - белый)."
    )
    # Размер области (в пикселях) в углах для анализа фона
    background_sample_size: int = Field(
        10,
        ge=1,
        description="Размер квадратной области в каждом из 4х углов изображения для анализа яркости фона."
    )

    # Параметры авто-ориентации (использует Tesseract)
    auto_orient_enabled: bool = Field(
        False,
        description="Включена ли автоматическая детекция и поворот ориентации (требует поддержки в TesseractWrapper)."
    )
    auto_orient_confidence_threshold: float = Field(
        0.5, # 0.0 - 1.0
        ge=0.0,
        le=1.0,
        description="Минимальная уверенность Tesseract в ориентации для применения поворота."
    )

    # Rotate / Deskew (conceptual, not implemented in ImageProcessor yet)
    rotate_deskew_enabled: bool = Field(False, description="Enable automatic rotation/deskewing.")

    # Other post-processing options
    remove_lines_enabled: bool = Field(False, description="Attempt to remove lines (e.g., tables).")

    # Валидатор для проверки, что соответствующий параметр установлен для выбранного режима
    @model_validator(mode='after')
    def check_resize_mode_params(self) -> 'OCRImageProcessingConfig':
        if self.resize_enabled:
            if self.resize_mode == "target_dim":
                if self.resize_target_dim is None or self.resize_target_dim <= 0:
                    raise ValueError(
                        "resize_target_dim must be set and > 0 when resize_mode is 'target_dim'"
                    )
                # Убедимся, что scale_factor не используется в этом режиме, хотя это не строго обязательно
                # self.resize_scale_factor = None # Или просто игнорируем

            elif self.resize_mode == "scale_factor":
                if self.resize_scale_factor is None or self.resize_scale_factor <= 0:
                     raise ValueError(
                        "resize_scale_factor must be set and > 0 when resize_mode is 'scale_factor'"
                     )
                # Убедимся, что target_dim не используется в этом режиме
                # self.resize_target_dim = None # Или просто игнорируем
        return self


class TesseractPageSegMode(str, Enum):
    """Tesseract Page Segmentation Modes (PSM)."""
    OSD_ONLY = "0"
    AUTO_OSD = "1"
    AUTO = "3" # default
    SINGLE_COLUMN = "4"
    SINGLE_BLOCK_VERT_TEXT = "5"
    SINGLE_BLOCK = "6"
    SINGLE_LINE = "7"
    SINGLE_WORD = "8"
    SINGLE_CHAR = "9"
    SPARSE_TEXT = "10"
    SPARSE_TEXT_OSD = "11"
    RAW_LINE = "12"
    COUNT = "13"


class TesseractConfig(BaseModel):
    """
    Конфигурация для Tesseract OCR, загружаемая из переменных окружения
    или файла.
    """
    model_config = ConfigDict(
        env_prefix='TESSERACT_',
        env_file='.env', # Assumes .env is loaded by main config
        env_file_encoding='utf-8',
        extra='ignore'
    )
    # Общие параметры
    lang: str = Field('rus+eng', description="Языки для распознавания (например, 'eng', 'rus+eng').")
    default_psm: int = Field(3, description="Режим сегментации страницы по умолчанию (3: Fully automatic page segmentation).")
    default_oem: int = Field(3, description="Режим движка OCR по умолчанию (3: Default).")
    default_whitelist: Optional[str] = Field(
        DEFAULT_WHITELIST,
        description="Список разрешенных символов по умолчанию."
    )
    image_processing: OCRImageProcessingConfig = Field(
         default_factory=OCRImageProcessingConfig,
         description="Конфигурация предобработки изображений перед OCR."
    )
    
    datapath: str = Field(
        #None,
        (os.getcwd() + '/src/sensory_detector/weights/tessdata').replace('\\', '/'), # Default relative path
        description="Путь к директории tessdata."
    )
    lib_path: Optional[str] = Field(
        (os.getcwd() + '/src/sensory_detector/weights/tesseract').replace('\\', '/'), # Default relative path
        #None,
        description="Путь к библиотеке Tesseract C API для Windows."
    )
def load_tesseract_config() -> TesseractConfig:
    """
    Загружает конфигурацию Tesseract из переменных окружения.
    Предполагается, что load_dotenv() уже был вызван.
    """
    try:
        config = TesseractConfig()
        return config
    except Exception as e:
        print(f"Error loading Tesseract configuration: {e}")
        # В продакшене лучше использовать логгер
        # logging.error(f"Error loading Tesseract configuration: {e}", exc_info=True)
        raise # Пробрасываем исключение, т.к. без конфига работать нельзя

# Пример использования (для отладки)
if __name__ == "__main__":
    print("--- Loading Tesseract Config Example ---")
    try:
        tess_cfg = load_tesseract_config()
        print("Tesseract Config Loaded Successfully:")
        print(tess_cfg.model_dump_json(indent=2))

        # Проверка платформенно-зависимого пути
        print(f"\nCurrent Platform: {sys.platform}")
        if sys.platform == "linux":
            print(f"Configured Linux Lib Path: {tess_cfg.lib_path}")
        elif sys.platform == "win32":
            print(f"Configured Windows Lib Path: {tess_cfg.lib_path}")
        # elif sys.platform == "darwin":
        #     print(f"Configured MacOS Lib Path: {tess_cfg.macos_lib_path}")

    except Exception as e:
        print(f"Failed to load config: {e}")