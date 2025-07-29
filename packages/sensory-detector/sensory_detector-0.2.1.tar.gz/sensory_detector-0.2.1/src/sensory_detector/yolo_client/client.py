# Содержимое файла: src/sensory_detector/yolo_client/client.py
from __future__ import annotations
import asyncio
import json
import mimetypes
import logging
import io # Import io for file-like object handling
from pathlib import Path
from typing import Literal, Sequence, Union, Optional, Any, Mapping, overload, List, Tuple # Added missing imports
import httpx

# Import all necessary Pydantic models from the unified location
from sensory_detector.models.models import (
    ModelsResponse,
    CacheStatsResponse,
    UnloadModelResponse,
    EnvelopeResponse,
    DetectionSeries,
    OCRSeries,
    EmbeddingSeries,
    FilesResponse,
    ObjectDetectionResult, # Frame-level result for direct access in client tests
    OCRFrameResult,        # Frame-level result
    EmbeddingFrameResult   # Frame-level result
)

log = logging.getLogger(__name__)

# --- Type Definitions ---
# _InputFile (local client path)
_InputFile = Union[str, Path]
# _InputBytes (raw binary data)
_InputBytes = bytes
# _InFileLike: Represents a single input (path or bytes)
_InFileLike = Union[_InputFile, _InputBytes]
# _InputList: Represents a sequence of inputs (for batch processing)
_InputList = Sequence[_InFileLike]

# FileTuple: (filename, file_like_object_or_bytes, mimetype)
# This is what httpx expects for `files` parameter. For paths, we return an opened file handle.
# Corrected type hint to reflect that file_obj can be bytes or a BufferedReader
FileTuple = tuple[str, Union[bytes, io.BufferedReader], str]

# --- Helper Functions ---
def _guess_mime(name: str) -> str:
    """Guesses the MIME type of a file based on its name."""
    return mimetypes.guess_type(name)[0] or "application/octet-stream"

def _mk_filetuple(src: _InFileLike) -> FileTuple:
    """
    Transforms a path or bytes object into a tuple format accepted by httpx for file uploads.
    For file paths, it returns an an opened file handle (io.BufferedReader) for streaming.
    """
    if isinstance(src, (str, Path)):
        p = Path(src).expanduser().resolve()
        if not p.exists():
            raise FileNotFoundError(f"Input file not found: {p}")
        # Open file in binary read mode. httpx will manage reading/closing if passed as file-like.
        file_obj = p.open('rb')
        log.debug(f"Created file tuple for path '{p}' for streaming upload.")
        return p.name, file_obj, _guess_mime(p.name)

    if isinstance(src, bytes):
        # For bytes, return bytes directly.
        log.debug(f"Created file tuple for bytes data (len={len(src)}).")
        return "buffer.bin", src, "application/octet-stream"

    raise TypeError(f"Unsupported input type: {type(src).__name__} for file tuple creation. Expected str, Path, or bytes.")

async def _prepare_and_send_request(
    self: SensoryAPIClient,
    url: str,
    images: Union[_InFileLike, _InputList],
    model_name: str | None,
    roi_json: str | None,
    extra: dict[str, Any] | None, # Добавляем extra, т.к. recognize_texts его использует
    proc_cfg: Mapping[str, Any] | None,
    path_mode: bool
) -> httpx.Response:
    """
    Helper to encapsulate the logic for handling image input types
    and calling the appropriate _post method (path-based or file upload).
    """
    if path_mode and isinstance(images, (str, Path)):
        log.debug(f"Handling request for URL '{url}' with server path: {images}")
        return await self._post_path(url, str(images), model_name, roi_json, extra, proc_cfg)
    else:
        if isinstance(images, (str, Path, bytes)):
            images_list = [images]
        elif isinstance(images, Sequence):
            images_list = list(images)
        else:
            raise TypeError(f"Unsupported 'images' input type: {type(images)}")
        log.debug(f"Handling request for URL '{url}' with {len(images_list)} file(s) for upload.")
        return await self._post_files(url, images_list, model_name, roi_json, extra, proc_cfg)


class SensoryAPIClient:
    """
    Asynchronous client for interacting with the Sensory Detector API.

    Provides methods for object detection, text recognition (OCR), and embedding generation.
    Supports both file upload and path-based file access on the server.
    """

    def __init__(self, base_url: str = "http://localhost:8000") -> None:
        """
        Initializes the asynchronous API client.

        Args:
            base_url: The base URL of the Sensory Detector API server.
        """
        self._base = base_url.rstrip("/")
        log.info(f"SensoryAPIClient initialized with base URL: {self._base}")

    async def _post_path(
        self,
        url: str,
        srv_path: str,
        model: str | None,
        roi_json: str | None,
        extra: dict[str, Any] | None = None,
        proc_cfg: Mapping[str, Any] | None = None,
    ) -> httpx.Response:
        """Helper to send a POST request with a server-side path."""
        form: dict[str, Any] = {"path": srv_path}
        if model:
            form["model_name"] = model
        if roi_json:
            form["roi"] = roi_json
        if extra:
            form.update(extra)
        if proc_cfg:
            for key, value in proc_cfg.items():
                if isinstance(value, (list, tuple, dict)):
                    try:
                        form[f"proc_{key}"] = json.dumps(value)
                    except TypeError:
                        log.warning(f"Could not JSON serialize processing config value for '{key}', sending as-is: {value}")
                        form[f"proc_{key}"] = value
                else:
                    form[f"proc_{key}"] = str(value) # Ensure all form values are strings for HTTP form data

        log.debug(f"POSTing to {self._base}{url} with path='{srv_path}' and form data: {form}")
        async with httpx.AsyncClient(base_url=self._base, timeout=None) as c:
            return await c.post(url, data=form)

    async def _post_files(
        self,
        url: str,
        files: Sequence[_InFileLike], # Этот параметр уже предполагает, что `files` является последовательностью элементов _InFileLike
        model: str | None,
        roi_json: str | None,
        extra: dict[str, Any] | None = None,
        proc_cfg: Mapping[str, Any] | None = None,
    ) -> httpx.Response:
        """Helper to send a POST request with file uploads."""
        
        httpx_files_param = []
        file_objects_to_close = [] # To keep track of opened file handles for explicit closing

        for f in files: # Loop over `files`
            filename, file_content_or_obj, mimetype = _mk_filetuple(f) # `f` comes from `files`
            # httpx expects tuple in form ('fieldname', ('filename', file_content_or_obj, mimetype))
            httpx_files_param.append(("files", (filename, file_content_or_obj, mimetype)))
            
            # If _mk_filetuple returned an opened file object (not bytes), store it for closing
            if isinstance(file_content_or_obj, io.BufferedReader):
                file_objects_to_close.append(file_content_or_obj)

        data: dict[str, Any] = {}
        if model:
            data["model_name"] = model
        if roi_json:
            data["roi"] = roi_json
        if extra:
            data.update(extra)
        if proc_cfg:
            for key, value in proc_cfg.items():
                if isinstance(value, (list, tuple, dict)):
                    try:
                        data[f"proc_{key}"] = json.dumps(value)
                    except TypeError:
                        log.warning(f"Could not JSON serialize processing config value for '{key}', sending as-is: {value}")
                        data[f"proc_{key}"] = value
                else:
                    data[f"proc_{key}"] = str(value) # Ensure all form values are strings
        
        log.debug(f"POSTing to {self._base}{url} with {len(files)} files and data: {data}")
        async with httpx.AsyncClient(base_url=self._base, timeout=None) as c:
            resp = await c.post(url, files=httpx_files_param, data=data)
            
            # Close the file objects after the request is completed
            for file_obj in file_objects_to_close:
                try:
                    file_obj.close()
                    log.debug(f"Closed file handle for {file_obj.name}.")
                except Exception as e:
                    log.warning(f"Error closing file handle {file_obj.name}: {e}")
            return resp

    @overload
    async def detect_objects(
        self,
        images: _InFileLike,
        model_name: str | None = None,
        roi: Tuple[Tuple[int, int], Tuple[int, int]] | None = None,
        proc_cfg: Mapping[str, Any] | None = None,
        *,
        path_mode: bool = False
    ) -> DetectionSeries: ...

    @overload
    async def detect_objects(
        self,
        images: _InputList,
        model_name: str | None = None,
        roi: Tuple[Tuple[int, int], Tuple[int, int]] | None = None,
        proc_cfg: Mapping[str, Any] | None = None,
        *,
        path_mode: bool = False
    ) -> List[DetectionSeries]: ...

    async def detect_objects(
        self,
        images: Union[_InFileLike, _InputList],
        model_name: str | None = None,
        roi: Tuple[Tuple[int, int], Tuple[int, int]] | None = None,
        proc_cfg: Mapping[str, Any] | None = None,
        *,
        path_mode: bool = False
    ) -> Union[DetectionSeries, List[DetectionSeries]]:
        """
        Detects objects in images or video streams using YOLO models.

        Args:
            images: Source image(s) or video(s). Can be a file path (str, Path),
                    raw bytes, or a list of such. For file uploads, these are local paths.
                    For path_mode=True, this is a path on the server's file system.
            model_name: Optional. The name of the YOLO model to use (e.g., 'yolov8s').
                        If None, the server's default model will be used.
            roi: Optional. Region of Interest as a tuple of two (x,y) tuples
                 defining the top-left and bottom-right corners (e.g., ((0,0),(100,100))).
                 Objects will only be detected within this region.
            proc_cfg: Optional. A dictionary of image preprocessing configurations.
                      Keys should correspond to `OCRImageProcessingConfig` fields (e.g.,
                      `{"enabled": True, "resize_enabled": True, "resize_target_dim": 640}`).
                      These will be prefixed with 'proc_' when sent to the server.
            path_mode: If True, `images` is treated as a path on the server's file system.
                       Requires `FILES_PATH` to be configured on the server.

        Returns:
            DetectionSeries for a single image/video, or List[DetectionSeries] for multiple.

        Raises:
            httpx.HTTPStatusError: If the API call fails (e.g., 4xx or 5xx response).
            FileNotFoundError: If a local file path is provided but the file does not exist.

        Examples:
            >>> client = SensoryAPIClient()
            >>> # Detect objects in an uploaded image (local file)
            >>> result = await client.detect_objects(images="path/to/image.jpg", model_name="yolov8s")
            >>> # Detect objects in a video located on the server
            >>> result = await client.detect_objects(images="/data/videos/my_video.mp4", path_mode=True)
            >>> # Detect objects with preprocessing (e.g., resize)
            >>> result = await client.detect_objects(images="path/to/image.jpg", proc_cfg={"enabled": True, "resize_enabled": True, "resize_target_dim": 800})
            >>> # Example curl for file upload:
            >>> # curl -X POST -F 'file=@test.jpg' -F 'model_name=yolov8s' http://localhost:8000/api/objects
            >>> # Example curl for path-based access:
            >>> # curl -X POST -d 'path=/data/video.mp4' -d 'model_name=yolov8s' http://localhost:8000/api/objects
            >>> # Example curl with preprocessing:
            >>> # curl -X POST -F 'file=@test.jpg' -F 'proc_enabled=true' -F 'proc_resize_enabled=true' -F 'proc_resize_target_dim=500' http://localhost:8000/api/objects
        """
        roi_json = json.dumps([[*roi[0]], [*roi[1]]]) if roi else None
        url = "/api/objects"
        
        resp = await _prepare_and_send_request(self,
            url, images, model_name, roi_json, None, proc_cfg, path_mode # 'extra' здесь None
        )

        resp.raise_for_status()
        # Parse the common EnvelopeResponse wrapper
        payload = EnvelopeResponse(**resp.json()).data
        log.debug(f"Received payload for detect_objects: {payload}")

        if isinstance(payload, list):
            # Server returned a list of series (e.g., video + images, or multiple videos)
            return [DetectionSeries(**item) for item in payload]
        else:
            # Server returned a single series (e.g., single image/video, or batch of images only)
            return DetectionSeries(**payload)

    @overload
    async def recognize_texts(
        self,
        images: _InFileLike,
        model_name: str | None = None,
        roi: Tuple[Tuple[int, int], Tuple[int, int]] | None = None,
        proc_cfg: Mapping[str, Any] | None = None,
        *,
        path_mode: bool = False,
        details: bool = True,
    ) -> OCRSeries: ...

    @overload
    async def recognize_texts(
        self,
        images: _InputList,
        model_name: str | None = None,
        roi: Tuple[Tuple[int, int], Tuple[int, int]] | None = None,
        proc_cfg: Mapping[str, Any] | None = None,
        *,
        path_mode: bool = False,
        details: bool = True,
    ) -> List[OCRSeries]: ...

    async def recognize_texts(
        self,
        images: Union[_InFileLike, _InputList],
        model_name: str | None = None,
        roi: Tuple[Tuple[int, int], Tuple[int, int]] | None = None,
        proc_cfg: Mapping[str, Any] | None = None,
        *,
        path_mode: bool = False,
        details: bool = True,
    ) -> Union[OCRSeries, List[OCRSeries]]:
        """
        Recognizes text in images or video frames using OCR models (EasyOCR or Tesseract).

        Args:
            images: Source image(s) or video(s). Can be a file path (str, Path),
                    raw bytes, or a list of such. For file uploads, these are local paths.
                    For path_mode=True, this is a path on the server's file system.
            model_name: Optional. The name of the OCR model to use (e.g., 'tesseract', 'easyocr-ru_en').
                        If None, the server will use its default OCR model.
            roi: Optional. Region of Interest as a tuple of two (x,y) tuples
                 defining the top-left and bottom-right corners. Text will only be
                 recognized within this region.
            proc_cfg: Optional. A dictionary of image preprocessing configurations.
                      Keys should correspond to `OCRImageProcessingConfig` fields (e.g.,
                      `{"enabled": True, "background_processing_enabled": True}`).
                      These will be prefixed with 'proc_' when sent to the server.
            path_mode: If True, `images` is treated as a path on the server's file system.
                       Requires `FILES_PATH` to be configured on the server.
            details: If True, includes word-level details (bounding boxes, confidence)
                     in the OCR result. Default is True.

        Returns:
            OCRResult for a single image/video, or List[OCRResult] for multiple.

        Raises:
            httpx.HTTPStatusError: If the API call fails.
            FileNotFoundError: If a local file path is provided but the file does not exist.

        Examples:
            >>> client = SensoryAPIClient()
            >>> # Recognize text in an uploaded image with EasyOCR
            >>> result = await client.recognize_texts(images="path/to/doc.png", model_name="easyocr-ru_en")
            >>> # Recognize text in a scanned document on the server using Tesseract, with preprocessing
            >>> result = await client.recognize_texts(
            >>>     images="/data/scanned.tiff", path_mode=True, model_name="tesseract",
            >>>     proc_cfg={"enabled": True, "borders_enabled": True, "border_size": 20, "border_color": [0,0,0]}
            >>> )
            >>> # Recognize text from a video, getting only full text without word details
            >>> result = await client.recognize_texts(images="/data/screen_rec.mp4", path_mode=True, details=False)
            >>> # Example curl for file upload:
            >>> # curl -X POST -F 'file=@doc.png' -F 'model_name=easyocr-ru_en' http://localhost:8000/api/texts
            >>> # Example curl for path-based access with preprocessing:
            >>> # curl -X POST -d 'path=/data/scanned.tiff' -d 'model_name=tesseract' -d 'proc_enabled=true' -d 'proc_borders_enabled=true' -d 'proc_border_size=20' -d 'proc_border_color=[0,0,0]' http://localhost:8000/api/texts
        """
        roi_json = json.dumps([[*roi[0]], [*roi[1]]]) if roi else None
        # Ensure 'details' is converted to string for form data.
        extra = {"details": str(details).lower()} 

        url = "/api/texts"

        
        resp = await _prepare_and_send_request(self,
            url, images, model_name, roi_json, None, proc_cfg, path_mode # 'extra' здесь None
        )
        resp.raise_for_status()
        payload = EnvelopeResponse(**resp.json()).data
        log.debug(f"Received payload for recognize_texts: {payload}")

        if isinstance(payload, list):
            return [OCRSeries(**p) for p in payload]
        else:
            return OCRSeries(**payload) # For single result (e.g. single image)

    @overload
    async def get_embeddings(
        self,
        images: _InFileLike,
        model_name: str | None = None,
        roi: Tuple[Tuple[int, int], Tuple[int, int]] | None = None,
        proc_cfg: Mapping[str, Any] | None = None,
        *,
        path_mode: bool = False
    ) -> EmbeddingSeries: ...

    @overload
    async def get_embeddings(
        self,
        images: _InputList,
        model_name: str | None = None,
        roi: Tuple[Tuple[int, int], Tuple[int, int]] | None = None,
        proc_cfg: Mapping[str, Any] | None = None,
        *,
        path_mode: bool = False
    ) -> List[EmbeddingSeries]: ...

    async def get_embeddings(
        self,
        images: Union[_InFileLike, _InputList],
        model_name: str | None = None,
        roi: Tuple[Tuple[int, int], Tuple[int, int]] | None = None,
        proc_cfg: Mapping[str, Any] | None = None,
        *,
        path_mode: bool = False
    ) -> Union[EmbeddingSeries, List[EmbeddingSeries]]:
        """
        Generates embedding vectors for images or video frames using CLIP models.

        Args:
            images: Source image(s) or video(s). Can be a file path (str, Path),
                    raw bytes, or a list of such. For file uploads, these are local paths.
                    For path_mode=True, this is a path on the server's file system.
            model_name: Optional. The name of the CLIP model to use (e.g., 'clip-ViT-B-32-laion2b_s34b_b79k').
                        If None, the server will use its default embedding model.
            roi: Optional. Region of Interest as a tuple of two (x,y) tuples
                 defining the top-left and bottom-right corners. Embeddings will be
                 generated only from this region.
            proc_cfg: Optional. A dictionary of image preprocessing configurations.
                      Keys should correspond to `OCRImageProcessingConfig` fields (e.g.,
                      `{"enabled": True, "resize_enabled": True, "resize_target_dim": 224}`).
                      These will be prefixed with 'proc_' when sent to the server.
            path_mode: If True, `images` is treated as a path on the server's file system.
                       Requires `FILES_PATH` to be configured on the server.

        Returns:
            EmbeddingResponse for a single image/video, or List[EmbeddingResponse] for multiple.

        Raises:
            httpx.HTTPStatusError: If the API call fails.
            FileNotFoundError: If a local file path is provided but the file does not exist.

        Examples:
            >>> client = SensoryAPIClient()
            >>> # Get embedding for an uploaded image (local file)
            >>> result = await client.get_embeddings(images="path/to/item.png", model_name="clip-ViT-B-32-laion2b_s34b_b79k")
            >>> # Get embeddings for a video on the server, with preprocessing to resize frames
            >>> result = await client.get_embeddings(
            >>>     images="/data/product_video.mp4", path_mode=True,
            >>>     proc_cfg={"enabled": True, "resize_enabled": True, "resize_target_dim": 224}
            >>> )
            >>> # Example curl for file upload:
            >>> # curl -X POST -F 'file=@item.png' -F 'model_name=clip-ViT-B-32-laion2b_s34b_b79k' http://localhost:8000/api/embeddings
            >>> # Example curl for path-based access with preprocessing:
            >>> # curl -X POST -d 'path=/data/product_video.mp4' -d 'proc_enabled=true' -d 'proc_resize_enabled=true' -d 'proc_resize_target_dim=224' http://localhost:8000/api/embeddings
        """
        roi_json = json.dumps([[*roi[0]], [*roi[1]]]) if roi else None
        url = "/api/embeddings"

        
        resp = await _prepare_and_send_request(self,
            url, images, model_name, roi_json, None, proc_cfg, path_mode # 'extra' здесь None
        )
        resp.raise_for_status()
        payload = EnvelopeResponse(**resp.json()).data
        log.debug(f"Received payload for get_embeddings: {payload}")

        if isinstance(payload, list):
            return [EmbeddingSeries(**item.model_dump()) for item in payload if isinstance(item, EmbeddingSeries)]
        else:
            return EmbeddingSeries(**payload.model_dump())


    async def get_available_models(self) -> ModelsResponse:
        """
        Retrieves a list of all models available on the server, categorized by task type.

        Returns:
            A ModelsResponse object containing available models and default model information.

        Raises:
            httpx.HTTPStatusError: If the API call fails.

        Examples:
            >>> client = SensoryAPIClient()
            >>> response = await client.get_available_models()
            >>> print(response.model_dump_json(indent=2))
            # curl -X GET http://localhost:8000/api/available_models
        """
        log.info("Requesting available models...")
        async with httpx.AsyncClient(base_url=self._base) as client:
            r = await client.get("/api/available_models")
            r.raise_for_status()
            return ModelsResponse(**r.json())

    async def get_loaded_models(self) -> List[CacheStatsResponse]:
        """
        Retrieves statistics for models currently loaded in the server's cache.

        Returns:
            A list of CacheStatsResponse objects, each detailing a loaded model.

        Raises:
            httpx.HTTPStatusError: If the API call fails.

        Examples:
            >>> client = SensoryAPIClient()
            >>> loaded_models = await client.get_loaded_models()
            >>> for model in loaded_models:
            >>>     print(f"Model: {model.model_name}, Task: {model.task_type}, Idle: {model.idle_seconds}s")
            # curl -X GET http://localhost:8000/api/loaded_models
        """
        log.info("Requesting loaded models statistics...")
        async with httpx.AsyncClient(base_url=self._base) as client:
            r = await client.get("/api/loaded_models")
            r.raise_for_status()
            return [CacheStatsResponse(**item) for item in r.json()]

    async def unload_model(self, model_name: str) -> UnloadModelResponse:
        """
        Requests the server to forcibly unload a specific model from its cache.

        Args:
            model_name: The name of the model to unload.

        Returns:
            An UnloadModelResponse object confirming the unload operation.

        Raises:
            httpx.HTTPStatusError: If the API call fails (e.g., model not found, 404).

        Examples:
            >>> client = SensoryAPIClient()
            >>> response = await client.unload_model("yolov8s")
            >>> print(response.detail)
            # curl -X DELETE http://localhost:8000/api/unload_model/yolov8s
        """
        log.info(f"Requesting to unload model: {model_name}...")
        async with httpx.AsyncClient(base_url=self._base) as client:
            r = await client.delete(f"/api/unload_model/{model_name}")
            r.raise_for_status()
            return UnloadModelResponse(**r.json())

    async def get_available_files(self) -> FilesResponse:
        """
        Retrieves a list of files available on the server for path-based access.
        These files are located in the server's configured FILES_PATH.

        Returns:
            A FilesResponse object containing the list of available files and the base path.

        Raises:
            httpx.HTTPStatusError: If the API call fails (e.g., 4xx or 5xx response).
            HTTPException: If the server reports an error (e.g., FILES_PATH not configured).

        Examples:
            >>> client = SensoryAPIClient()
            >>> response = await client.get_available_files()
            >>> print(f"Available files (relative to {response.base_path}):")
            >>> for file_name in response.files:
            >>>     print(f"- {file_name}")
            # Example curl:
            # curl -X GET http://localhost:8000/api/files
        """
        log.info("Requesting available files from server...")
        async with httpx.AsyncClient(base_url=self._base) as client:
            r = await client.get("/api/files")
            r.raise_for_status() # Raise an exception for 4xx/5xx responses
            return FilesResponse(**r.json())
    
    def sync(self) -> "SensoryAPIClientSync":
        """Returns a synchronous version of this API client."""
        return SensoryAPIClientSync(self._base)




def _prepare_and_send_request_sync(
        self: SensoryAPIClientSync,
        client: httpx.Client, # Здесь нужен httpx.Client, который создается в каждом публичном методе
        url: str,
        images: Union[_InFileLike, _InputList],
        model_name: str | None,
        roi_json: str | None,
        extra: dict[str, Any] | None,
        proc_cfg: Mapping[str, Any] | None,
        path_mode: bool
    ) -> httpx.Response:
        """
        Helper to encapsulate the logic for handling image input types
        and calling the appropriate _post_sync method (path-based or file upload).
        """
        if path_mode and isinstance(images, (str, Path)):
            log.debug(f"Handling sync request for URL '{url}' with server path: {images}")
            return self._post_path_sync(client, url, str(images), model_name, roi_json, extra, proc_cfg)
        else:
            if isinstance(images, (str, Path, bytes)):
                images_list = [images]
            elif isinstance(images, Sequence):
                images_list = list(images)
            else:
                raise TypeError(f"Unsupported 'images' input type: {type(images)}")
            log.debug(f"Handling sync request for URL '{url}' with {len(images_list)} file(s) for upload.")
            return self._post_files_sync(client, url, images_list, model_name, roi_json, extra, proc_cfg)


class SensoryAPIClientSync:
    """
    Synchronous client for interacting with the Sensory Detector API.
    All methods are blocking.
    """

    def __init__(self, base_url: str = "http://localhost:8000") -> None:
        """
        Initializes the synchronous API client.

        Args:
            base_url: The base URL of the Sensory Detector API server.
        """
        self._base = base_url.rstrip("/")
        log.info(f"SensoryAPIClientSync initialized with base URL: {self._base}")

    def _post_path_sync(
        self,
        client: httpx.Client,
        url: str,
        srv_path: str,
        model: str | None,
        roi_json: str | None,
        extra: dict[str, Any] | None = None,
        proc_cfg: Mapping[str, Any] | None = None,
    ) -> httpx.Response:
        """Helper to send a synchronous POST request with a server-side path."""
        form: dict[str, Any] = {"path": srv_path}
        if model:
            form["model_name"] = model
        if roi_json:
            form["roi"] = roi_json
        if extra:
            form.update(extra)
        if proc_cfg:
            for key, value in proc_cfg.items():
                if isinstance(value, (list, tuple, dict)):
                    try:
                        form[f"proc_{key}"] = json.dumps(value)
                    except TypeError:
                        log.warning(f"Could not JSON serialize processing config value for '{key}', sending as-is: {value}")
                        form[f"proc_{key}"] = value
                else:
                    form[f"proc_{key}"] = str(value)
        log.debug(f"SYNC POSTing to {self._base}{url} with path='{srv_path}' and form data: {form}")
        return client.post(url, data=form)

    def _post_files_sync(
        self,
        client: httpx.Client,
        url: str,
        files: Sequence[_InFileLike],
        model: str | None,
        roi_json: str | None,
        extra: dict[str, Any] | None = None,
        proc_cfg: Mapping[str, Any] | None = None,
    ) -> httpx.Response:
        """Helper to send a synchronous POST request with file uploads."""
        
        httpx_files_param = []
        file_objects_to_close = [] # To keep track of opened file handles for explicit closing

        for f in files:
            filename, file_content_or_obj, mimetype = _mk_filetuple(f)
            # httpx expects tuple in form ('fieldname', ('filename', file_content_or_obj, mimetype))
            httpx_files_param.append(("files", (filename, file_content_or_obj, mimetype)))
            
            # If _mk_filetuple returned an opened file object (not bytes), store it for closing
            if isinstance(file_content_or_obj, io.BufferedReader):
                file_objects_to_close.append(file_content_or_obj)

        data: dict[str, Any] = {}
        if model:
            data["model_name"] = model
        if roi_json:
            data["roi"] = roi_json
        if extra:
            data.update(extra)
        if proc_cfg:
            for key, value in proc_cfg.items():
                if isinstance(value, (list, tuple, dict)):
                    try:
                        data[f"proc_{key}"] = json.dumps(value)
                    except TypeError:
                        log.warning(f"Could not JSON serialize processing config value for '{key}', sending as-is: {value}")
                        data[f"proc_{key}"] = value
                else:
                    data[f"proc_{key}"] = str(value)

        log.debug(f"SYNC POSTing to {self._base}{url} with {len(files)} files and data: {data}")
        resp = client.post(url, files=httpx_files_param, data=data)
        
        # Close the file objects after the request is completed
        for file_obj in file_objects_to_close:
            try:
                file_obj.close()
                log.debug(f"Closed file handle for {file_obj.name}.")
            except Exception as e:
                log.warning(f"Error closing file handle {file_obj.name}: {e}")
        return resp

    @overload
    def detect_objects(
        self,
        images: _InFileLike,
        model_name: str | None = None,
        roi: Tuple[Tuple[int, int], Tuple[int, int]] | None = None,
        proc_cfg: Mapping[str, Any] | None = None,
        *,
        path_mode: bool = False
    ) -> DetectionSeries: ...

    @overload
    def detect_objects(
        self,
        images: _InputList,
        model_name: str | None = None,
        roi: Tuple[Tuple[int, int], Tuple[int, int]] | None = None,
        proc_cfg: Mapping[str, Any] | None = None,
        *,
        path_mode: bool = False
    ) -> List[DetectionSeries]: ...

    def detect_objects(
        self,
        images: Union[_InFileLike, _InputList],
        model_name: str | None = None,
        roi: Tuple[Tuple[int, int], Tuple[int, int]] | None = None,
        proc_cfg: Mapping[str, Any] | None = None,
        *,
        path_mode: bool = False
    ) -> Union[DetectionSeries, List[DetectionSeries]]:
        """
        Synchronously detects objects in images or video streams using YOLO models.
        (See async `detect_objects` for detailed parameter descriptions and examples).
        """
        roi_json = json.dumps([[*roi[0]], [*roi[1]]]) if roi else None
        url = "/api/objects"

        with httpx.Client(base_url=self._base, timeout=None) as client:
            r: httpx.Response = _prepare_and_send_request_sync(self,
                client, url, images, model_name, roi_json, None, proc_cfg, path_mode # 'extra' здесь None
            )
            r.raise_for_status()
            payload = EnvelopeResponse(**r.json()).data
            log.debug(f"Received payload for sync detect_objects: {payload}")


            if isinstance(payload, list):
                return [DetectionSeries(**item.model_dump()) for item in payload]
            else:
                return DetectionSeries(**payload.model_dump())

    @overload
    def recognize_texts(
        self,
        images: _InFileLike,
        model_name: str | None = None,
        roi: Tuple[Tuple[int, int], Tuple[int, int]] | None = None,
        proc_cfg: Mapping[str, Any] | None = None,
        *,
        path_mode: bool = False,
        details: bool = True,
    ) -> OCRSeries: ...

    @overload
    def recognize_texts(
        self,
        images: _InputList,
        model_name: str | None = None,
        roi: Tuple[Tuple[int, int], Tuple[int, int]] | None = None,
        proc_cfg: Mapping[str, Any] | None = None,
        *,
        path_mode: bool = False,
        details: bool = True,
    ) -> List[OCRSeries]: ...

    def recognize_texts(
        self,
        images: Union[_InFileLike, _InputList],
        model_name: str | None = None,
        roi: Tuple[Tuple[int, int], Tuple[int, int]] | None = None,
        proc_cfg: Mapping[str, Any] | None = None,
        *,
        path_mode: bool = False,
        details: bool = True,
    ) -> Union[OCRSeries, List[OCRSeries]]:
        """
        Synchronously recognizes text in images or video frames using OCR models.
        (See async `recognize_texts` for detailed parameter descriptions and examples).
        """
        roi_json = json.dumps([[*roi[0]], [*roi[1]]]) if roi else None
        extra = {"details": str(details).lower()} # Ensure 'details' is converted to string for form data.
        url = "/api/texts"

        with httpx.Client(base_url=self._base, timeout=None) as client:
            
            r: httpx.Response = _prepare_and_send_request_sync(self,
                client, url, images, model_name, roi_json, None, proc_cfg, path_mode # 'extra' здесь None
            )
            r.raise_for_status()
            payload = EnvelopeResponse(**r.json()).data
            log.debug(f"Received payload for sync recognize_texts: {payload}")

            if isinstance(payload, list):
                return [OCRSeries(**item.model_dump()) for item in payload]
            else:
                return OCRSeries(**payload.model_dump())

    @overload
    def get_embeddings(
        self,
        images: _InFileLike,
        model_name: str | None = None,
        roi: Tuple[Tuple[int, int], Tuple[int, int]] | None = None,
        proc_cfg: Mapping[str, Any] | None = None,
        *,
        path_mode: bool = False
    ) -> EmbeddingSeries: ...

    @overload
    def get_embeddings(
        self,
        images: _InputList,
        model_name: str | None = None,
        roi: Tuple[Tuple[int, int], Tuple[int, int]] | None = None,
        proc_cfg: Mapping[str, Any] | None = None,
        *,
        path_mode: bool = False
    ) -> List[EmbeddingSeries]: ...

    def get_embeddings(
        self,
        images: Union[_InFileLike, _InputList],
        model_name: str | None = None,
        roi: Tuple[Tuple[int, int], Tuple[int, int]] | None = None,
        proc_cfg: Mapping[str, Any] | None = None,
        *,
        path_mode: bool = False
    ) -> Union[EmbeddingSeries, List[EmbeddingSeries]]:
        """
        Synchronously generates embedding vectors for images or video frames using CLIP models.
        (See async `get_embeddings` for detailed parameter descriptions and examples).
        """
        roi_json = json.dumps([[*roi[0]], [*roi[1]]]) if roi else None
        url = "/api/embeddings"

        with httpx.Client(base_url=self._base, timeout=None) as client:
            
            r: httpx.Response = _prepare_and_send_request_sync(self,
                client, url, images, model_name, roi_json, None, proc_cfg, path_mode # 'extra' здесь None
            )
            r.raise_for_status()
            payload = EnvelopeResponse(**r.json()).data
            log.debug(f"Received payload for sync get_embeddings: {payload}")

            arr = payload if isinstance(payload, list) else [payload]
            return [EmbeddingSeries(**d.model_dump()) for d in arr]

    def get_available_models(self) -> ModelsResponse:
        """
        Synchronously retrieves a list of all models available on the server, categorized by task type.
        (See async `get_available_models` for detailed parameter descriptions).
        """
        log.info("Requesting available models (sync)...")
        with httpx.Client(base_url=self._base) as c:
            r = c.get("/api/available_models")
            r.raise_for_status()
            return ModelsResponse(**r.json())

    def get_loaded_models(self) -> List[CacheStatsResponse]:
        """
        Synchronously retrieves statistics for models currently loaded in the server's cache.
        (See async `get_loaded_models` for detailed parameter descriptions).
        """
        log.info("Requesting loaded models statistics (sync)...")
        with httpx.Client(base_url=self._base) as c:
            r = c.get("/api/loaded_models")
            r.raise_for_status()
            return [CacheStatsResponse(**item) for item in r.json()]

    def unload_model(self, model_name: str) -> UnloadModelResponse:
        """
        Synchronously requests the server to forcibly unload a specific model from its cache.
        (See async `unload_model` for detailed parameter descriptions).
        """
        log.info(f"Requesting to unload model (sync): {model_name}...")
        with httpx.Client(base_url=self._base) as c:
            r = c.delete(f"/api/unload_model/{model_name}")
            r.raise_for_status()
            return UnloadModelResponse(**r.json())
        
    def get_available_files(self) -> FilesResponse:
        """
        Synchronously retrieves a list of files available on the server for path-based access.
        (See async `get_available_files` for detailed parameter descriptions).
        """
        log.info("Requesting available files from server (sync)...")
        with httpx.Client(base_url=self._base) as c:
            r = c.get("/api/files")
            r.raise_for_status()
            return FilesResponse(**r.json())