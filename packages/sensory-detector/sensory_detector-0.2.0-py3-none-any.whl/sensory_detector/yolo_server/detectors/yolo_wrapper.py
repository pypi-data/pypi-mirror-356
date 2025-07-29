from ultralytics import YOLO
import cv2, os
import numpy as np
from typing import List, Optional, Any
from sensory_detector.models.models import DetectedObject, BoundingBox, ObjectDetectionResult
from pathlib import Path
from sensory_detector.yolo_server.app.config import config
import av
from mimetypes import guess_type        
from sensory_detector.yolo_server.video_analizer.video_processor import process_video_sync
from sensory_detector.yolo_server.detectors.detector_interface import Detector, ModelTaskType
import time

import logging
log = logging.getLogger(__name__)

# Try importing torch and check for CUDA availability gracefully for unload/mem_bytes
_torch_available = False
try:
    import torch
    _torch_available = True
except ImportError:
    log.warning("Torch not installed, CUDA memory estimation disabled.")



class YOLOv8Wrapper(Detector): # Убедитесь, что наследуется от Detector

    def __init__(self, model_name: str, device=None):
        """
        Инициализирует враппер YOLOv8.

        Args:
            model_name: Имя модели для загрузки (например, 'yolov8s').
                        Ultralytics попытается найти model_name.pt локально
                        (включая свой кэш) или скачать его.
        """
        self._model_name = model_name
        model_path = config.WEIGHTS_DIR / f"{model_name}.pt"
        log.debug(f"Initializing YOLOv8 model: {model_name}")
    
        # Determine device - base model should be on 'cuda:0' for DataParallel
        if device:
            self.device = device
        else:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"

        if self.device.startswith('cuda') and torch.cuda.device_count() >= 1:
            base_device_id = int(os.environ.get("WORKER_PHYSICAL_GPU_ID", "0"))
            used_gpu_ids = list(range(torch.cuda.device_count()))
            self.device = f"cuda:{base_device_id}"
            log.info(f"Using on devices: {used_gpu_ids}. Base device set to: {self.device}")
        else:
            pass
        
        
        if not model_path.exists():
            log.warning(f"Model weights not found at {model_path}. Attempting to download '{model_name}.pt'...")
            self.model = YOLO(f"{model_name}.pt")
            downloaded_file = Path(f"{model_name}.pt")

            if downloaded_file.exists():
                downloaded_file.rename(model_path)
                log.debug(f"Model weights successfully moved to {model_path}.")
            else:
                raise FileNotFoundError(f"Файл {downloaded_file} не найден после загрузки.")
        else:
            log.debug(f"Model weights found at {model_path}.")
            self.model = YOLO(str(model_path))
            log.debug("Model loaded successfully.")
            
        self.model.to(self.device)

    @property
    def model_name(self) -> str:
        return self._model_name
    
    def task_type(self):
        return ModelTaskType.DETECTION

    def detect_from_file(self, file_path: str, timestamp: float = 0.0, frame_index: int = -1, **kwargs: Any) -> ObjectDetectionResult:
        """
        Processes a single image from a file path. Returns single ObjectDetectionResult.
        Videos are handled by process_video_sync.
        """
        mime, _ = guess_type(file_path)
        if not mime or not mime.startswith("image/"):
             raise ValueError(f"Unsupported file type for single image detection: {file_path} (mime: {mime})")

        img = cv2.imread(file_path)
        if img is None:
            raise IOError(f"Не удалось прочитать изображение: {file_path}")

        # _detect возвращает List[DetectedObject], оборачиваем его в ObjectDetectionResult
        detections = self._detect(img, timestamp=timestamp, frame_index=frame_index)
        return ObjectDetectionResult(
            frame_index=frame_index,
            timestamp=timestamp,
            detections=detections,
            processing_time_ms=0.0
        )

    # bytes
    def detect_from_bytes(self, image_bytes: bytes, timestamp: float = 0.0, frame_index: int = -1, **kwargs: Any) -> ObjectDetectionResult:
        #start_time = time.perf_counter() # <--- ДОБАВЛЕНО
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError("Could not decode image from bytes.")
        detections = self._detect(img, timestamp=timestamp, frame_index=frame_index)
        #processing_time_ms = (time.perf_counter() - start_time) * 1000.0 # <--- ДОБАВЛЕНО
        return ObjectDetectionResult(
            frame_index=frame_index,
            timestamp=timestamp,
            detections=detections,
            processing_time_ms=0.0
        )
    
    # ndarray
    def detect_from_frame(self, frame: np.ndarray, timestamp: float = 0.0, frame_index: int = -1, **kwargs: Any) -> ObjectDetectionResult:
        """Detects objects in a video frame (numpy array)."""
        #start_time = time.perf_counter() # <--- ДОБАВЛЕНО
        detections = self._detect(frame, timestamp=timestamp, frame_index=frame_index)
        #processing_time_ms = (time.perf_counter() - start_time) * 1000.0 # <--- ДОБАВЛЕНО
        return ObjectDetectionResult(
            frame_index=frame_index,
            timestamp=timestamp,
            detections=detections,
            processing_time_ms=0.0 # <--- ИСПРАВЛЕНИЕ
        )


    def _detect(self, img: np.ndarray, timestamp: float = 0.0, frame_index: int = -1) -> List[DetectedObject]:
        log.debug("Running YOLO inference...")
        results = self.model(img, verbose=False) # results is List[Results] for single image input
        detections: List[DetectedObject] = []

        # Предполагается, что results содержит один объект результата для одного входного изображения
        if results and hasattr(results[0], 'boxes') and results[0].boxes is not None:
            boxes = results[0].boxes
            for i, box in enumerate(boxes):
                if len(box.cls) == 0 or len(box.conf) == 0 or len(box.xyxy) == 0:
                     log.warning(f"Skipping incomplete box data: cls={box.cls}, conf={box.conf}, xyxy={box.xyxy}")
                     continue
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                xyxy = box.xyxy[0].tolist()

                bbox = BoundingBox(
                    x1=xyxy[0],
                    y1=xyxy[1],
                    x2=xyxy[2],
                    y2=xyxy[3]
                )

                object_name = "unknown"
                if hasattr(self.model, 'names') and cls in self.model.names:
                    object_name = self.model.names[cls]

                detections.append(
                    DetectedObject(
                        index=i,
                        object_name=object_name,
                        confidence=conf,
                        bounding_box=bbox
                    )
                )
        return detections

    
    
    # Добавим вспомогательный метод для обработки DetectedObject
    def _process_video(self, video_path: str) -> List[ObjectDetectionResult]:
        """
        Processes a video file frame by frame using pyAV (blocking operation).
        This method is designed to be run inside a thread pool.
        """
        log.info(f"Processing video file: {video_path}")
        detection_frames: List[ObjectDetectionResult] = []
        container = None # Инициализация вне try
        try:
            # av.open является блокирующей операцией
            container = av.open(video_path)
            # Берем первый видео стрим
            try:
                stream = container.streams.video[0]
            except IndexError:
                log.error(f"No video stream found in {video_path}")
                raise ValueError(f"No video stream found in file: {video_path}")

            # Decode video frames - this loop is CPU bound
            for frame_index, frame in enumerate(container.decode(stream)):
                try:
                    # Convert frame to numpy array (blocking)
                    img = frame.to_ndarray(format="bgr24")
                    # Calculate timestamp
                    # frame.time * stream.time_base gives timestamp in seconds
                    # If frame.time is None or not reliable, use frame index and stream rate
                    timestamp = float(frame.time) if frame.time is not None else frame_index / stream.rate
                    # Run detection on the frame
                    detections = self.detect_from_frame(img, timestamp=timestamp)
                    # Append results for this frame
                    detection_frames.append(ObjectDetectionResult(frame_index=frame_index, 
                                                                  timestamp=timestamp, 
                                                                  detections=detections,
                                                                  processing_time_ms=0.0 # НЕ РАБОТАЕТ. НУЖНО ПРИДУМАТЬ СПОСБ ЗАПУСКА МЕТРИКИ, НО ЧТОБЫ НЕ ВЛИЯЛО НА РЕСУРС
                                                                  ))
                    log.debug(f"Processed frame {frame_index} at {timestamp:.2f}s with {len(detections)} detections.")

                except Exception as e:
                     log.error(f"Error processing frame {frame_index}: {e}", exc_info=True)
                     # Decide how to handle frame errors: skip frame or stop? Skipping frame for now.
                     # Continue to the next frame

        except av.AVError as e:
            log.error(f"Error opening or processing video file {video_path} with pyAV: {e}", exc_info=True)
            raise IOError(f"Could not process video file {video_path}. Is it a valid video?") from e
        except Exception as e:
            log.error(f"An unexpected error occurred during video processing {video_path}: {e}", exc_info=True)
            raise RuntimeError(f"An unexpected error occurred during video processing.") from e
        finally:
            # Ensure container is closed even if errors occur
            if container:
                try:
                    container.close()
                    log.debug(f"Video container for {video_path} closed.")
                except Exception as e:
                    log.warning(f"Error closing video container for {video_path}: {e}", exc_info=True)


        log.info(f"Finished processing video file: {video_path}. Total frames processed: {len(detection_frames)}")
        return detection_frames

    def detect_batch(self, frames: List[np.ndarray], timestamps: Optional[List[float]] = None, frame_indices: Optional[List[int]] = None, **kwargs: Any) -> List[ObjectDetectionResult]:
        """
        Выполняет детекцию объектов на батче изображений.

        Args:
            frames: Список изображений как numpy array.
            timestamps: Optional list of timestamps for each frame.
            frame_indices: Optional list of frame indices for each frame.

        Returns:
            Список результатов детекции для каждого изображения в батче (List[ObjectDetectionResult]).

        Raises:
            RuntimeError: Если модель не загружена или внутренняя ошибка инференса.
        """
        # Проверка, что модель загружена (устойчивость к unload)
        if self.model is None:
            log.error(f"Attempted to use unloaded YOLO model '{self._model_name}'.")
            raise RuntimeError(f"YOLO model '{self._model_name}' is unloaded.")

        if not frames:
             log.debug("Received empty batch for YOLO processing.")
             return [] # Вернуть пустой список для пустого батча

        log.debug(f"Running YOLO inference for batch of {len(frames)} images...")
        try:
            # Вызываем метод predict модели Ultralytics с батчем
            # Передаем дополнительные параметры инференса из kwargs
            # predict() с List[np.ndarray] нативно обрабатывает батч
            results_list = self.model.predict(frames, verbose=False) # results_list is List[Results]

            batch_detection_results: List[ObjectDetectionResult] = []
            batch_start_time = time.perf_counter()
            # results_list содержит один Results объект для каждого изображения в батче
            if results_list:
                 for i, result in enumerate(results_list):
                    current_frame_detections: List[DetectedObject] = []
                    if hasattr(result, 'boxes') and result.boxes is not None:
                        boxes = result.boxes
                        for j, box in enumerate(boxes):
                            if len(box.cls) == 0 or len(box.conf) == 0 or len(box.xyxy) == 0:
                                log.warning(f"Skipping incomplete box data: cls={box.cls}, conf={box.conf}, xyxy={box.xyxy}")
                                continue # Пропускаем некорректные данные
                            cls = int(box.cls[0])
                            conf = float(box.conf[0])
                            xyxy = box.xyxy[0].tolist()

                            bbox = BoundingBox(
                                x1=xyxy[0],
                                y1=xyxy[1],
                                x2=xyxy[2],
                                y2=xyxy[3]
                            )
                            object_name = "unknown"
                            if hasattr(self.model, 'names') and cls in self.model.names:
                                object_name = self.model.names[cls]
                            # else: log.warning(...)

                            current_frame_detections.append(
                                DetectedObject(
                                    index=j, # Индекс внутри этого кадра
                                    object_name=object_name,
                                    confidence=conf,
                                    bounding_box=bbox
                                )
                            )
                    
                    batch_total_time_ms = (time.perf_counter() - batch_start_time) * 1000.0
                    avg_processing_time_per_frame = batch_total_time_ms / len(frames) if frames else 0.0 # <--- ДОБАВЛЕНО

                    # Создать ObjectDetectionResult для этого кадра
                    batch_detection_results.append(
                        ObjectDetectionResult(
                            frame_index=frame_indices[i] if frame_indices else i,
                            timestamp=timestamps[i] if timestamps else 0.0,
                            detections=current_frame_detections,
                            processing_time_ms=avg_processing_time_per_frame # <--- ИСПРАВЛЕНИЕ
                        )
                    )

            log.debug(f"Finished YOLO inference for batch. Processed {len(frames)} images in {batch_total_time_ms:.2f} ms.")
            return batch_detection_results

        except Exception as e:
            log.error(f"Error during YOLO batch inference for model '{self._model_name}': {e}", exc_info=True)
            # Оборачиваем ошибку инференса в RuntimeError
            raise RuntimeError(f"YOLO batch inference failed for model '{self._model_name}': {e}") from e


    def unload(self) -> None:
        """
        Освобождает VRAM / RAM.  Вызывается Cache-менеджером,
        когда модель простаивала дольше MODEL_CACHE_TIMEOUT_SEC.
        """
        log.info("Unloading YOLO model '%s' from memory …", self._model_name)
        try:
            del self.model
            #torch.cuda.empty_cache()   
        except Exception as e:
            log.warning("Error while unloading model '%s': %s",
                           self._model_name, e, exc_info=True)