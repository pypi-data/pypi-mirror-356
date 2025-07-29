from __future__ import annotations

import asyncio
import gc
import logging
import time
from typing import Any, List, Sequence, Tuple, Union, Optional

import numpy as np
import torch
from fastapi import APIRouter, File, Form, HTTPException, UploadFile, Request 
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY, HTTP_500_INTERNAL_SERVER_ERROR

from sensory_detector.models.models import EmbeddingSeries, EmbeddingFrameResult # <--- ИСПРАВЛЕНИЕ: Добавлен EmbeddingFrameResult
from sensory_detector.yolo_server.detectors.detector_interface import ModelTaskType # Обновленный импорт
from sensory_detector.yolo_server.app.model_utils import get_wrapper
from sensory_detector.yolo_server.endpoints.shared_input import load_frames, parse_processing_config, cv2_to_pil, pil_to_cv2
from sensory_detector.yolo_server.endpoints.shared_output import TaskType, make_response # <--- ИСПРАВЛЕНИЕ: Добавлен make_response
from sensory_detector.yolo_server.app.config import OCRImageProcessingConfig # <--- ИСПРАВЛЕНИЕ: Корректный импорт
from sensory_detector.yolo_server.ocr.image_processor import OCRImageProcessor # <--- ИСПРАВЛЕНИЕ: Добавлен импорт, если используется
from sensory_detector.yolo_server.video_analizer.video_processor import process_video_sync # <--- ИСПРАВЛЕНИЕ: Добавлен импорт
ACTIVITY_UPDATE_INTERVAL_FRAMES = 15

log = logging.getLogger(__name__)
router = APIRouter(prefix="/api/embeddings", tags=["embeddings"])


def _split(
    items: Sequence[np.ndarray | str | Any],
) -> Tuple[List[np.ndarray], List[Union[str, Any]]]:
    imgs, vids = [], []
    for o in items:
        (imgs if isinstance(o, np.ndarray) else vids).append(o)
    return imgs, vids


@router.post("")
async def image_embedding(
    request: Request, # Need request to get form data for proc_ config
    files: List[UploadFile] | None = File(None),
    file: UploadFile | None = File(None),
    path: str | None = Form(None),
    roi: str | None = Form(None),
    model_name: str | None = Form(None),
):
    tic = time.perf_counter()
    try:
        model_cache_instance = request.app.state.model_cache
        
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
        log.debug(f"1******************{raw_items}")
        images_np, videos = _split(raw_items)
        log.debug(f"2******************{images_np, videos}")

        wrapper = await get_wrapper(
            model_cache_instance,
            ModelTaskType.EMBEDDING, model_name)

        all_series_results: List[EmbeddingSeries] = [] # To store final series objects if needed

        # -------------------- VIDEO -----------------------------------------
        if videos:
            loop = asyncio.get_running_loop()
            for idx, v_src in enumerate(videos):
                try:
                    # Pass the image_processor to video processing
                    video_frame_results: List[EmbeddingFrameResult] = await asyncio.to_thread(
                        process_video_sync, v_src, wrapper, model_cache_instance, loop, image_processor
                    )
                    if video_frame_results:
                        total_video_time_ms = sum(r.processing_time_ms for r in video_frame_results if r.processing_time_ms is not None)
                        all_series_results.append(
                            EmbeddingSeries(
                                model_name=wrapper.model_name,
                                total_items=len(video_frame_results),
                                total_processing_time_ms=total_video_time_ms,
                                results=video_frame_results
                            )
                        )
                    _free_mem()
                except Exception as exc:  # noqa: BLE001
                    log.error("Embedding video #%s error: %s", idx, exc, exc_info=True)
                    raise HTTPException(
                        HTTP_500_INTERNAL_SERVER_ERROR,
                        f"Embedding failed on video #{idx}: {exc}",
                    ) from exc

        # -------------------- IMAGES ----------------------------------------
        if images_np:
            log.info(f"Starting image embedding processing for {len(images_np)} images.")
            
            processed_images_np: List[np.ndarray] = []

            # Apply image processing to static images
            if image_processor:
                log.debug("Applying image processing to static images...")
                pil_images = await asyncio.to_thread(lambda imgs: [cv2_to_pil(img) for img in imgs], images_np)
                processed_pil_images = await asyncio.gather(*[
                    asyncio.to_thread(image_processor.process_image, pil_img) for pil_img in pil_images
                ])
                processed_images_np = await asyncio.to_thread(lambda pil_imgs: [pil_to_cv2(pil_img) for pil_img in pil_imgs], processed_pil_images)
                log.debug(f"Finished image processing for {len(processed_images_np)} static images.")
            else:
                log.debug("No image processing applied to static images.")
                processed_images_np = images_np

            # Run detector batch processing on processed images
            if processed_images_np:
                static_image_frame_results: List[EmbeddingFrameResult] = await asyncio.to_thread(
                    wrapper.detect_batch,
                    processed_images_np,
                    timestamps=[0.0] * len(processed_images_np), # Static images have 0 timestamp
                    frame_indices=list(range(len(processed_images_np)))
                )
            
                log.debug(f"After calling detect_batch: static_image_frame_results type: {type(static_image_frame_results)}, value length: {len(static_image_frame_results)}") 
                if static_image_frame_results:
                    total_static_image_time_ms = sum(r.processing_time_ms for r in static_image_frame_results if r.processing_time_ms is not None)
                    all_series_results.append(
                        EmbeddingSeries(
                            model_name=wrapper.model_name,
                            total_items=len(static_image_frame_results),
                            total_processing_time_ms=total_static_image_time_ms,
                            results=static_image_frame_results
                        )
                    )
                log.debug(f"******************{total_static_image_time_ms}")
            else:
                 log.warning("No processed static images to process.")

        _free_mem() # Clean up memory after processing

        if not all_series_results:
            raise HTTPException(
                HTTP_422_UNPROCESSABLE_ENTITY, "No valid images or video frames were processed. EmbeddingSeries"
            )

        # make_response now expects List[Series] or a single Series object
        final_payload_for_response: Union[EmbeddingSeries, List[EmbeddingSeries]]
        if len(all_series_results) == 1:
            final_payload_for_response = all_series_results[0]
        else:
            final_payload_for_response = all_series_results

        return make_response(TaskType.EMBEDDING, wrapper.model_name, final_payload_for_response, tic)

    
    except HTTPException:
        raise
    except Exception as exc:  # noqa: BLE001
        log.error("Unexpected /api/embeddings error: %s", exc, exc_info=True)
        raise HTTPException(HTTP_500_INTERNAL_SERVER_ERROR, "Internal server error") from exc


def _free_mem() -> None:
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()