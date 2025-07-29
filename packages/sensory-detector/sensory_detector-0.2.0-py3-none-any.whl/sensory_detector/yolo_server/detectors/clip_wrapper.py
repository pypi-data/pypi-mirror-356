# src/sensory_detector/yolo_server/detectors/clip_wrapper.py
import numpy as np
from PIL import Image
import open_clip
import time
import torch
import torch.nn as nn # <-- Добавляем этот импорт
import cv2
import gc, os
import logging
from typing import List, Tuple, Any, Optional # Add Dict, Any

from sensory_detector.yolo_server.detectors.detector_interface import Detector, ModelTaskType
from sensory_detector.yolo_server.app.config import config # Corrected import for main app config
from sensory_detector.models.models import EmbeddingFrameResult # Импортируем новую модель

log = logging.getLogger(__name__)

class CLIPWrapper(Detector):
    _infer_lock = None # CLIP doesn't typically need a lock like EasyOCR/Tesseract

    def __init__(self,
                 model_name: str, # Name used for caching and API (e.g., 'clip')
                 openclip_model_name: str = 'ViT-B-32', # Specific OpenCLIP model architecture name
                 openclip_pretrained: str = 'laion2b_s34b_b79k', # Specific OpenCLIP pretrained weights name
                 device: str | None = None, # Optional device override ('cpu', 'cuda')
                 **kwargs # Accept any other init_kwargs for compatibility
                ):
        """
        Initializes the CLIP wrapper with optional DataParallel support.

        Args:
            model_name: The name used for caching and API (e.g., 'clip').
            openclip_model_name: The specific model name for open_clip.create_model_and_transforms.
            openclip_pretrained: The specific pretrained weights name for open_clip.create_transforms.
            device: Optional device override. Defaults to 'cuda' if available, otherwise 'cpu'.
            gpu_ids: List of GPU IDs to use for DataParallel. If None, uses all available GPUs.
            **kwargs: Additional keyword arguments (ignored).
        """
        self._model_name = model_name
        self._openclip_model_name = openclip_model_name
        self._openclip_pretrained = openclip_pretrained

        # Determine device - base model should be on 'cuda:0' for DataParallel
        if device:
            self.device = device
        else:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"

        # If DataParallel is requested and available, adjust the base device
        # DataParallel expects the main model to be on the first device or cuda:0
        if self.device.startswith('cuda') and torch.cuda.device_count() >= 1:
             # Use cuda:0 as the base device for DataParallel unless specific IDs are given and include 0
            
            base_device_id = int(os.environ.get("WORKER_PHYSICAL_GPU_ID", "0"))
            used_gpu_ids = list(range(torch.cuda.device_count()))
            self.device = f"cuda:{base_device_id}"
            log.info(f"Using on devices: {used_gpu_ids}. Base device set to: {self.device}")
        else:
            pass


        log.info(f"Loading OpenCLIP model '{openclip_model_name}' pretrained on '{openclip_pretrained}' for internal name '{self._model_name}' on device '{self.device}'")

        clip_cache_dir = str(config.CLIP_CACHE_DIR) if config.CLIP_CACHE_DIR else None
        try:
            # Use the OpenCLIP specific names here for loading
            # Load model initially onto the base device
            self.model, _, self.preprocess = open_clip.create_model_and_transforms(
                openclip_model_name, pretrained=openclip_pretrained, 
                device=self.device,
                cache_dir=clip_cache_dir
            )
            # Set the model to evaluation mode (important for inference)
            self.model.eval()

            log.info(f"CLIP model '{self._model_name}' loaded successfully on device: {self.device}")

        except Exception as e:
             log.error(f"Failed to load OpenCLIP model '{openclip_model_name}' pretrained on '{openclip_pretrained}': {e}", exc_info=True)
             # Raise a more specific error if possible, or wrap in RuntimeError
             if isinstance(e, FileNotFoundError):
                  raise FileNotFoundError(f"OpenCLIP pretrained weights not found or downloadable for '{openclip_model_name}' pretrained='{openclip_pretrained}'. Details: {e}") from e
             else:
                  raise RuntimeError(f"Failed to load OpenCLIP model '{self._model_name}'. Details: {e}") from e

    @property
    def model_name(self) -> str:
        """Returns the internal name used for caching and API."""
        return self._model_name

    def task_type(self) -> ModelTaskType:
        """Returns the task type supported by this wrapper."""
        return ModelTaskType.EMBEDDING
    
    # process_image method is still needed for single image processing
    # It should move the single image tensor to the primary device before calling the model

    def process_image(self, frame: np.ndarray, timestamp: float = 0.0, frame_index: int = -1) -> EmbeddingFrameResult:
        """
        Generates embedding for a single image (numpy array).
        Assumes frame is BGR format (OpenCV default).
        """
        if frame is None or frame.size == 0:
             log.warning("Received empty frame for embedding processing.")
             return EmbeddingFrameResult(embedding=[], frame_index=frame_index, timestamp=timestamp, processing_time_ms=0.0)

        start_time = time.perf_counter()
        try:
            pil_img = Image.fromarray(frame[..., ::-1])
        except Exception as e:
            log.error(f"Error converting frame to PIL image: {e}", exc_info=True)
            raise RuntimeError("Failed to convert image frame for CLIP processing.") from e

        try:
            img_t = self.preprocess(pil_img).unsqueeze(0).to(self.device)
        except Exception as e:
            log.error(f"Error applying CLIP preprocessing or moving to device: {e}", exc_info=True)
            raise RuntimeError("Failed during CLIP preprocessing.") from e

        with torch.no_grad():
            try:
                emb = self.model.encode_image(img_t)
            except Exception as e:
                 log.error(f"Error during CLIP model encoding: {e}", exc_info=True)
                 raise RuntimeError("Failed during CLIP model encoding.") from e

        try:
            emb = emb / emb.norm(dim=-1, keepdim=True)
            emb_np = emb.cpu().numpy().flatten()
        except Exception as e:
             log.error(f"Error normalizing or converting CLIP embedding: {e}", exc_info=True)
             raise RuntimeError("Failed during CLIP postprocessing.") from e

        processing_time_ms = (time.perf_counter() - start_time) * 1000.0
        log.debug(f"Generated CLIP embedding of size {emb_np.shape[0]} in {processing_time_ms:.2f} ms.")
        return EmbeddingFrameResult(
            embedding=emb_np.tolist(),
            frame_index=frame_index,
            timestamp=timestamp,
            processing_time_ms=processing_time_ms
        )
        
    def detect_from_bytes(self, image_bytes: bytes, timestamp: float = 0.0, frame_index: int = -1, **kwargs: Any) -> EmbeddingFrameResult:
        """
        Generates embedding for a single image from bytes.
        """
        nparr = np.frombuffer(image_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if frame is None:
            log.warning(f"Failed to decode image from bytes for frame {frame_index}.")
            # Return an empty/default result rather than raising an error if an empty frame is acceptable
            return EmbeddingFrameResult(embedding=[], frame_index=frame_index, timestamp=timestamp, processing_time_ms=0.0)
        return self.detect_from_frame(frame, timestamp, frame_index, **kwargs)

    def detect_from_frame(self, frame: np.ndarray, timestamp: float = 0.0, frame_index: int = -1, **kwargs: Any) -> EmbeddingFrameResult:
        """
        Generates embedding for a single image (numpy array).
        Assumes frame is BGR format (OpenCV default).
        """
        if frame is None or frame.size == 0:
             log.warning("Received empty frame for embedding processing.")
             return EmbeddingFrameResult(embedding=[], frame_index=frame_index, timestamp=timestamp, processing_time_ms=0.0)

        # Call detect_batch with a single frame
        results = self.detect_batch([frame], timestamps=[timestamp], frame_indices=[frame_index], **kwargs)
        
        if results:
            return results[0]
        else:
            # This case should ideally not happen if detect_batch handles single non-empty frames
            log.warning(f"detect_batch returned empty list for single frame {frame_index}. Returning empty result.")
            return EmbeddingFrameResult(embedding=[], frame_index=frame_index, timestamp=timestamp, processing_time_ms=0.0)

    def detect_batch(self, frames: List[np.ndarray], timestamps: Optional[List[float]] = None, frame_indices: Optional[List[int]] = None) -> List[EmbeddingFrameResult]:
        """
        Generates embeddings for a batch of images.
        """
        log.debug(f"Processing batch of {len(frames)}")
        if not frames:
            return [] # Return empty list for empty input batch

        log.debug(f"for CLIP embeddings.")
        batch_start_time = time.perf_counter()
        # Preprocess all images (PIL conversion + transforms)
        transformed_images: List[torch.Tensor] = []
        valid_indices: List[int] = [] # Отслеживаем исходные индексы действительных кадров
        for i, frame in enumerate(frames):
            if frame is None or frame.size == 0:
                 log.warning(f"Skipping empty frame {i} in batch processing.")
                 continue # Skip empty frames in batch
            try:
                # Convert BGR numpy array to RGB PIL Image
                pil_img = Image.fromarray(frame[..., ::-1])
                # Apply preprocessing transforms - DO NOT unsqueeze yet, stack does that
                # Move to the primary device (self.device is the base device for DataParallel)
                img_t = self.preprocess(pil_img).to(self.device)
                transformed_images.append(img_t)
                valid_indices.append(i) # Сохраняем исходный индекс
            except Exception as e:
                log.error(f"Error processing frame {i} in CLIP batch: {e}", exc_info=True)
                # Decide how to handle errors in batch: skip or raise? Skipping for now.
                continue # Skip frame on error
        
        
        if not transformed_images:
             log.warning("No valid images left after preprocessing for batch.")
             return [] # Return empty if all images failed preprocessing

        # Stack transformed tensors into a single batch tensor
        try:
            # Stack adds the batch dimension (size len(transformed_images))
            # This batch_tensor is already on the primary device (e.g., cuda:0)
            batch_tensor = torch.stack(transformed_images)
        except Exception as e:
            log.error(f"Error stacking CLIP image batch tensors: {e}", exc_info=True)
            raise RuntimeError(f"Failed to create batch tensor for CLIP batch: {e}") from e

        # Encode the batch using the (potentially wrapped) model
        # No autocast needed here
        embeddings_results: List[EmbeddingFrameResult] = []
        with torch.no_grad():
            try:
                # If self.model is DataParallel, it will scatter batch_tensor,
                # run inference on multiple GPUs, and gather results back to the main device.
                batch_embeddings = self.model.encode_image(batch_tensor)

                # Normalization happens on the main device after gathering
                batch_embeddings /= batch_embeddings.norm(dim=-1, keepdim=True)
                
                batch_total_time_ms = (time.perf_counter() - batch_start_time) * 1000.0
                avg_processing_time_per_frame = batch_total_time_ms / len(transformed_images) if transformed_images else batch_total_time_ms # <--- ДОБАВЛЕНО

                # Convert each embedding in the batch back to numpy array
                # results are already on the main device thanks to DataParallel gather
                for i, emb_np in enumerate(batch_embeddings.cpu().numpy().tolist()):
                    original_idx = valid_indices[i]
                    embeddings_results.append(
                        EmbeddingFrameResult(
                            embedding=emb_np,
                            frame_index=frame_indices[original_idx] if frame_indices else original_idx,
                            timestamp=timestamps[original_idx] if timestamps else 0.0,
                            processing_time_ms=avg_processing_time_per_frame # Время на кадр нелегко получить в пакете
                        )
                    )

            except Exception as e:
                 log.error(f"Error during CLIP model batch encoding: {e}", exc_info=True)
                 # Specific check for device/type errors that DataParallel might still reveal
                 if "Expected all tensors to be on the same device" in str(e) or "Input type" in str(e) and "weight type" in str(e):
                      log.error("Potential device or type mismatch issue during DataParallel execution.")
                 raise RuntimeError("Failed during CLIP model batch encoding.") from e

        batch_total_time_ms = (time.perf_counter() - batch_start_time) * 1000.0
        
        log.debug(f"Generated {len(embeddings_results)} CLIP embeddings from batch in {batch_total_time_ms:.2f} ms.")
        return embeddings_results

    def unload(self) -> None:
        """
        Releases model resources. Called by the cache manager.
        Handles DataParallel case.
        """
        log.info("Unloading CLIP model '%s' (%s/%s) from device '%s' ...",
                 self._model_name, self._openclip_model_name, self._openclip_pretrained, self.device)
        try:
            if hasattr(self, 'model') and self.model is not None:
                # If it's DataParallel, we need to access the underlying module
                if isinstance(self.model, nn.DataParallel):
                    log.debug("Unwrapping DataParallel model for unload.")
                    # Attempt to access the original module (may vary based on DP setup)
                    # This is a common pattern, but might need adjustment based on how exactly DataParallel is used.
                    # For simple cases, accessing .module might work if it wasn't moved before wrapping.
                    # However, DataParallel itself holds references. Deleting the wrapper should be enough.
                    # For a clean unload, simply delete the DataParallel wrapper.
                    pass # No explicit unwrapping needed before deleting the wrapper
                else:
                     # Move single model to CPU if on CUDA
                     if self.device.startswith('cuda') and torch.cuda.is_available():
                          self.model.to('cpu')
                          log.debug("CLIP model moved to CPU.")

                del self.model # Delete the model instance (either base or DataParallel wrapper)
                self.model = None # Set to None

            # Delete other potentially large attributes
            if hasattr(self, 'preprocess') and self.preprocess is not None:
                 del self.preprocess
                 self.preprocess = None
            # If you had a tokenizer instance:
            # if hasattr(self, 'tokenizer') and self.tokenizer is not None:
            #     del self.tokenizer
            #     self.tokenizer = None

            # Suggest garbage collection
            gc.collect()

            # Empty CUDA cache if on GPU
            if self.device.startswith('cuda') and torch.cuda.is_available():
                try:
                    # Empty cache for *all* devices used by DataParallel
                    torch.cuda.empty_cache()
                    log.debug("torch.cuda.empty_cache() called after CLIP unload.")
                except Exception as e:
                    log.warning(f"Error calling torch.cuda.empty_cache() during CLIP unload: {e}")

            log.info("CLIP model '%s' unloaded successfully.", self._model_name)

        except Exception as e:
            log.warning("Error while unloading CLIP model '%s': %s",
                           self._model_name, e, exc_info=True)

    def mem_bytes(self) -> int:
        """
        Estimates memory used by the model.
        Returns bytes.
        This is hard to do accurately for DataParallel.
        """
        # Estimating memory for DataParallel is complex as it scatters the model.
        # A simple approach is to estimate the size on the primary device + a factor for others.
        # Or, more simply, return 0 or rely on higher-level monitoring.
        # Let's keep the simple 0 estimate for now.
        return 0