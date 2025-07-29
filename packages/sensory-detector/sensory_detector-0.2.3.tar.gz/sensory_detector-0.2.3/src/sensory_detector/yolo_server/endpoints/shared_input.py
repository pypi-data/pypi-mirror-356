# Содержимое файла: src/sensory_detector/yolo_server/endpoints/shared_input.py
from __future__ import annotations
import asyncio
import base64
import io
import json
import logging
import mimetypes
from pathlib import Path
from typing import Any, List, Optional, Tuple, Dict
import av
import cv2
import numpy as np
from fastapi import File, Form, HTTPException, UploadFile
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN, HTTP_422_UNPROCESSABLE_ENTITY, HTTP_500_INTERNAL_SERVER_ERROR # Corrected imports for HTTP status codes
from starlette.datastructures import FormData

from sensory_detector.yolo_server.app.appconfig import config # Corrected import for main config
from sensory_detector.yolo_server.app.config import OCRImageProcessingConfig
from PIL import Image # Import PIL for conversions


log = logging.getLogger(__name__)

# --- Image Format Conversion Helpers ---
def cv2_to_pil(frame: np.ndarray) -> Image.Image:
    """Converts a CV2 (NumPy BGR) image to a PIL (RGB) image."""
    if frame is None or frame.size == 0:
         # Handle empty frames gracefully
         log.warning("Attempted to convert empty numpy array to PIL.")
         # Return a small dummy image or raise an error depending on desired behavior
         # Returning a small dummy image might prevent downstream errors
         return Image.new('RGB', (1, 1))
    if frame.ndim == 2: # Grayscale
         img = Image.fromarray(frame, 'L').convert('RGB')
    else: # Assume BGR
         img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    return img

def pil_to_cv2(image: Image.Image) -> np.ndarray:
    """Converts a PIL (RGB) image to a CV2 (NumPy BGR) image."""
    if image.mode != 'RGB':
         image = image.convert('RGB')
    numpy_image = np.array(image)
    opencv_image = cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)
    return opencv_image

# --- Config Parsing Utility ---
def parse_processing_config(form: FormData) -> Optional[OCRImageProcessingConfig]:
    """
    Extracts and validates image processing configuration from form data.
    Looks for keys starting with 'proc_'.
    """
    proc_kwargs: Dict[str, Any] = {}
    for key, value in form.items():
        if key.startswith("proc_"):
            config_key = key.removeprefix("proc_")
            # FastAPI form data might pass values as strings,
            # Pydantic can handle basic type casting (e.g., "true" -> True)
            # but for complex types like lists/tuples, need explicit parsing if expected.
            # For now, rely on Pydantic's default type casting.
            # For tuples like border_color=(r,g,b), clients might need to send as JSON string: proc_border_color="[255, 0, 0]"
            # Let's assume simple types or Pydantic-castable strings for now.
            # If a value is a string that looks like JSON, try parsing it.
            if isinstance(value, str):
                 try:
                      # Attempt JSON parse for lists/tuples/dicts
                      parsed_value = json.loads(value)
                      # If parsing succeeds, use the parsed value, otherwise keep original string
                      value = parsed_value
                 except (json.JSONDecodeError, TypeError):
                      pass # Not JSON or not parsable, keep as string


            proc_kwargs[config_key] = value

    if not proc_kwargs:
        log.debug("No 'proc_' parameters found in form data.")
        return None

    log.debug(f"Found 'proc_' parameters: {proc_kwargs}")

    try:
        # Validate and create config instance
        config_instance = OCRImageProcessingConfig.model_validate(proc_kwargs)
        log.debug(f"Successfully parsed image processing config: {config_instance.model_dump_json()}")
        # Only return if processing is enabled, otherwise None
        if config_instance.enabled:
             return config_instance
        else:
             log.info("Image processing config provided but disabled (enabled=False).")
             return None

    except Exception as e:
        log.error(f"Failed to parse/validate image processing config: {e}", exc_info=True)
        raise HTTPException(
            HTTP_422_UNPROCESSABLE_ENTITY, f"Bad preprocessing config format: {e}"
        ) from e



# ------------------------------------------------------------------ #
#                               ROI                                  #
# ------------------------------------------------------------------ #
def parse_roi(raw: str | None) -> Optional[Tuple[int, int, int, int]]:
    if not raw:
        return None
    try:
        (x1, y1), (x2, y2) = json.loads(raw)  # type: ignore[misc]
        x1, y1, x2, y2 = map(int, (x1, y1, x2, y2))
        if x2 <= x1 or y2 <= y1:
            raise ValueError("invalid bbox")
        return x1, y1, x2, y2
    except Exception as e:  # noqa: BLE001
        raise HTTPException(HTTP_400_BAD_REQUEST, f"Incorrect ROI format: {e}") from e


def crop_roi(img: np.ndarray, roi: Tuple[int, int, int, int]) -> np.ndarray:
    x1, y1, x2, y2 = roi
    h, w = img.shape[:2]
    x1, y1 = max(0, x1), max(0, y1)
    x2, y2 = min(w, x2), min(h, y2)
    if x2 <= x1 or y2 <= y1:
        return np.empty((0, 0, img.shape[2]), dtype=img.dtype)
    return img[y1:y2, x1:x2]


# ------------------------------------------------------------------ #
#                       path-based security                           #
# ------------------------------------------------------------------ #
def safe_resolve_path(path_str: str) -> Path:
    if config.FILES_PATH is None:
        raise HTTPException(
            HTTP_403_FORBIDDEN, "Path-based access disabled – FILES_PATH not set"
        )

    p = Path(path_str)
    p = (config.FILES_PATH / p).resolve() if not p.is_absolute() else p.resolve()

    if not str(p).startswith(str(config.FILES_PATH)):
        raise HTTPException(
            HTTP_403_FORBIDDEN,
            f"Access to '{path_str}' denied – outside {config.FILES_PATH}",
        )
    if not p.exists():
        raise HTTPException(404, f"File '{p}' not found")
    if not p.is_file():
        raise HTTPException(HTTP_400_BAD_REQUEST, f"Path '{p}' is not a file")
    return p


# ------------------------------------------------------------------ #
#                       bytes → numpy helpers                         #
# ------------------------------------------------------------------ #
def _bytes_to_ndarray(b: bytes) -> np.ndarray | None:
    arr = np.frombuffer(b, np.uint8)
    return cv2.imdecode(arr, cv2.IMREAD_COLOR)  # may return None


async def read_upload_file(upload: UploadFile) -> bytes:
    if upload.file.closed:
        raise HTTPException(
            HTTP_400_BAD_REQUEST, f"Uploaded file '{upload.filename or ''}' is closed"
        )
    try:
        return await upload.read()
    except Exception as e:  # noqa: BLE001
        raise HTTPException(HTTP_500_INTERNAL_SERVER_ERROR, f"Upload read error: {e}") from e


async def file_bytes_from_path(p: Path) -> bytes:
    try:
        return await asyncio.to_thread(p.read_bytes)
    except Exception as e:  # noqa: BLE001
        raise HTTPException(HTTP_500_INTERNAL_SERVER_ERROR, f"Read '{p}' failed: {e}") from e


# ------------------------------------------------------------------ #
#                MAIN – unify  path / upload / batch                 #
# ------------------------------------------------------------------ #
async def load_frames(  # noqa: C901  pylint: disable=too-complex,too-many-branches
    files: List[UploadFile] | None = File(None),
    file: UploadFile | None = File(None),
    path: str | None = Form(None),
    roi: str | None = Form(None),
) -> Tuple[List[np.ndarray | str | io.BufferedIOBase], bool]:
    """
    Возвращает:
        items:
            изображения → np.ndarray
            видео       → str (path) | file-like (UploadFile.file)
        is_video_detected:
            True,  если ХОТЯ БЫ один элемент — видео
    """
    roi_t = parse_roi(roi)

    sources = [bool(files), bool(file), bool(path)]
    if sum(sources) == 0:
        raise HTTPException(
            HTTP_422_UNPROCESSABLE_ENTITY,
            "Provide 'files[]', single 'file' or 'path'.",
        )
    if sum(sources) > 1:
        raise HTTPException(
            HTTP_422_UNPROCESSABLE_ENTITY,
            "Provide only ONE source: 'files[]' OR 'file' OR 'path'.",
        )

    processed: list[np.ndarray | str | io.BufferedIOBase] = []
    video_found = False

    # helper-func ---------------------------------------------------- #
    async def _handle_unknown_upload(
        upl: UploadFile, data: bytes | None = None
    ) -> None:
        """
        Для файлов с MIME, отличным от image/* или video/*:
            • пробуем открыть через PyAV → видео
            • иначе  decode через OpenCV → изображение
        """
        nonlocal video_found

        # 1️⃣  видео-проверка ---------------------------------------- #
        try:
            await asyncio.to_thread(av.open, upl.file)
            video_found = True
            processed.append(upl.file)
            log.debug("Treating '%s' as VIDEO by AV probe", upl.filename)
            return
        except (ValueError):
            log.debug("Treating '%s' as VIDEO by AV probe", upl.filename)
            pass
        except Exception as e:
            log.debug(f"Exception _handle_unknown_upload {e}")
        finally:
            upl.file.seek(0)

        # 2️⃣  изображение-проверка ---------------------------------- #
        if data is None:
            data = await read_upload_file(upl)
        img = await asyncio.to_thread(_bytes_to_ndarray, data)
        if img is not None:
            if roi_t:
                img = crop_roi(img, roi_t)
            processed.append(img)
            log.debug("Treating '%s' as IMAGE by OpenCV probe", upl.filename)
            return

        raise HTTPException(
            HTTP_400_BAD_REQUEST,
            f"Unsupported MIME type '{upl.content_type}' for '{upl.filename or ''}'",
        )

    # ------------------------- batch upload ------------------------ #
    if files:
        for upl in files:
            mime = upl.content_type or mimetypes.guess_type(upl.filename or "")[0]

            # VIDEO --------------------------------------------------- #
            if mime and mime.startswith("video/"):
                video_found = True
                processed.append(upl.file)
                continue

            # IMAGE --------------------------------------------------- #
            if mime and mime.startswith("image/"):
                data = await read_upload_file(upl)
                img = await asyncio.to_thread(_bytes_to_ndarray, data)
                if img is None:
                    raise HTTPException(
                        HTTP_400_BAD_REQUEST,
                        f"Cannot decode image '{upl.filename or ''}'",
                    )
                if roi_t:
                    img = crop_roi(img, roi_t)
                processed.append(img)
                continue

            # UNKNOWN  ------------------------------------------------ #
            await _handle_unknown_upload(upl)

        return processed, video_found

    # ------------------------ single upload ------------------------ #
    if file:
        mime = file.content_type or mimetypes.guess_type(file.filename or "")[0]

        if mime and mime.startswith("video/"):
            return [file.file], True

        if mime and mime.startswith("image/"):
            data = await read_upload_file(file)
            img = await asyncio.to_thread(_bytes_to_ndarray, data)
            if img is None:
                raise HTTPException(HTTP_400_BAD_REQUEST, "Cannot decode image")
            if roi_t:
                img = crop_roi(img, roi_t)
            return [img], False

        # UNKNOWN
        await _handle_unknown_upload(file)
        return processed, video_found  # type: ignore[return-value]

    # ----------------------------- path ---------------------------- #
    if path:
        p = safe_resolve_path(path)
        mime = mimetypes.guess_type(p)[0]

        # VIDEO
        if mime and mime.startswith("video/"):
            return [str(p)], True

        # IMAGE
        if mime and mime.startswith("image/"):
            img_bytes = await file_bytes_from_path(p)
            img = await asyncio.to_thread(_bytes_to_ndarray, img_bytes)
            if img is None:
                raise HTTPException(
                    HTTP_400_BAD_REQUEST, f"Cannot decode image at '{path}'"
                )
            if roi_t:
                img = crop_roi(img, roi_t)
            return [img], False

        # UNKNOWN — пробуем AV / OpenCV
        try:
            await asyncio.to_thread(av.open, str(p))
            return [str(p)], True
        except Exception as e:
            log.debug(f"Exception _handle_unknown_upload {e}")
        #except av.AVError:
        #    pass

        img_bytes = await file_bytes_from_path(p)
        img = await asyncio.to_thread(_bytes_to_ndarray, img_bytes)
        if img is not None:
            if roi_t:
                img = crop_roi(img, roi_t)
            return [img], False

        raise HTTPException(
            HTTP_400_BAD_REQUEST, f"Unsupported file type for '{p}' (mime='{mime}')"
        )

    # ─ недостижимо благодаря валидации в начале ─
    raise RuntimeError("load_frames — unreachable state")