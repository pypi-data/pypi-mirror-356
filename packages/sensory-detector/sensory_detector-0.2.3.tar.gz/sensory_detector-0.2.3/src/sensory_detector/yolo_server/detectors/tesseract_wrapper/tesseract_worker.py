# src/sensory_detector/yolo_server/detectors/tesseract_worker.py
# ПОПЫТКА СОЗДАТЬ ВОРКЕР ДЛЯ МУЛЬТИПОТОКОВОЙ ОБРАБОТКИ TODO НЕ РЕАЛИЗОВАНА
import os
import logging
from typing import Any, Dict, Optional, Tuple

import numpy as np
import cv2
from PIL import Image

# Импортируем TesseractWrapper и его зависимости
from sensory_detector.yolo_server.detectors.tesseract_wrapper.tesseract_wrapper import (
    TesseractWrapper, TesseractConfig, TesseractError
)
from Services.Yolo.src.sensory_detector.yolo_server.app.config import OCRImageProcessingConfig
from sensory_detector.yolo_server.ocr.image_processor import OCRImageProcessor

# Глобальные переменные для хранения экземпляров в каждом worker-процессе
_tesseract_instance: Optional[TesseractWrapper] = None
_image_processor_instance: Optional[OCRImageProcessor] = None

# Настраиваем логгирование для worker-процессов
# TODO: Возможно, стоит получать конфиг логгирования из основного процесса
worker_logger = logging.getLogger(__name__)
worker_logger.setLevel(logging.DEBUG) # Или другой уровень в зависимости от env
handler = logging.StreamHandler() # Или использовать RotatingFileHandler
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(name)s | PID:%(process)d | %(message)s')
handler.setFormatter(formatter)
# Избегаем добавления нескольких хэндлеров
if not worker_logger.handlers:
    worker_logger.addHandler(handler)


def _worker_init(tess_config_dict: Dict[str, Any]):
    """
    Инициализирует TesseractWrapper и OCRImageProcessor в каждом worker-процессе.
    Эта функция вызывается ProcessPoolExecutor один раз при запуске worker'а.
    """
    global _tesseract_instance, _image_processor_instance
    try:
        worker_logger.info(f"Worker PID {os.getpid()} initializing Tesseract and ImageProcessor...")

        # Создаем объекты конфигурации из словарей
        tess_config = TesseractConfig.model_validate(tess_config_dict)

        # Создаем инстанс TesseractWrapper в этом процессе
        _tesseract_instance = TesseractWrapper(config=tess_config)
        worker_logger.info(f"Worker PID {os.getpid()}: TesseractWrapper initialized.")

    except Exception as e:
        # Логгируем ошибку инициализации worker'а, она может быть проглочена пулом
        worker_logger.error(f"Worker PID {os.getpid()} initialization failed: {e}", exc_info=True)
        # ВАЖНО: Не пробрасываем исключение здесь, так как это может остановить весь пул или вызвать проблемы.
        # Вместо этого, можно установить флаг или вернуть признак ошибки, если это возможно.
        # Но ProcessPoolExecutor ожидает успешного завершения initializer'а.
        # Самый безопасный вариант - залоггировать и, возможно, позволить последующим вызовам
        # _worker_process_frame обнаружить, что _tesseract_instance None.
        _tesseract_instance = None # Убеждаемся, что инстанс не создан, если произошла ошибка
        _image_processor_instance = None
        # Перебрасываем для ProcessPoolExecutor
        raise # Worker exit will be handled by the pool


def _worker_process_frame(
    frame_np: np.ndarray, # numpy array
    details: bool,
    params_dict: Dict[str, Any], # Дополнительные параметры для Tesseract.process_pil_image
) -> OCRResult:
    """
    Обрабатывает один кадр в worker-процессе, используя локальный TesseractWrapper.
    Эта функция вызывается методом map пула.
    """
    global _tesseract_instance, _image_processor_instance

    # Проверяем, был ли TesseractWrapper успешно инициализирован
    if _tesseract_instance is None:
        worker_logger.error(f"Worker PID {os.getpid()}: TesseractWrapper instance is None. Initialization likely failed.")
        raise TesseractError("Tesseract API instance not initialized in worker process.")

    worker_logger.debug(f"Worker PID {os.getpid()} processing frame...")

    try:
        # Конвертируем numpy array (CV2, BGR) в PIL (RGB)
        # Это должно выполняться в worker'е, т.к. worker получает numpy array
        if frame_np is None or frame_np.size == 0:
             worker_logger.warning(f"Worker PID {os.getpid()}: Received empty frame.")
             # Вернуть пустой результат OCR, а не ошибку
             return OCRResult(full_text="", words=[])

        try:
             # Используем cv2_to_pil из shared_input (или перенести сюда)
             # TODO: Ideally, image conversion/processing helpers should be in a common place or passed
             pil_image = Image.fromarray(cv2.cvtColor(frame_np, cv2.COLOR_BGR2RGB))
        except Exception as e:
             worker_logger.error(f"Worker PID {os.getpid()}: Failed to convert numpy to PIL: {e}", exc_info=True)
             raise RuntimeError(f"Failed to convert image for worker: {e}") from e

        # Применяем предобработку, если image_processor инициализирован
        processed_pil_image = pil_image
        if _image_processor_instance:
             try:
                  worker_logger.debug(f"Worker PID {os.getpid()}: Applying image processing...")
                  # ImageProcessor.process_image работает с PIL Image
                  processed_pil_image = _image_processor_instance.process_image(pil_image)
                  worker_logger.debug(f"Worker PID {os.getpid()}: Image processing complete.")
             except Exception as e:
                  worker_logger.error(f"Worker PID {os.getpid()}: Failed to apply image processing: {e}", exc_info=True)
                  # Решите, что делать при ошибке предобработки: пропустить кадр или упасть?
                  # Пока пробрасываем ошибку
                  raise RuntimeError(f"Failed to process image in worker: {e}") from e


        # Вызываем process_pil_image TesseractWrapper
        worker_logger.debug(f"Worker PID {os.getpid()}: Running Tesseract process_pil_image...")
        # params_dict содержит дополнительные параметры из запроса (psm, whitelist etc.)
        ocr_result = _tesseract_instance.process_pil_image(
            processed_pil_image,
            details=details,
            **params_dict
        )
        worker_logger.debug(f"Worker PID {os.getpid()}: Tesseract process_pil_image complete.")

        # OCRResult (Pydantic model) должен быть picklable
        return ocr_result

    except Exception as e:
        worker_logger.error(f"Worker PID {os.getpid()}: Error processing frame: {e}", exc_info=True)
        # Пробрасываем исключение, ProcessPoolExecutor его поймает и перешлет в основной процесс
        raise