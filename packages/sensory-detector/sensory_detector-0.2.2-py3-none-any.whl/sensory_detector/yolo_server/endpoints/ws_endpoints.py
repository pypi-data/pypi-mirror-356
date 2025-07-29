# src/sensory_detector/yolo_server/endpoints/ws_endpoints.py
from fastapi import WebSocket, APIRouter, WebSocketDisconnect, Query, Request
import cv2, numpy as np, logging, json
import asyncio
from typing import List, Union, Dict, Any, Optional

from sensory_detector.models.models import (
    ObjectDetectionResult,
    OCRFrameResult,
    EmbeddingFrameResult,
    TaskType,
)
from sensory_detector.yolo_server.detectors.detector_interface import ModelTaskType
from sensory_detector.yolo_server.app.model_utils import get_wrapper

log = logging.getLogger(__name__)

ws_router = APIRouter()

@ws_router.websocket("/ws/analyze")
async def analyze_stream(
    websocket: WebSocket,
    task_type: TaskType = Query(..., description="Тип задачи: 'detection', 'ocr' или 'embedding'."),
    model_name: str | None = Query(None, description="Опционально: имя модели для анализа (например, 'yolov8s', 'tess', 'clip-ViT-B-32-laion2b_s34b_b79k')."),
    details: bool = Query(True, alias="ocr_details", description="Для OCR: Включать детализацию по словам (bbox, уверенность) в ответ. По умолчанию `true`."),
    request: Request = None
):
    await websocket.accept()
    detector = None
    frame_idx = 0

    log.info(f"WebSocket connection accepted. Task: {task_type.value}, Model: {model_name or 'default'}, OCR Details: {details}")

    try:
        model_cache_instance = request.app.state.model_cache

        selected_detector_task_type = ModelTaskType(task_type.value)

        detector = await get_wrapper(
            model_cache_instance,
            task_type=selected_detector_task_type,
            model_name=model_name
        )
        log.info(f"WebSocket using model: '{detector.model_name}' for task: '{detector.task_type().value}'")

        while True:
            data = await websocket.receive_bytes()
            log.debug(f"Received {len(data)} bytes for frame {frame_idx} (Task: {task_type.value})")

            if not data:
                 log.debug("Received empty bytes, client likely disconnecting.")
                 break

            try:
                await model_cache_instance.update_activity(detector.model_name)
                log.debug(f"Activity updated for model '{detector.model_name}' from WS frame {frame_idx}.")
            except Exception as update_e:
                log.warning(f"Failed to send activity update for model '{detector.model_name}' from WS frame {frame_idx}: {update_e}", exc_info=True)

            nparr = np.frombuffer(data, np.uint8)
            frame = await asyncio.to_thread(cv2.imdecode, nparr, cv2.IMREAD_COLOR)

            if frame is None:
                log.warning(f"Failed to decode image data for frame {frame_idx}. Sending error.")
                await websocket.send_json({"frame_index": frame_idx, "error": "Bad image data: Could not decode image."})
                frame_idx += 1
                continue

            timestamp = float(frame_idx / 30.0)
            log.debug(f"Running {task_type.value} for frame {frame_idx} at approx {timestamp:.2f}s")

            extra_kwargs: Dict[str, Any] = {}
            if task_type == TaskType.OCR:
                extra_kwargs["details"] = details

            frame_result: Union[ObjectDetectionResult, OCRFrameResult, EmbeddingFrameResult] = await asyncio.to_thread(
                detector.detect_from_frame, frame, timestamp=timestamp, frame_index=frame_idx, **extra_kwargs
            )

            response_data: Dict[str, Any] = {
                "frame_index": frame_result.frame_index,
                "timestamp": frame_result.timestamp,
                "processing_time_ms": frame_result.processing_time_ms
            }

            if isinstance(frame_result, ObjectDetectionResult):
                response_data["detections"] = [d.model_dump() for d in frame_result.detections]
                log.debug(f"Detection complete for frame {frame_idx}. Found {len(frame_result.detections)} objects.")
            elif isinstance(frame_result, OCRFrameResult):
                response_data["full_text"] = frame_result.full_text
                response_data["mean_confidence"] = frame_result.mean_confidence
                if details and frame_result.words:
                    response_data["words"] = [w.model_dump() for w in frame_result.words]
                else:
                    response_data["words"] = []
                log.debug(f"OCR complete for frame {frame_idx}. Text: '{frame_result.full_text[:50]}...'")
            elif isinstance(frame_result, EmbeddingFrameResult):
                response_data["embedding"] = frame_result.embedding
                log.debug(f"Embedding complete for frame {frame_idx}. Vector length: {len(frame_result.embedding)}.")
            else:
                log.warning(f"Unsupported frame result type received: {type(frame_result).__name__}. Skipping response for frame {frame_idx}.")
                await websocket.send_json({"frame_index": frame_idx, "error": f"Unsupported result type: {type(frame_result).__name__}"})
                frame_idx += 1
                continue

            await websocket.send_json(response_data)
            frame_idx += 1

    except WebSocketDisconnect as e:
        log.info(f"WebSocket client disconnected. Code: {e.code}, Reason: {e.reason}")
    except (ValueError, FileNotFoundError, RuntimeError) as e:
         log.error(f"Error getting/loading model for WS: {e}", exc_info=True)
         await websocket.send_json({"error": f"Server error: {e}"})
         await websocket.close(code=1011)
    except Exception as e:
        log.exception("Unexpected error in WebSocket stream: %s", e)
        await websocket.send_json({"error": "Internal server error"})
        await websocket.close(code=1011)

    finally:
        log.info(f"WebSocket handler finished for model {detector.model_name if detector else 'N/A'}. Total frames: {frame_idx}")