
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
import av
import open_clip

openclip_model_name: str = 'ViT-B-32' # Specific OpenCLIP model architecture name
openclip_pretrained: str = 'laion2b_s34b_b79k' # Specific OpenCLIP pretrained weights name
device = f"cuda:0"
clip_cache_dir = './'
model, _, preprocess = open_clip.create_model_and_transforms(
                openclip_model_name, pretrained=openclip_pretrained, 
                device=device,
                cache_dir=clip_cache_dir
            )
_container = av.open("/home/fox/Services/Yolo/tests/data/screen.avi") # Blocking call
_stream = _container.streams.video[0]
_frame_iter = _container.decode(_stream)

startr = time.time()
for idx, frame in enumerate(_frame_iter):
    start = time.time()
    img = frame.to_ndarray(format="bgr24")
    pil_img = Image.fromarray(img[..., ::-1])
    img_t = preprocess(pil_img).unsqueeze(0).to(device)
    emb = model.encode_image(img_t)
    #emb = emb / emb.norm(dim=-1, keepdim=True)
    #emb_np = emb.cpu().numpy().flatten()
    print(time.time() -start)

print(time.time() -startr)