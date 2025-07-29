"""
Bridge-класс: сводит «тяжёлый» TesseractWrapper (C-API) к минимальному
протоколу Detector, который использует весь сервер.

Поддерживает:
• detect_from_bytes / detect_from_frame / detect_from_file
• detect_batch(frames, detail=0|1, **extra)
• thread-safe инференс (lock)
• передачу OCRImageProcessingConfig извне — одинаково с EasyOCR
"""

from __future__ import annotations

import threading
from pathlib import Path
from typing import List, Any, Optional
import time 
import numpy as np
import cv2
from PIL import Image

# ---- импорт ядра ----------------------------------------------------
# Исправьте путь, если ваш TesseractWrapper лежит в другом пакете
from sensory_detector.yolo_server.detectors.detector_interface import Detector, ModelTaskType
from sensory_detector.yolo_server.app.config import TesseractConfig, OCRImageProcessingConfig, load_tesseract_config
from sensory_detector.models.models import OCRFrameResult, OCRWordResult, Bbox # Обновленный импорт import
from sensory_detector.yolo_server.ocr.image_processor import OCRImageProcessor
from sensory_detector.yolo_server.detectors.tesseract_wrapper.tesseract_wrapper import TesseractWrapper # Correct import path for TesseractWrapper
import logging

log = logging.getLogger(__name__)
# ---------------------------------------------------------------------


class TesseractOCRWrapper(Detector):
    """
    Лёгкая обёртка над C-API Tesseract.

    Parameters
    ----------
    model_name : str
        Идентификатор модели в кэше/эндпоинте (`model_name=tesseract`).
    tess_config : TesseractConfig | None
        Полная конфигурация «движка» Tesseract (datapath, lang, psm…).
        Если None — берётся конфиг по умолчанию.
    img_proc_cfg : OCRImageProcessingConfig | None
        Конфиг предобработки изображений (resize, borders, B&W…).
        Если указан, подменяет `config.image_processing`.
    """

    _infer_lock = threading.Lock()  # потоковая безопасность Easy-OCR стиля

    # -----------------------------------------------------------------
    def __init__(
        self,
        model_name: str = "tess",
        tess_config: Optional[TesseractConfig] = None,
    ) -> None:
        self._model_name = model_name
        self._tess_cfg = tess_config or TesseractConfig()  # type: ignore

        # если отдельно дали конфиг пред-обработки – подменяем

        self._core = TesseractWrapper(self._tess_cfg)

    # -----------------------------------------------------------------
    # Detector protocol
    # -----------------------------------------------------------------
    @property
    def model_name(self) -> str:  # noqa: D401
        return self._model_name


    def task_type(self) -> ModelTaskType:
        """Возвращает тип задачи, которую выполняет этот детектор (OCR)."""
        return ModelTaskType.OCR 

    # ---- helpers ----------------------------------------------------
    @staticmethod
    def _cv2_to_pil(frame: np.ndarray) -> Image.Image:
        return Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    # ---- basic API ---------------------------------------------------
    def detect_from_bytes(self, image_bytes: bytes, timestamp: float = 0.0, frame_index: int = -1, details: bool = True, **kwargs: Any) -> OCRFrameResult:
        arr = cv2.imdecode(
            np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR
        )
        return self.detect_from_frame(arr, timestamp, frame_index, details, **kwargs)

    def detect_from_frame(
        self,
        frame: np.ndarray,
        timestamp: float = 0.0,
        frame_index: int = -1,
        details: bool = True, # Параметр details передается
        **params: Any,
    ) -> OCRFrameResult | None: # Изменен тип возвращаемого значения
        with self._infer_lock:
            start_time = time.perf_counter()
            pil_img_raw = self._cv2_to_pil(frame)

            # _core.process_pil_image теперь должен возвращать OCRFrameResult
            res: OCRFrameResult | None = self._core.process_pil_image(
                pil_img_raw, details=details, **params
            )
            if res:
                processing_time_ms = (time.perf_counter() - start_time) * 1000.0

                # Заполняем поля, которые не зависят от _core (timestamp, model_name, frame_index)
                res.frame_index = frame_index
                res.timestamp = timestamp
                res.processing_time_ms = processing_time_ms # Убедимся, что время также заполняется
            
                return res # Возвращаем одиночный OCRFrameResult
    
    def detect_from_file(self, file_path: str, timestamp: float = 0.0, frame_index: int = -1, details: bool = True, **kwargs: Any) -> OCRFrameResult:
        frame = cv2.imread(str(Path(file_path)))
        if frame is None:
            raise FileNotFoundError(file_path)
        return self.detect_from_frame(frame, timestamp, frame_index, details, **kwargs)


    # ---- batch -------------------------------------------------------

    def detect_batch(
        self,
        frames: List[np.ndarray],
        details: bool = None, # Изменено с detail:int на details:bool
        timestamps: Optional[List[float]] = None,
        frame_indices: Optional[List[int]] = None,
        **params: Any,
    ) -> List[OCRFrameResult]: # Изменен тип возвращаемого значения
        results: List[OCRFrameResult] = []
        with self._infer_lock:
            for i, fr in enumerate(frames):
                start_time_frame = time.perf_counter()
                pil_img_raw = self._cv2_to_pil(fr)
                # _core.process_pil_image теперь должен возвращать OCRFrameResult
                
                res: OCRFrameResult | None = self._core.process_pil_image(
                    pil_img_raw, details=details, **params
                )
                if res:
                    processing_time_ms = (time.perf_counter() - start_time_frame) * 1000.0

                    # Заполняем поля, которые не зависят от _core (timestamp, model_name, frame_index)
                    res.frame_index = frame_indices[i] if frame_indices else i
                    res.timestamp = timestamps[i] if timestamps else float(i)
                    res.processing_time_ms = processing_time_ms # Время на кадр

                    results.append(res)
        return results

    # ---- housekeeping -----------------------------------------------

    def unload(self) -> None:
        """Releases Tesseract model resources."""
        log.info("Unloading Tesseract model '%s'...", self._model_name)
        try:
            self._core.unload()
            log.info("Tesseract model '%s' unloaded successfully.", self._model_name)
        except Exception as e:
            log.warning("Error while unloading Tesseract model '%s': %s",
                            self._model_name, e, exc_info=True)

    def mem_bytes(self) -> int:
        """Estimates memory used by the model."""
        return 0 # Tesseract's memory usage is hard to query from C API reliably.