# src/sensory_detector/yolo_server/video_analizer/video_processor.py
from __future__ import annotations

import asyncio
import io
import logging
from typing import Any, List, Union, Optional

from sensory_detector.yolo_server.video_analizer.frame_reader import (
    FrameReader,
    FrameReadError,
)
from sensory_detector.yolo_server.detectors.detector_interface import (
    Detector,
    ModelTaskType,
)
from sensory_detector.models.models import (
    ObjectDetectionResult,
    OCRFrameResult,
    EmbeddingFrameResult,
)
from sensory_detector.yolo_server.ocr.image_processor import OCRImageProcessor

_logger = logging.getLogger(__name__)

# ------------- «умолчания». При желании можно вынести в конфиг -------------
DEFAULT_BATCH_SIZES = {
    ModelTaskType.EMBEDDING: 64,   # CLIP
    ModelTaskType.DETECTION: 16,   # YOLO
    ModelTaskType.OCR: 2,          # Tesseract / EasyOCR
}
PING_EVERY_N_FRAMES = 15


def _ping_cache(model_cache, detector: Detector, loop: asyncio.AbstractEventLoop) -> None:
    """
    Обновляем TTL модели. Запускается в event-loop,
    чтобы не блокировать рабочий поток FrameReader-а.
    """
    asyncio.run_coroutine_threadsafe(
        model_cache._async_update_activity(detector.model_name), loop  # type: ignore[attr-defined]
    )


def _effective_batch_size(detector: Detector, user_value: int | None) -> int:
    """
    Вычисляем реальный размер партии:
    1) если пользователь явно передал batch_size – используем его;
    2) иначе смотрим на тип задачи (embedding / detection / ocr).
    """
    if user_value and user_value > 0:
        return user_value

    try:
        return DEFAULT_BATCH_SIZES[detector.task_type()]
    except Exception:
        # если детектор некорректно реализовал task_type() – подстрахуемся
        return 4


def process_video_sync(
    video_source: Union[str, io.BufferedIOBase],
    detector: Detector,
    model_cache: "ModelCache",
    event_loop: asyncio.AbstractEventLoop,
    image_processor: Optional[OCRImageProcessor] = None,
    batch_size: int | None = None,
    **kwargs: Any,
) -> List[Union[ObjectDetectionResult, OCRFrameResult, EmbeddingFrameResult]]:
    """
    Блокирующая (вызывается в thread-pool) обработка видеофайла/стрима.

    1. Кадры декодируются pyAV-ом на CPU.
    2. Накопливаются в буфер до `batch_size`.
    3. Скопом отправляются в `detector.detect_batch`.
    4. Результаты собираются в «плоский» список и возвращаются вызывающему.
    """
    src_desc = (
        video_source
        if isinstance(video_source, str)
        else f"{type(video_source).__name__}(in-mem)"
    )
    _logger.info("Processing video source: %s", src_desc)

    # ------------------------------------------------------------------ #
    #  Настройка параметров                                              #
    # ------------------------------------------------------------------ #
    batch_size = _effective_batch_size(detector, batch_size)
    _logger.debug("Effective batch_size for %s → %d", detector.task_type(), batch_size)

    all_results: List[
        Union[ObjectDetectionResult, OCRFrameResult, EmbeddingFrameResult]
    ] = []

    frames: list[Any] = []        # буфер изображений / тензоров – тип зависит от detect_batch
    timestamps: list[float] = []
    indices: list[int] = []

    # ------------------------------ helpers --------------------------- #
    def _flush_batch() -> None:
        """
        Внутренняя функция: передаёт накопленные кадры в detect_batch
        и очищает буферы. Вызывается когда буфер заполнен или в самом
        конце обработки файла.
        """
        if not frames:
            return

        try:
            batch_res = detector.detect_batch(  # type: ignore[arg-type]
                frames, timestamps=timestamps, frame_indices=indices, **kwargs
            )
            all_results.extend(batch_res)
            _logger.debug(
                "Flushed %d frames → %d results (total=%d)",
                len(frames),
                len(batch_res),
                len(all_results),
            )
        finally:  # чтобы освободить память при любой ошибке
            frames.clear()
            timestamps.clear()
            indices.clear()

    # ------------------------------ main loop ------------------------- #
    try:
        with FrameReader(video_source) as reader:
            for idx, raw_frame_bgr, ts in reader.read_frames():
                # Пинг кеша раз в N кадров
                if idx % PING_EVERY_N_FRAMES == 0:
                    _ping_cache(model_cache, detector, event_loop)

                # --- опциональная предобработка для OCR/др. ---
                frame_bgr = raw_frame_bgr
                if image_processor and image_processor.enabled:
                    try:
                        from sensory_detector.yolo_server.endpoints.shared_input import (
                            cv2_to_pil,
                            pil_to_cv2,
                        )

                        frame_bgr = pil_to_cv2(
                            image_processor.process_image(cv2_to_pil(raw_frame_bgr))
                        )
                    except Exception as e:  # noqa: BLE001
                        _logger.warning(
                            "Image-processing failed on frame %d: %s (skip preproc)",
                            idx,
                            e,
                        )

                # ----- наполняем буферы -----
                frames.append(frame_bgr)
                timestamps.append(ts)
                indices.append(idx)

                # если достигли лимита → отдаём партию на инференс
                if len(frames) >= batch_size:
                    _flush_batch()

            # обработать «хвост», если остался
            _flush_batch()

    except FrameReadError as e:
        raise RuntimeError(f"Video processing error: {e}") from e
    except Exception as e:  # noqa: BLE001
        _logger.error("Unexpected error during video processing: %s", e, exc_info=True)
        raise

    _logger.info(
        "Finished %s. Frames processed: %d, results collected: %d",
        src_desc,
        len(all_results),
        len(all_results),
    )
    return all_results