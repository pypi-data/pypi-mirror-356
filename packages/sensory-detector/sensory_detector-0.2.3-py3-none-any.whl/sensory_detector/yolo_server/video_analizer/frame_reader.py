# project_root/yolo_server/frame_reader.py
import av
import numpy as np
import logging
import os
from typing import Generator, Tuple, Optional, Union, Any
from pathlib import Path
try:                                # PyAV >= 11
    from av.error import FFmpegError as _AVError
except (ImportError, AttributeError):
    # «старый» PyAV
    _AVError = getattr(av, "AVError", OSError)
AVError = _AVError    

logger = logging.getLogger(__name__)

class FrameReadError(Exception):
    """Custom exception for errors during frame reading."""
    pass

class FrameReader:
    """
    Reads video frames from a file using pyAV and yields them.
    Acts as a context manager for resource handling.
    """
    def __init__(self, video_source: Union[str, Any]):
        self.video_source = video_source # Сохраняем исходный источник
        self._container: Optional[av.container.InputContainer] = None
        self._stream: Optional[av.Stream] = None
        self._frame_iterator: Optional[Generator] = None
        self._frame_count = 0

        if isinstance(video_source, str):
            if not os.path.exists(video_source):
                logger.error(f"Video file not found for reading: {video_source}")
                raise FileNotFoundError(f"Video file not found: {video_source}")

        logger.info(f"FrameReader initialized for source type: {type(video_source).__name__}")

    def __enter__(self) -> "FrameReader":
        try:
            print()
            self._container = av.open(self.video_source) # Blocking call
            self._stream = self._container.streams.video[0]
            self._frame_iter = self._container.decode(self._stream)
            logger.info(
                "Opened video source: codec=%s, fps=%s",
                self._stream.codec_context.codec.name,
                self._stream.average_rate,
            )
            return self
        except IndexError as e:
            self.close()
            raise FrameReadError(f"No video stream in source {type(self.video_source).__name__}") from e
        except AVError as e:
            self.close()
            logger.error(f"PyAV cannot open source {type(self.video_source).__name__}: {e}", exc_info=True)
            # Более информативное сообщение об ошибке PyAV
            error_detail = str(e)
            if "seek" in error_detail.lower() and not isinstance(self.video_source, str):
                    # Если ошибка связана с seek и источник не строка (т.е. файловый объект)
                    error_detail += " (This might happen if the file-like object is not seekable, try saving to disk first if necessary)"
            raise FrameReadError(f"PyAV cannot open or process source {type(self.video_source).__name__}: {error_detail}") from e
        except Exception:
            logger.error(f"Unexpected error in FrameReader.__enter__ for source {type(self.video_source).__name__}.", exc_info=True)
            self.close()
            raise

    # __exit__ и read_frames() остаются без изменений, close() тоже
    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.debug(f"Closing video container for source type: {type(self.video_source).__name__}.")
        self.close()
        return False
    
    def read_frames(self) -> Generator[Tuple[int, np.ndarray, float], None, None]:
        """Yields (idx, frame_bgr, ts_seconds)."""
        if self._frame_iter is None:
            raise FrameReadError("FrameReader must be used inside a `with` block")

        for idx, frame in enumerate(self._frame_iter):
            try:
                logger.debug(f"Decoding frame {idx} to numpy array...") # <-- НОВЫЙ ЛОГ
                img = frame.to_ndarray(format="bgr24")
                ts = float(frame.time or 0.0)
                logger.debug(f"Successfully decoded frame {idx} to numpy ({img.shape}).") # <-- НОВЫЙ ЛОГ
                yield idx, img, ts
            except AVError as e:
                logger.warning("AVError on frame %s: %s (skipped)", idx, e)
                continue
            except Exception as e:
                logger.warning("Unexpected error on frame %s: %s (skipped)", idx, e)
                continue

    def close(self):
        """Closes the pyAV container and releases resources."""
        if self._container:
            try:
                # Ensure container is closed regardless of source type
                self._container.close()
                logger.debug(f"Video container for source type {type(self.video_source).__name__} closed.")
            except Exception as e:
                logger.warning(f"Error closing video container for source type {type(self.video_source).__name__}: {e}", exc_info=True)
            self._container = None
            self._stream = None
            self._frame_iterator = None
    # __del__ тоже без изменений
    def __del__(self):
        self.close()