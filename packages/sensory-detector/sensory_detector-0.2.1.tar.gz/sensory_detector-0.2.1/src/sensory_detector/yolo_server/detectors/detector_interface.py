"""
Базовый интерфейс-протокол для любых object-detector’ов, которые
подключаются к сервису (YOLOv8, Detectron2, …).

Все методы БЛОКИРУЮЩИЕ.  Из асинхронного кода их вызываем через
`await asyncio.to_thread(detector.detect_...)`.
"""
from __future__ import annotations

from typing import Protocol, List, Union, Any, Optional
from enum import Enum
import numpy as np

from sensory_detector.models.models import (
    ObjectDetectionResult, # Новое имя для DetectionFrame
    OCRFrameResult,        # Новое имя для OCRResult
    EmbeddingFrameResult,  # Новое имя для EmbeddingResponse
    DetectedObject,        # Используется внутри ObjectDetectionResult
)
class ModelTaskType(str, Enum):
    DETECTION = "detection"
    EMBEDDING = "embedding"
    OCR = "text"


class Detector(Protocol):
    """
    Протокол, определяющий интерфейс для всех оберток моделей (YOLO, CLIP, EasyOCR, Tesseract).
    """
    @property
    def model_name(self) -> str:
        """Возвращает внутреннее имя загруженной модели (например, 'yolov8s', 'easyocr-ru_en')."""
        ...

    def task_type(self) -> ModelTaskType:
        """Возвращает тип задачи, которую выполняет этот детектор (например, DETECTION, OCR, EMBEDDING)."""
        ...

    # --- Методы для обработки одиночного изображения/кадра ---
    def detect_from_bytes(self, image_bytes: bytes, timestamp: float = 0.0, frame_index: int = -1, **kwargs: Any) -> Union[ObjectDetectionResult, OCRFrameResult, EmbeddingFrameResult]:
        """Обрабатывает изображение из байтов. Возвращает специфический для задачи результат кадра."""
        ...

    def detect_from_frame(self, frame: np.ndarray, timestamp: float = 0.0, frame_index: int = -1, **kwargs: Any) -> Union[ObjectDetectionResult, OCRFrameResult, EmbeddingFrameResult]:
        """Обрабатывает один кадр изображения OpenCV (numpy). Возвращает специфический для задачи результат кадра."""
        ...

    def detect_from_file(self, file_path: str, timestamp: float = 0.0, frame_index: int = -1, **kwargs: Any) -> Union[ObjectDetectionResult, OCRFrameResult, EmbeddingFrameResult]:
        """Обрабатывает изображение или видео из пути к файлу. Возвращает специфический для задачи результат кадра (для одиночного изображения)."""
        ...

    # --- Метод для пакетной обработки ---
    def detect_batch(self, frames: List[np.ndarray], timestamps: Optional[List[float]] = None, frame_indices: Optional[List[int]] = None, **kwargs: Any) -> List[Union[ObjectDetectionResult, OCRFrameResult, EmbeddingFrameResult]]:
        """Обрабатывает пакет кадров изображения OpenCV (numpy). Возвращает список специфических для задачи результатов кадра."""
        ...

    def unload(self) -> None:
        """Освобождает ресурсы модели (например, высвобождает память GPU)."""
        ...

    def mem_bytes(self) -> int:
        """Возвращает предполагаемое использование памяти моделью в байтах."""
        ...