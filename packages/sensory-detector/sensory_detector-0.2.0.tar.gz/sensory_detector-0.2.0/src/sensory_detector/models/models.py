from __future__ import annotations
from pydantic import BaseModel, Field
from typing import List, Optional, Tuple, Dict, Union, Literal
from enum import Enum

Bbox = Tuple[int, int, int, int]           # (x1, y1, x2, y2)

class BaseFrameResult(BaseModel):
    """
    Base model for results pertaining to a single image frame or item within a series.
    Includes common metadata like frame index and timestamp.
    """
    frame_index: Optional[int] = Field(None, description="Index of the frame if part of a video stream or batch.")
    timestamp: Optional[float] = Field(None, description="Timestamp of the frame in seconds if part of a video stream.")
    processing_time_ms: Optional[float] = Field(0.0, description="Time taken for embedding processing in milliseconds.")
    # For now, it's specific to OCRFrameResult and EmbeddingFrameResult, so kept there.


class BoundingBox(BaseModel):
    """
    Represents a bounding box with top-left (x1, y1) and bottom-right (x2, y2) coordinates.
    Coordinates are typically floats representing pixel positions.
    """
    x1: float = Field(..., description="Левая граница")
    y1: float = Field(..., description="Верхняя граница")
    x2: float = Field(..., description="Правая граница")
    y2: float = Field(..., description="Нижняя граница")

class DetectedObject(BaseModel):
    """
    Represents a single detected object with its name, confidence, and bounding box.
    """
    index: int = Field(..., description="Уникальный индекс объекта в кадре")
    object_name: str = Field(..., description="Название объекта, распознанного YOLO ")
    confidence: float = Field(..., ge=0.0, le=1.0, description="скор модели в диапазоне от 0 до 1")
    bounding_box: BoundingBox = Field(..., description="Координаты ограничивающего прямоугольника")

class ObjectDetectionResult(BaseFrameResult):
    """
    Represents the detection results for a single frame, typically from a video.
    """
    detections: List[DetectedObject]


    # ───────────────────────────────  OCR (Easy / Tess)  ───────────────────────
class OCRWordResult(BaseModel):
    """
    Represents a single word detected by OCR, including its text, bounding box, and confidence.
    """
    text: str = Field(..., description="The recognized text of the word.")
    bbox: Bbox = Field(..., description="Bounding box of the word (x1, y1, x2, y2).")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score for the word recognition, ranging from 0.0 to 1.0.")

class OCRFrameResult(BaseFrameResult):
    """
    Represents the OCR results for a single image or frame.
    """
    full_text: str = Field(..., description="The concatenated full text recognized from the image/frame.")
    words: Optional[List[OCRWordResult]] = Field(default_factory=list, description="List of individual word results with bounding boxes and confidences.")
    mean_confidence: Optional[float] = Field(None, ge=0.0, le=100.0, description="Average confidence across all recognized words (0.0 to 1.0).")

# ───────────────────────────────  CLIP ‑ Embeddings  ───────────────────────
class EmbeddingFrameResult(BaseFrameResult):
    """
    Represents the embedding vector generated for an image or frame.
    """
    embedding: List[float] = Field(..., description="The embedding vector as a list of floats.")

# =============================================================================
# 2. Task-Specific Series Models
#    (These represent results for a sequence of frames/images, e.g., a video or a batch)
# =============================================================================

class TaskType(str, Enum):
    """
    Enum for different types of model tasks.
    """
    DETECTION = "detection"
    OCR = "ocr"
    EMBEDDING = "embedding"
    
class BaseTaskSeries(BaseModel):
    """
    Base model for a series of results for a specific task (e.g., from a video or a batch of images).
    """
    model_name: str = Field(..., description="Name of the model used (e.g., 'yolov8s', 'tesseract', 'clip-ViT-B-32').")
    total_items: int = Field(..., description="Total number of items (frames/images) processed in this series.")
    total_processing_time_ms: Optional[float] = Field(None, description="Время обработки кадра в миллисекундах.")    # The actual list of frame-level results will be in a concrete subclass (e.g., 'results' field)

class DetectionSeries(BaseTaskSeries):
    """
    Represents the object detection results for a series of frames/images.
    """
    results: List[ObjectDetectionResult] = Field(..., description="List of object detection results for each frame/image.")

class OCRSeries(BaseTaskSeries):
    """
    Represents the OCR results for a series of frames/images.
    """
    results: List[OCRFrameResult] = Field(..., description="List of OCR results for each frame/image.")

class EmbeddingSeries(BaseTaskSeries):
    """
    Represents the embedding results for a series of frames/images.
    """
    results: List[EmbeddingFrameResult] = Field(..., description="List of embedding results for each frame/image.")


# =============================================================================
# 3. API Response Envelope and Utility Models
# =============================================================================

class ModelsResponse(BaseModel):
    """Response model for available models endpoint."""
    available_models: Dict["TaskType", List[str]] = Field(..., description="List of available model names.")
    default_model: Optional[str] = Field(..., description="Name of the default model.")
    message: str = Field(..., description="Informational message.")
    
class CacheStatsResponse(BaseModel):
    """
    Схема ответа для эндпоинта /api/loaded_models (статус кэша).
    """
    model_name: str = Field(..., description="Name of the model in cache.")
    task_type: TaskType = Field(..., description="Type of task this model performs.") # Added task_type
    wrapper_class: str = Field(..., description="Python class name of the model wrapper.")
    first_load_at: str = Field(..., description="ISO 8601 timestamp when the model was first loaded into cache.") # Renamed
    last_used: str = Field(..., description="ISO 8601 timestamp when the model was last accessed.")
    idle_seconds: float = Field(..., description="Time in seconds since the model was last used.")
    use_count: int = Field(..., description="Number of times the model has been requested/used.") # Renamed
    estimated_mem_bytes: int = Field(..., description="Estimated memory (RAM/VRAM) used by the model in bytes.")

class UnloadModelResponse(BaseModel):
    """
    Response model for a successful model unload operation.
    """
    detail: str = Field(..., description="Confirmation message about the unloaded model.")

    

class EnvelopeResponse(BaseModel):
    """
    Standard envelope response structure for all API responses.
    This wrapper provides consistent metadata across different API endpoints
    and holds the task-specific results within its 'data' field.
    """
    task_type: TaskType = Field(..., description="The type of task performed by the API.")
    model_name: str = Field(..., description="The name of the model used for the task.")
    total_runtime_ms: float = Field(..., description="Total time taken to process the request (including I/O, preprocessing, inference) in milliseconds.")
    # The 'data' field now holds one of the Series types or a list of them
    data: Union[DetectionSeries, OCRSeries, EmbeddingSeries, List[DetectionSeries], List[OCRSeries], List[EmbeddingSeries]] = \
        Field(..., description="The actual response data, which is typically a series of results (e.g., DetectionSeries) or a list of such series.")
    message: Optional[str] = Field(None, description="Optional message related to the response.")
    
class FilesResponse(BaseModel):
    """
    Response model for listing available files on the server's FILES_PATH.
    """
    files: List[str] = Field(..., description="List of available file paths relative to FILES_PATH.")
    base_path: Optional[str] = Field(None, description="The base path (FILES_PATH) from which files are listed. None if FILES_PATH is not configured.")
    message: str = Field("Successfully retrieved file list.")