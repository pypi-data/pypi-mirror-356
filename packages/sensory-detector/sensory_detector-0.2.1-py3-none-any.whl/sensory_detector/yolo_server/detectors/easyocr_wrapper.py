
"""
EasyOCR → единый интерфейс Detector.
Поддерживает пакетную обработку (readtext_batched) и конвертацию
результата в список OCRWordResult.
src/sensory_detector/yolo_server/detectors/easyocr_wrapper.py
"""
from __future__ import annotations

import cv2, numpy as np, logging, time, os
import easyocr
from typing import List, Optional, Any
from pathlib import Path
import torch

from threading import Lock
from sensory_detector.models.models import OCRFrameResult, OCRWordResult, Bbox 
from sensory_detector.yolo_server.ocr.config import OCRImageProcessingConfig
from sensory_detector.yolo_server.ocr.image_processor import OCRImageProcessor
from sensory_detector.yolo_server.detectors.detector_interface import Detector, ModelTaskType

log = logging.getLogger(__name__)

class EasyOCRWrapper(Detector):
    _infer_lock = Lock()     
    def __init__(
        self,
        model_name: str = "easyocr",
        langs: tuple[str, ...] = ("ru", "en"),
        device=None,
    ):
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
        
        self._model_name = model_name
        self._reader = easyocr.Reader(list(langs), gpu=self.device.startswith("cuda"))
        log.info("EasyOCRWrapper loaded (%s, gpu=%s)", langs, self.device)

    # ─────────────────────────────── Detector API ─────────────────────────────
    @property
    def model_name(self) -> str:
        return self._model_name

    def task_type(self) -> ModelTaskType:
        return ModelTaskType.OCR

    # bytes → Detected list (single image)
    def detect_from_bytes(self, image_bytes: bytes, timestamp: float = 0.0, frame_index: int = -1, **kwargs: Any) -> OCRFrameResult:
        with self._infer_lock:
            frame = cv2.imdecode(
                np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR
            )
            return self._run_ocr_single(frame, timestamp, frame_index, **kwargs)

    def detect_from_file(self, file_path: str, timestamp: float = 0.0, frame_index: int = -1, **kwargs: Any) -> OCRFrameResult:
        with self._infer_lock:
            frame = cv2.imread(file_path)
            if frame is None:
                raise FileNotFoundError(file_path)
            return self._run_ocr_single(frame, timestamp, frame_index, **kwargs)

    def detect_from_frame(self, frame: np.ndarray, timestamp: float = 0.0, frame_index: int = -1, **kwargs: Any) -> OCRFrameResult | None:
        """
        Processes a single image frame (numpy array).
        """
        if frame is None or frame.size == 0:
            log.warning("Received empty frame for OCR processing.")
            return OCRFrameResult(full_text="", words=[], mean_confidence=None, frame_index=frame_index, timestamp=timestamp, processing_time_ms=0.0)
        
        # Call _run_ocr_single which wraps detect_batch for single frame processing
        # Pass details and any other kwargs
        return self._run_ocr_single(frame, timestamp, frame_index, **kwargs)


    # ─ batch helper (НЕ часть базового протокола, но общедоступно) ─
    def detect_batch(
        self,
        frames: List[np.ndarray],
        details: int = 1, # EasyOCR's detail=1 means word-level details
        beam_width: int = 8,
        batch_size: int = 96,
        workers: int = 0,
        timestamps: Optional[List[float]] = None, # Added for video processing
        frame_indices: Optional[List[int]] = None, # Added for video processing
    ) -> List[OCRFrameResult]:
        with self._infer_lock:
            tic = time.time()
            #processed = [self._preprocess(f) for f in frames]
            results = self._reader.readtext_batched(
                frames,
                detail=1 if details else 0,
                beamWidth=beam_width,
                batch_size=batch_size,
                workers=workers,
            )
            toc = (time.time() - tic) * 1000
            avg_processing_time_per_frame = toc / len(frames) if frames else 0.0 # <--- ДОБАВЛЕНО
            ocr_results: List[OCRFrameResult] = []
            for img_idx, img_words in enumerate(results):
                
                words = [
                    OCRWordResult(
                        text=w[1],
                        bbox=(
                            int(w[0][0][0]),
                            int(w[0][0][1]),
                            int(w[0][2][0]),
                            int(w[0][2][1]),
                        ),
                        confidence=float(w[2]),
                    )
                    for w in img_words
                ]
                full_text = " ".join([w.text for w in words])
                if full_text != '':
                    mean_conf = sum(w.confidence for w in words) / max(len(words), 1) if words else None
                    if mean_conf is not None:
                        mean_conf = round(mean_conf, 4) # Round to 4 decimal places for float precision
                
                    ocr_results.append(
                        OCRFrameResult(
                            full_text=full_text,
                            words=words if details else [], # Включаем слова только если запрошены детали
                            mean_confidence=mean_conf,
                            processing_time_ms=avg_processing_time_per_frame, # <--- ИСПРАВЛЕНИЕ
                            frame_index=frame_indices[img_idx] if frame_indices else img_idx,
                            timestamp=timestamps[img_idx] if timestamps else 0.0,
                        )
                    )
            return ocr_results
        
    def unload(self) -> None:
        """
        Unloads EasyOCR model resources.
        """
        log.info("Unloading EasyOCR model '%s'...", self._model_name)
        # EasyOCR doesn't explicitly provide a .close() method.
        # Deleting the reader instance is the primary way to release resources.
        try:
            del self._reader
            # Optionally, trigger Python's garbage collector
            import gc
            gc.collect()
            log.info("EasyOCR model '%s' unloaded successfully.", self._model_name)
        except Exception as e:
            log.warning("Error while unloading EasyOCR model '%s': %s", self._model_name, e, exc_info=True)

    def mem_bytes(self) -> int:
        # EasyOCR's memory footprint is mostly from its underlying models loaded by PyTorch/PaddlePaddle.
        # This is a rough estimate; true memory usage depends on loaded languages and GPU.
        # For GPU, it's typically a few hundred MB per language.
        # If we had a way to query torch.cuda.memory_allocated(), that would be better.
        return 0 # Placeholder for now, hard to get exact number without deeper integration


    def _run_ocr_single(self, frame: np.ndarray, timestamp: float = 0.0, frame_index: int = -1, details: bool = True) -> OCRFrameResult:
        """Вспомогательная функция для запуска OCR на одном кадре и возврата одного OCRFrameResult."""
        res_list = self.detect_batch([frame], details=details, timestamps=[timestamp], frame_indices=[frame_index])
        if res_list:
            return res_list[0]
        # In case EasyOCR returns an empty list for some reason, return a default empty OCRResult
        return OCRFrameResult(
            full_text="",
            words=[],
            mean_confidence=None,
            frame_index=frame_index,
            timestamp=timestamp,
            processing_time_ms=0.0
        )