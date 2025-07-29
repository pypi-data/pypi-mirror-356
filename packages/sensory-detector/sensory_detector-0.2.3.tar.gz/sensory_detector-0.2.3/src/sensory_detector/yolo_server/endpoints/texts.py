from __future__ import annotations

import asyncio
import gc
import logging
import time
from typing import Any, List, Sequence, Tuple, Union, Optional

import numpy as np
import torch
from fastapi import APIRouter, File, Form, HTTPException, Request, UploadFile
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY, HTTP_500_INTERNAL_SERVER_ERROR

from sensory_detector.yolo_server.detectors.detector_interface import ModelTaskType
from sensory_detector.yolo_server.app.model_utils import get_wrapper
from sensory_detector.yolo_server.endpoints.shared_input import load_frames, parse_processing_config, cv2_to_pil, pil_to_cv2 # Import helpers
from sensory_detector.yolo_server.endpoints.shared_output import (
    TaskType,
    make_response,
)
from sensory_detector.yolo_server.app.config import OCRImageProcessingConfig

from sensory_detector.models.models import OCRFrameResult, OCRSeries, TaskType
from sensory_detector.yolo_server.ocr.image_processor import OCRImageProcessor
from sensory_detector.yolo_server.video_analizer.video_processor import process_video_sync # Import for video processing


log = logging.getLogger(__name__)
router = APIRouter(prefix="/api/texts", tags=["ocr / texts"])


def _split(
    items: Sequence[np.ndarray | str | Any],
) -> Tuple[List[np.ndarray], List[Union[str, Any]]]:
    images, videos = [], []
    for o in items:
        (images if isinstance(o, np.ndarray) else videos).append(o)
    return images, videos


@router.post("")
async def recognize_texts(
    request: Request, # Request нужен для доступа к form(), чтобы достать proc_* параметры
    files: List[UploadFile] | None = File(None, description="Список файлов для загрузки"), # Добавляем description
    file: UploadFile | None = File(None, description="Одиночный файл для загрузки"), # Добавляем description
    path: str | None = Form(None, description="Абсолютный путь к файлу/видео на сервере (требует FILES_PATH)"), # Добавляем description
    roi: str | None = Form(None, description="ROI в формате JSON [[x1,y1],[x2,y2]] для применения перед инференсом"), # Добавляем description
    model_name: str | None = Form(None, description="Имя OCR-модели (например, 'tesseract', 'easyocr')"), # Добавляем description
    details: bool = Form(None, description="Включать детализация по словам (bbox, уверенность) в ответ"), # <-- Add details parameter
):
    tic = time.perf_counter()
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

        raw_items, _ = await load_frames(files=files, file=file, path=path, roi=roi)
        images_np, videos = _split(raw_items)


        # -------- proc_* → config -------------------------------------------
        wrapper = await get_wrapper(
        model_cache_instance,
        ModelTaskType.OCR, model_name 
    )


        all_series_results: List[OCRSeries] = []
        # ------------------- VIDEO ------------------------------------------
        if videos:
            loop = asyncio.get_running_loop()
            for idx, v_src in enumerate(videos):
                try:
                    # Pass the image_processor and 'details' parameter to video processing
                    video_frame_results: List[OCRFrameResult] = await asyncio.to_thread(
                        process_video_sync, v_src, wrapper, model_cache_instance, loop, image_processor,
                        details=details # Pass details to the detector's calls within video_processor
                    )
                    if video_frame_results:
                        total_video_time_ms = sum(r.processing_time_ms for r in video_frame_results if r.processing_time_ms is not None)
                        all_series_results.append(
                            OCRSeries(
                                model_name=wrapper.model_name,
                                total_items=len(video_frame_results),
                                total_processing_time_ms=total_video_time_ms,
                                results=video_frame_results
                            )
                        )
                except Exception as exc:
                    log.error("OCR video #%s error: %s", idx, exc, exc_info=True)
                    raise HTTPException(
                        HTTP_500_INTERNAL_SERVER_ERROR,
                        f"OCR failed on video #{idx}: {exc}",
                    ) from exc


        # ------------------- IMAGES -----------------------------------------
        if images_np:
            log.info(f"Starting image OCR processing for {len(images_np)} images.")
            
            processed_images_np: List[np.ndarray] = []

            # Apply image processing to static images
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
                 processed_images_np = images_np

            # Run detector batch processing on processed images
            if processed_images_np:
                static_image_frame_results: List[OCRFrameResult] = await asyncio.to_thread(
                    wrapper.detect_batch,
                    processed_images_np,
                    timestamps=[0.0] * len(processed_images_np), # Static images have 0 timestamp
                    frame_indices=list(range(len(processed_images_np))),
                    details=details # Pass details to the detector's batch call
                )
                log.debug(f"After calling detect_batch: static_image_frame_results type: {type(static_image_frame_results)}, value length: {len(static_image_frame_results)}") 
                if static_image_frame_results:
                    total_static_image_time_ms = sum(r.processing_time_ms for r in static_image_frame_results if r.processing_time_ms is not None)
                    all_series_results.append(
                        OCRSeries(
                            model_name=wrapper.model_name,
                            total_items=len(static_image_frame_results),
                            total_processing_time_ms=total_static_image_time_ms,
                            results=static_image_frame_results
                        )
                    )
            else:
                 log.warning("No processed static images to process.")

        _free_mem()

        if not all_series_results:
            raise HTTPException(
                HTTP_422_UNPROCESSABLE_ENTITY, "No valid images or video frames were processed."
            )

        final_payload_for_response: Union[OCRSeries, List[OCRSeries]]
        if len(all_series_results) == 1:
            final_payload_for_response = all_series_results[0]
        else:
            final_payload_for_response = all_series_results

        return make_response(TaskType.OCR, wrapper.model_name, final_payload_for_response, tic)

    except HTTPException:
        log.exception("HTTPException in /api/texts")
        raise
    except Exception as exc:
        log.error("Unexpected /api/texts error: %s", exc, exc_info=True)
        raise HTTPException(HTTP_500_INTERNAL_SERVER_ERROR, "Internal server error") from exc

def _free_mem() -> None:
    """Простая утилита для облегчения RAM/VRAM между батчами."""
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()