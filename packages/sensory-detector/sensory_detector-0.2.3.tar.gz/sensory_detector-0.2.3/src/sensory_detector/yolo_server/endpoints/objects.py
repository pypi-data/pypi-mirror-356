from __future__ import annotations

import asyncio
import logging
import time
from typing import Any, List, Sequence, Tuple, Union, Optional

import numpy as np
from fastapi import APIRouter, File, Form, HTTPException, Request, UploadFile
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from sensory_detector.models.models import (
    ObjectDetectionResult, # Используем новое имя
    DetectionSeries,       # Используем новую модель Series
    DetectedObject,        # Все еще используется для отдельных объектов
    TaskType,              # Enum для shared_output
)
from sensory_detector.yolo_server.detectors.detector_interface import (
    ModelTaskType,
)
from sensory_detector.yolo_server.app.model_utils import get_wrapper
from sensory_detector.yolo_server.endpoints.shared_input import load_frames, parse_processing_config, cv2_to_pil, pil_to_cv2 # Import helpers
from sensory_detector.yolo_server.endpoints.shared_output import (
    TaskType,
    make_response,
)
from sensory_detector.yolo_server.video_analizer.video_processor import (
    process_video_sync,
)

from sensory_detector.yolo_server.app.config import OCRImageProcessingConfig
from sensory_detector.yolo_server.ocr.image_processor import OCRImageProcessor

router = APIRouter(prefix="/api/objects", tags=["objects"])
log = logging.getLogger(__name__)


def _split_sources(
    items: Sequence[np.ndarray | str | Any],
) -> tuple[list[np.ndarray], list[Union[str, Any]]]:
    """Разделяет источники на картинки (np.ndarray) и видео (str | file-like)."""
    images: list[np.ndarray] = []
    videos: list[Union[str, Any]] = []
    for it in items:
        if isinstance(it, np.ndarray):
            images.append(it)
        else:  # всё, что не ndarray, считаем видео-источником
            videos.append(it)
    return images, videos


@router.post("")
async def detect_objects(
    request: Request,
    files: List[UploadFile] | None = File(None, description="Список файлов"),
    file: UploadFile | None = File(None, description="Одиночный файл"),
    path: str | None = Form(None, description="Путь на сервере"),
    roi: str | None = Form(None, description="ROI [[x1,y1],[x2,y2]]"),
    model_name: str | None = Form(None, description="Имя YOLO-модели"),
):
    """Обработка изображений и/или видео любыми комбинациями."""
    tic = time.time()
    try:
        model_cache_instance = request.app.state.model_cache # Get model_cache instance from app.state

        form_data = await request.form()
        img_proc_config: Optional[OCRImageProcessingConfig] = parse_processing_config(form_data)
        image_processor: Optional[OCRImageProcessor] = None
        if img_proc_config and img_proc_config.enabled:
             log.debug("Image processing is enabled, creating processor.")
             # OCRImageProcessor uses PIL, need cv2_to_pil/pil_to_cv2 wrappers
             image_processor = OCRImageProcessor(config=img_proc_config)
        elif img_proc_config:
             log.debug("Image processing config found but disabled.")
        else:
             log.debug("No image processing config found in request.")
        # ---- загружаем данные --------------------------------------------------
        frames_data, _ = await load_frames(files=files, file=file, path=path, roi=roi)

        # ---- детектор ----------------------------------------------------------
        detector = await get_wrapper(
            model_cache_instance,
            ModelTaskType.DETECTION, model_name)

        # ---- делим на картинки и видео ----------------------------------------
        images_np, videos = _split_sources(frames_data)
        loop = asyncio.get_running_loop()
        all_detection_series: List[DetectionSeries] = []

        # ───────────── 1. видео -------------------------
        for vid_idx, video_source in enumerate(videos):
            video_start_time = time.perf_counter()
            try:
                # process_video_sync должен возвращать List[ObjectDetectionResult]
                det_frames: List[ObjectDetectionResult] = await asyncio.to_thread(
                    process_video_sync, video_source, detector, model_cache_instance, loop, image_processor
                )
                video_processing_time_ms = (time.perf_counter() - video_start_time) * 1000
                all_detection_series.append(
                    DetectionSeries(
                        model_name=detector.model_name, # Убедитесь, что вызывается .model_name()
                        results=det_frames,
                        total_items=len(det_frames),
                        total_processing_time_ms=video_processing_time_ms
                    )
                )
            except Exception as exc:  # noqa: BLE001
                log.error("Video #%s processing error: %s", vid_idx, exc, exc_info=True)
                raise HTTPException(
                    HTTP_500_INTERNAL_SERVER_ERROR,
                    f"Video #{vid_idx} analysis error: {exc}",
                ) from exc

       

        # ───────────── 2. изображения ------------------------------------------
        if images_np:
            images_processing_start_time = time.perf_counter()
            processed_images_np: List[np.ndarray] = []

            # --- Применение обработки изображений к статическим изображениям ---
            if image_processor:
                 log.debug("Applying image processing to static images...")
                 pil_images = await asyncio.to_thread(lambda imgs: [cv2_to_pil(img) for img in imgs], images_np)
                 processed_pil_images = await asyncio.gather(*[
                     asyncio.to_thread(image_processor.process_image, pil_img) for pil_img in pil_images
                 ])
                 processed_images_np = await asyncio.to_thread(lambda pil_imgs: [pil_to_cv2(pil_img) for pil_img in processed_pil_images], processed_pil_images)
                 log.debug(f"Finished image processing for {len(images_np)} static images.")
            else:
                 log.debug("No image processing applied to static images.")
                 processed_images_np = images_np # Используем сырые изображения, если нет процессора

            # Пакетный режим обнаружения
            batch_detections_raw: List[ObjectDetectionResult] # Changed type hint as detector.detect_batch now returns List[ObjectDetectionResult]
            if hasattr(detector, "detect_batch") and callable(detector.detect_batch):
                batch_detections_raw = await asyncio.to_thread(
                    detector.detect_batch, processed_images_np,
                    timestamps=[float(i) for i in range(len(processed_images_np))],
                    frame_indices=[i for i in range(len(processed_images_np))]
                )
            else:
                tasks = [
                    asyncio.to_thread(detector.detect_from_frame, img, float(i), i)
                    for i, img in enumerate(processed_images_np)
                ]
                batch_detections_raw = await asyncio.gather(*tasks)

            # batch_detections_raw уже является List[ObjectDetectionResult], поэтому нет необходимости в дополнительном преобразовании
            img_detection_results = batch_detections_raw # Use directly
            images_processing_time_ms = (time.perf_counter() - images_processing_start_time) * 1000

            all_detection_series.append(
                DetectionSeries(
                    model_name=detector.model_name,
                    results=img_detection_results,
                    total_items=len(img_detection_results),
                    total_processing_time_ms=images_processing_time_ms
                )
            )

        # ---- финальная полезная нагрузка -------------------------------------------------
        if not all_detection_series:
            raise HTTPException(
                HTTP_500_INTERNAL_SERVER_ERROR, "No valid data found in request to process."
            )

        # Возвращаем одну серию, если она одна, или список серий, если несколько источников
        final_payload: Union[DetectionSeries, List[DetectionSeries]]
        if len(all_detection_series) == 1:
            final_payload = all_detection_series[0]
        else:
            final_payload = all_detection_series

        return make_response(
            TaskType.DETECTION,
            detector.model_name, # Убедитесь, что вызывается .model_name()
            final_payload,
            tic
        )

    except HTTPException:
        log.exception("HTTPException in /api/objects")
        raise
    except Exception as exc:
        log.error("Unexpected /api/objects error: %s", exc, exc_info=True)
        raise HTTPException(
            HTTP_500_INTERNAL_SERVER_ERROR, "Internal server error"
        ) from exc