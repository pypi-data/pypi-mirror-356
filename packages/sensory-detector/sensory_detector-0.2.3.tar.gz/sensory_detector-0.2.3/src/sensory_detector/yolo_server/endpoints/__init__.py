# Содержимое файла: src/sensory_detector/yolo_server/endpoints/__init__.py
# Импортируем только роутеры, которые будут включаться в основной FastAPI-приложение
"""
Роутеры объединяются здесь для удобного импорта в main.py
"""
import base64, cv2, numpy as np
from typing import Tuple
from .objects import router as objects_router  # noqa: F401
from .texts import router as texts_router      # noqa: F401
from .embeddings import router as embed_router # noqa: F401

__all__ = ["objects_router", "texts_router", "embed_router"] # Обновляем __all__

def b64_to_cv2(b64_str: str):
    return cv2.imdecode(
        np.frombuffer(base64.b64decode(b64_str), np.uint8), cv2.IMREAD_COLOR
    )

def cv2_to_b64(img) -> str:
    _, buf = cv2.imencode(".png", img)
    return base64.b64encode(buf).decode()

def crop(img, roi: Tuple[int, int, int, int]):
    x1, y1, x2, y2 = roi
    return img[y1:y2, x1:x2]


