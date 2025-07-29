from __future__ import annotations
import logging
from PIL import Image, ImageOps, ImageChops
from typing import Optional
from sensory_detector.yolo_server.app.config import OCRImageProcessingConfig
import numpy as np
import cv2 
log = logging.getLogger(__name__)

try:
    Resampling = Image.Resampling  # Pillow ≥ 9.1
except AttributeError:             # Pillow < 9.1
    Resampling = Image

class OCRImageProcessor:
    def __init__(self, config: OCRImageProcessingConfig):
        if not isinstance(config, OCRImageProcessingConfig):
            raise TypeError("config must be OCRImageProcessingConfig")
        self._cfg = config
        self.enabled = config.enabled

    # ─ public ─
    def process_image(self, image: Image.Image) -> Image.Image:
        if not self._cfg.enabled:
            return image
        img = image.copy()

        # background / B&W
        if self._cfg.background_processing_enabled:
            img = self._process_background(img)

        # resize
        if self._cfg.resize_enabled:
            img = self._resize(img)

        if self._cfg.beckbin:
            img = self._apply_mixed_background_binarization(img)
        # borders (needs color compatible with current image mode)
        if self._cfg.borders_enabled and self._cfg.border_size > 0:
            # --- ПЕРЕМЕЩЕНО И ИЗМЕНЕНО: ОПРЕДЕЛЯЕМ ЦВЕТ ГРАНИЦЫ ПОСЛЕ ОБРАБОТКИ ФОНА ---
            border_color_rgb = self._cfg.border_color # Конфигурированный цвет как RGB

            # Определяем цвет заливки границы в зависимости от текущего режима изображения
            # ImageOps.expand для режима '1' неявно преобразует его в 'L'.
            # Поэтому для режимов 'L' и '1' нам нужен integer.
            if img.mode in ("L", "1"):
                # Конвертируем RGB цвет границы в grayscale integer
                r, g, b = border_color_rgb
                border_fill_color = int(0.299 * r + 0.587 * g + 0.114 * b)
                # Убедимся, что цвет в диапазоне 0-255
                border_fill_color = max(0, min(255, border_fill_color))
            elif img.mode == "RGB":
                # Для RGB используем RGB кортеж как есть
                border_fill_color = border_color_rgb
            # Добавьте другие режимы, если необходимо (RGBA, P, etc.)
            # Для большинства других режимов может потребоваться int или single-element tuple
            # или конвертация в RGB/L. Пока обрабатываем L, 1, RGB как наиболее частые.
            # Если возникнут другие ошибки, нужно будет добавить их сюда.
            else:
                # Fallback: попробуем использовать RGB кортеж. Pillow может справиться,
                # или может потребоваться конвертация в RGB/L.
                log.warning(f"OCRImageProcessor: Handling border for unexpected image mode '{img.mode}'. Using RGB color.")
                try:
                     # Попробуем конвертировать изображение в RGB перед добавлением границы
                     original_mode = img.mode
                     img = img.convert("RGB")
                     border_fill_color = border_color_rgb
                     log.debug(f"Converted image from {original_mode} to RGB for border processing.")
                except Exception as e:
                     log.error(f"Could not convert image mode '{img.mode}' to RGB for border. Falling back to integer color.", exc_info=True)
                     # Если не удалось конвертировать в RGB, попробуем grayscale
                     r, g, b = border_color_rgb
                     border_fill_color = int(0.299 * r + 0.587 * g + 0.114 * b)
                     border_fill_color = max(0, min(255, border_fill_color))
                     # Попробуем конвертировать изображение в L
                     try:
                          img = img.convert("L")
                          log.debug(f"Converted image from {original_mode} to L for border processing fallback.")
                     except Exception:
                          log.error(f"Could not convert image mode '{original_mode}' to L either. Border might fail.", exc_info=True)
                          # В крайнем случае, просто используем рассчитанный grayscale integer цвет

            # Добавляем границу с выбранным цветом
            img = ImageOps.expand(img, border=self._cfg.border_size, fill=border_fill_color)
            #img.save('/home/fox/Services/Yolo/src/sensory_detector/yolo_server/ocr/image_processor.png')
            # -----------------------------------------------------------------


        return img
    
    # ─ internal helpers ─
    def _resize(self, img: Image.Image) -> Image.Image:
        mode = self._cfg.resize_mode
        filt_name = self._cfg.resize_filter.upper()
        filt = getattr(Resampling, filt_name, getattr(Image, filt_name, Resampling.LANCZOS))
        if mode == "target_dim":
            target = self._cfg.resize_target_dim or max(img.size)
            if max(img.size) <= target:
                return img
            if img.width > img.height:
                new = (target, int(img.height * target / img.width))
            else:
                new = (int(img.width * target / img.height), target)
        else:
            factor = self._cfg.resize_scale_factor or 1.0
            new = (int(img.width * factor), int(img.height * factor))
        return img.resize(new, resample=filt)

    def _process_background(self, img: Image.Image) -> Image.Image:
        if img.mode != "L":
            img = img.convert("L")
        w, h = img.size
        s = self._cfg.background_sample_size
        corners = []
        corners.extend(img.crop((0, 0, s, s)).getdata())
        corners.extend(img.crop((w - s, 0, w, s)).getdata())
        corners.extend(img.crop((0, h - s, s, h)).getdata())
        corners.extend(img.crop((w - s, h - s, w, h)).getdata())
        if not corners:
            return img
        avg = sum(corners) / len(corners)
        invert = avg <= self._cfg.background_lightness_threshold
        if invert:
            img = ImageOps.invert(img)
        bw_thr = self._cfg.bw_threshold
        img = img.point(lambda p: 0 if p <= bw_thr else 255, mode="1")
        return img
    

    def _apply_mixed_background_binarization(self, img: Image.Image) -> Image.Image:
        """
        Двух-проходная адаптивная бинаризация.

        1-й проход: erode только mask_dark  →  result1 = ~mask_light   (mask = mask_dark)
        2-й проход: erode только mask_light →  result2 = ~mask_dark   (mask = mask_light)

        Итог = result1 AND result2  →  белый фон / чёрный текст, «дырки» сохраняются.
        Возвращается Pillow-Image mode '1'.
        """

        # ————— общие константы ———————————————————————————————————————
        BLOCK_SIZE           = 25        # нечётное, ~2-4 высоты символа
        C_DARK               = 0
        C_LIGHT              = 0
        MAX_BLACK_BLOB_RATIO = 0.03      # >3 % кадра считаем фоном
        # ----------------------------------------------------------------

        gray = np.asarray(img.convert("L"), dtype=np.uint8)

        # ----------------------------------------------------------------
        # ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
        # ----------------------------------------------------------------
        def _make_masks() -> tuple[np.ndarray, np.ndarray]:
            """строим две адаптивные маски (тёмный-текст и светлый-текст)"""
            m_dark = cv2.adaptiveThreshold(
                gray, 255,
                cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,
                BLOCK_SIZE, C_DARK
            )
            m_light = cv2.adaptiveThreshold(
                gray, 255,
                cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV,
                BLOCK_SIZE, C_LIGHT
            )
            return m_dark, m_light

        def _wipe_big_black(mask: np.ndarray) -> np.ndarray:
            """убираем крупные (фоновые) чёрные пятна"""
            h, w = mask.shape
            thr  = int(h * w * MAX_BLACK_BLOB_RATIO)
            n, lbl, stats, _ = cv2.connectedComponentsWithStats((mask == 0).astype(np.uint8))
            for i in range(1, n):
                if stats[i, cv2.CC_STAT_AREA] > thr:
                    mask[lbl == i] = 255
            return mask

        def _pass(erode_dark: bool,
                erode_light: bool,
                invert_src: str,          # 'dark' | 'light'
                invert_mask: str          # 'dark' | 'light'
                ) -> np.ndarray:
            """один проход + опциональное erode + инверсия с маской"""
            m_dark, m_light = _make_masks()

            # лёгкое «усушение» нужной маски
            kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (5, 5))
            if erode_dark:
                m_dark  = cv2.erode(m_dark,  kernel, iterations=1)
            if erode_light:
                m_light = cv2.erode(m_light, kernel, iterations=1)

            # чистим крупные заливки
            m_dark  = _wipe_big_black(m_dark)
            m_light = _wipe_big_black(m_light)

            # выбираем src и mask для cv2.bitwise_not(...)
            src  = m_dark  if invert_src  == "dark"  else m_light
            mask = m_dark  if invert_mask == "dark"  else m_light

            return cv2.bitwise_not(src, mask=mask)   # белый фон / чёрный текст

        # ----------------------------------------------------------------
        # ПРОХОД 1  (усушка dark-маски)
        # ----------------------------------------------------------------
        img1 = _pass(
            erode_dark  = True,
            erode_light = False,
            invert_src  = "light",
            invert_mask = "dark"
        )

        if np.count_nonzero(img1 == 0) > img1.size * 0.5:
            img1 = cv2.bitwise_not(img1)
        # ----------------------------------------------------------------
        # ПРОХОД 2  (усушка light-маски)
        # ----------------------------------------------------------------
        img2 = _pass(
            erode_dark  = False,
            erode_light = True,
            invert_src  = "dark",
            invert_mask = "light"
        )

        if np.count_nonzero(img2 == 0) > img2.size * 0.5:
            img2 = cv2.bitwise_not(img2)
        # ----------------------------------------------------------------
        # «накладываем» два результата
        # ----------------------------------------------------------------
        final_bin = cv2.bitwise_and(img1, img2)      # 0 если хотя бы один 0; 255 иначе

        # Pillow back → mode '1'
        # 6. Гарантируем: фон белый
        img_binary_inv = Image.fromarray(final_bin).convert("1")       
        #img_binary_inv.save('/home/fox/Services/Yolo/src/sensory_detector/yolo_server/ocr/binary_inv.png') # For debugging
        # 4) переводим обратно в Pillow, сразу в режим '1'
        return img_binary_inv