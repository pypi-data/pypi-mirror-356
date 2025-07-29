# ocr_service/detectors/tesseract/tesseract_wrapper.py

import ctypes
import ctypes.util
import os, sys
import logging
from PIL import Image
# from io import BytesIO # Больше не нужна, т.к. принимаем PIL Image напрямую
from typing import Dict, Any, Optional, List, Tuple, TYPE_CHECKING
from sensory_detector.yolo_server.app.config import TesseractConfig  
from sensory_detector.yolo_server.ocr.image_processor import OCRImageProcessor
from sensory_detector.models.models import OCRFrameResult, Bbox, OCRWordResult   
from typing import Optional, Tuple, TYPE_CHECKING



# Добавьте импорт этого класса в соответствующие __init__.py файлы модулей modules/session/data/


    
    
import ctypes
import ctypes.util
import os
import logging
import time # Импортируем для замера времени
from PIL import Image
from typing import Dict, Any, Optional, List, Tuple

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
class TesseractError(Exception):
    """Специальное исключение для ошибок Tesseract."""
    pass

class TesseractWrapper:
    _lib = None # Будет загружена один раз на процесс
    PLATFORM_LIB_NAMES: Dict[str, List[str]] = {
        "linux": ['libtesseract.so.5', 'libtesseract.so.4', 'libtesseract.so', 'tesseract'], # Add 'tesseract' as a common name for find_library
        "win32": ['libtesseract-5.dll', 'libtesseract-4.dll', 'libtesseract3051.dll', 'libtesseract304.dll', 'tesseract'], # Add 'tesseract' for find_library (might need dll suffix?)
        "darwin": ['libtesseract.dylib', 'tesseract'], # Add 'tesseract' for find_library
        # Add other platforms as needed
    }

    
    class TessBaseAPI(ctypes._Pointer):
        _type_ = type('_TessBaseAPI', (ctypes.Structure,), {})

    class TessResultIterator(ctypes._Pointer): # Определение типа итератора
        _type_ = type('_TessResultIterator', (ctypes.Structure,), {})

    # Выносим Enum уровней итерации на уровень класса
    # Используем ctypes.c_int как базовый тип, как в capi.h
    class TessPageIteratorLevel(ctypes.c_int):
        RIL_BLOCK = 0      # Block of text
        RIL_PARA = 1       # Paragraph
        RIL_TEXTLINE = 2   # Line of text
        RIL_WORD = 3       # Word
        RIL_SYMBOL = 4     # Character/Symbol

    # Добавляем TessOrientation и TessScriptDirection если планируется авто-ориентация
    class TessOrientation(ctypes.c_int):
        ORIENTATION_PAGE_UP = 0
        ORIENTATION_PAGE_RIGHT = 1
        ORIENTATION_PAGE_DOWN = 2
        ORIENTATION_PAGE_LEFT = 3

    class TessScriptDirection(ctypes.c_int):
        WRITING_DIRECTION_LEFT_TO_RIGHT = 0
        WRITING_DIRECTION_RIGHT_TO_LEFT = 1
        WRITING_DIRECTION_TOP_TO_BOTTOM = 2

    class TessTextlineOrder(ctypes.c_int):
         ORDER_LEFT_TO_RIGHT = 0
         ORDER_RIGHT_TO_LEFT = 1
         ORDER_TOP_TO_BOTTOM = 2


    @classmethod
    def _get_tesseract_lib(cls, config: "TesseractConfig"):
        """
        Загружает библиотеку Tesseract C API один раз на процесс.
        Сначала пытается найти библиотеку в директории, указанной в config.lib_path.
        Если не найдено, использует системный поиск (ctypes.util.find_library).

        Args:
            config: Объект конфигурации Tesseract (TesseractConfig), содержащий lib_path.

        Returns:
            Загруженная библиотека Tesseract (ctypes.CDLL).

        Raises:
            TesseractError: Если библиотека не найдена.
        """
        if cls._lib is not None:
            log.debug("Tesseract library already loaded.")
            return cls._lib

        log.info("Attempting to load Tesseract library...")

        found_lib_path: Optional[str] = None
        current_platform = sys.platform
        # Получаем список имен файлов библиотек для текущей платформы
        platform_lib_names = cls.PLATFORM_LIB_NAMES.get(current_platform, [])
        lib_dir_from_config = config.lib_path # Получаем путь к директории из конфига

        log.info(f"Current platform: {current_platform}")
        log.info(f"Expected library names: {platform_lib_names}")
        log.info(f"Configured library directory: {lib_dir_from_config}")


        # 1. Попытка найти библиотеку в указанной в конфиге директории
        if lib_dir_from_config:
            log.info(f"Searching in configured directory: {lib_dir_from_config}")
            # Убеждаемся, что путь из конфига - это директория
            if os.path.isdir(lib_dir_from_config):
                 for lib_name in platform_lib_names:
                      full_path = os.path.join(lib_dir_from_config, lib_name)
                      log.debug(f"Checking: {full_path}")
                      if os.path.exists(full_path):
                           found_lib_path = full_path
                           print(f"Found Tesseract library in configured directory: {found_lib_path}")
                           break # Нашли библиотеку, прекращаем поиск в этой директории
                 if not found_lib_path:
                     log.warning(f"None of the expected library names found in configured directory {lib_dir_from_config}.")
            else:
                 log.warning(f"Configured Tesseract library path '{lib_dir_from_config}' is not a valid directory or does not exist. Trying system search.")
        else:
            log.debug("No Tesseract library directory configured ('lib_path' is None). Trying system search.")


        # 2. Если не найдено в указанной директории, пытаемся использовать системный поиск
        if not found_lib_path:
            log.debug("Attempting system search for Tesseract library...")
            # ctypes.util.find_library обычно ищет по базовому имени, например 'tesseract'
            # На некоторых системах может потребоваться полное имя файла (например, 'libtesseract.so.4')
            # Попробуем сначала полные имена из списка, потом общее имя 'tesseract'
            system_search_names_to_try = platform_lib_names + ['tesseract'] # Добавляем 'tesseract' как запасной вариант для find_library

            for name_to_try in system_search_names_to_try:
                 system_path = ctypes.util.find_library(name_to_try)
                 if system_path:
                     found_lib_path = system_path
                     log.info(f"Found Tesseract library using system search: {found_lib_path}")
                     break # Нашли библиотеку, прекращаем системный поиск

            if not found_lib_path:
                 log.error(f"Tesseract library not found in system search for names: {system_search_names_to_try}")


        # 3. Проверяем, найдена ли библиотека, и загружаем ее
        if not found_lib_path:
            # Если библиотека не найдена после всех попыток
             error_msg = (
                 f"Tesseract library not found for platform '{current_platform}'. "
                 f"Looked for names: {platform_lib_names} and 'tesseract'. "
                 f"Tried configured directory '{lib_dir_from_config}' (if specified) and system search."
                 f"Please ensure libtesseract is installed and in your system's PATH, "
                 f"or configure 'lib_path' in tesseract_config.py or .env with the correct directory path."
             )
             log.error(error_msg)
             raise TesseractError(error_msg)

        # Загрузка найденной библиотеки
        try:
            cls._lib = ctypes.CDLL(found_lib_path)
            log.info(f"Successfully loaded Tesseract library from: {found_lib_path}")
        except OSError as e:
            # Если загрузка не удалась, хотя файл найден
            raise TesseractError(f"Failed to load Tesseract library from {found_lib_path}: {e}") from e

        # Настройка сигнатур функций API
        # https://github.com/tesseract-ocr/tesseract/blob/main/src/api/capi.h
        # 4. Настройка сигнатур API и проверка обязательных функций (остаются без изменений)
        cls._configure_api_signatures()
        cls._check_required_functions()
        return cls._lib
           
    @classmethod
    def _configure_api_signatures(cls):
        """Настраивает сигнатуры функций Tesseract C API."""
        if not cls._lib:
            raise TesseractError("Tesseract library not loaded before configuring API signatures.")

        # --- Настройка сигнатур функций API (ваш существующий код) ---
        # Основные функции
        cls._lib.TessBaseAPICreate.restype = cls.TessBaseAPI
        cls._lib.TessBaseAPIDelete.argtypes = (cls.TessBaseAPI,)
        cls._lib.TessBaseAPIInit3.argtypes = (cls.TessBaseAPI, ctypes.c_char_p, ctypes.c_char_p)
        cls._lib.TessBaseAPIInit3.restype = ctypes.c_int # 0 on success
        cls._lib.TessBaseAPISetImage.argtypes = (cls.TessBaseAPI, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int)
        cls._lib.TessBaseAPISetImage.restype = None
        cls._lib.TessBaseAPISetVariable.argtypes = (cls.TessBaseAPI, ctypes.c_char_p, ctypes.c_char_p)
        cls._lib.TessBaseAPISetVariable.restype = ctypes.c_int # 0 for failure, non-zero for success
        cls._lib.TessBaseAPIGetUTF8Text.restype = ctypes.c_char_p # MUST BE FREED by TessDeleteText
        cls._lib.TessBaseAPIGetUTF8Text.argtypes = (cls.TessBaseAPI,)
        cls._lib.TessDeleteText.argtypes = (ctypes.c_char_p,) # Function to free text returned by GetUTF8Text etc.
        cls._lib.TessDeleteText.restype = None # Should be void

        # Функции для итерации и деталей
        cls._lib.TessBaseAPIRecognize.argtypes = (cls.TessBaseAPI, ctypes.c_void_p)
        cls._lib.TessBaseAPIRecognize.restype = ctypes.c_int # 0 on success

        cls._lib.TessBaseAPIGetIterator.argtypes = (cls.TessBaseAPI,)
        cls._lib.TessBaseAPIGetIterator.restype = cls.TessResultIterator
        if hasattr(cls._lib, 'TessBaseAPIGetMutableIterator'):
             cls._lib.TessBaseAPIGetMutableIterator.argtypes = (cls.TessBaseAPI,)
             cls._lib.TessBaseAPIGetMutableIterator.restype = cls.TessResultIterator


        cls._lib.TessResultIteratorDelete.argtypes = (cls.TessResultIterator,)
        cls._lib.TessResultIteratorDelete.restype = None

        cls._lib.TessResultIteratorNext.argtypes = (cls.TessResultIterator, cls.TessPageIteratorLevel)
        cls._lib.TessResultIteratorNext.restype = ctypes.c_int

        cls._lib.TessResultIteratorGetUTF8Text.argtypes = (cls.TessResultIterator, cls.TessPageIteratorLevel)
        cls._lib.TessResultIteratorGetUTF8Text.restype = ctypes.c_char_p

        cls._lib.TessPageIteratorBoundingBox.argtypes = (
            cls.TessResultIterator, cls.TessPageIteratorLevel,
            ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int),
            ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)
        )
        cls._lib.TessPageIteratorBoundingBox.restype = ctypes.c_int

        if hasattr(cls._lib, 'TessResultIteratorConfidence'):
             cls._lib.TessResultIteratorConfidence.argtypes = (cls.TessResultIterator, cls.TessPageIteratorLevel)
             cls._lib.TessResultIteratorConfidence.restype = ctypes.c_float

        if hasattr(cls._lib, 'TessBaseAPIMeanTextConf'):
             cls._lib.TessBaseAPIMeanTextConf.argtypes = (cls.TessBaseAPI,)
             cls._lib.TessBaseAPIMeanTextConf.restype = ctypes.c_int # Returns int 0-100

        if hasattr(cls._lib, 'TessBaseAPISetSourceResolution'):
             cls._lib.TessBaseAPISetSourceResolution.argtypes = (cls.TessBaseAPI, ctypes.c_int)
             cls._lib.TessBaseAPISetSourceResolution.restype = None

        if hasattr(cls._lib, 'TessBaseAPISetRectangle'):
             cls._lib.TessBaseAPISetRectangle.argtypes = (cls.TessBaseAPI, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int)
             cls._lib.TessBaseAPISetRectangle.restype = None

        # Functions for auto-orientation
        if hasattr(cls._lib, 'TessBaseAPIDetectOrientationScript'):
            cls._lib.TessBaseAPIDetectOrientationScript.argtypes = (
                 cls.TessBaseAPI, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_float),
                 ctypes.POINTER(ctypes.c_char_p), ctypes.POINTER(cls.TessOrientation),
                 ctypes.POINTER(cls.TessScriptDirection), ctypes.POINTER(cls.TessTextlineOrder),
                 ctypes.POINTER(ctypes.c_float)
            )
            cls._lib.TessBaseAPIDetectOrientationScript.restype = ctypes.c_int # Returns 0 on success


        cls._lib.TessBaseAPIClear.argtypes = (cls.TessBaseAPI,)
        cls._lib.TessBaseAPIClear.restype = None
        cls._lib.TessBaseAPIEnd.argtypes = (cls.TessBaseAPI,)
        cls._lib.TessBaseAPIEnd.restype = None
        # --- Конец настройки сигнатур ---
        return cls._lib

    @classmethod
    def _check_required_functions(cls):
         """Проверяет наличие обязательных функций Tesseract C API после загрузки."""
         required_funcs = [
            'TessBaseAPICreate', 'TessBaseAPIDelete', 'TessBaseAPIInit3',
            'TessBaseAPISetImage', 'TessBaseAPISetVariable', 'TessBaseAPIGetUTF8Text',
            'TessDeleteText', 'TessBaseAPIClear', 'TessBaseAPIEnd', 'TessBaseAPIRecognize',
            'TessBaseAPIGetIterator', 'TessResultIteratorDelete', 'TessResultIteratorNext',
            'TessResultIteratorGetUTF8Text', 'TessPageIteratorBoundingBox'
         ]
         for func_name in required_funcs:
             if not hasattr(cls._lib, func_name):
                 raise TesseractError(f"Required Tesseract function '{func_name}' not found in loaded library. Check Tesseract version.")
         log.debug("All required Tesseract C API functions found.")


    def __init__(
        self,
        config: TesseractConfig # Принимаем объект конфигурации
    ):
        """
        Инициализация обертки Tesseract с использованием объекта конфигурации.

        Args:
            config: Объект конфигурации Tesseract (TesseractConfig).
        """
        if not isinstance(config, TesseractConfig):
            raise TypeError("Config must be an instance of TesseractConfig")
        
        self._config = config # Сохраняем объект конфигурации
        # Ensure the library is loaded before creating API instance
        # Передаем объект конфига в метод загрузки библиотеки
        self._get_tesseract_lib(self._config)

        print('************************')
        self._api: Optional[ctypes._Pointer] = None
        self._is_initialized = False

        # Используем datapath и lang из объекта конфигурации
        datapath = self._config.datapath
        lang = self._config.lang

        if not os.path.exists(datapath):
             # Здесь можно добавить логику для попытки загрузки tessdata, если она отсутствует
             raise TesseractError(f"Tessdata directory not found at {datapath}. Ensure tessdata is installed and accessible, or configure 'datapath' correctly.")

        try:
            self._api = self._lib.TessBaseAPICreate()
            if not self._api:
                 raise TesseractError("Failed to create Tesseract API instance.")

            lang_bytes = lang.encode('utf-8')
            datapath_bytes = datapath.encode('utf-8')

            log.debug(f"Initializing Tesseract API with datapath='{datapath}', lang='{lang}'")
            # Initialize Tesseract with language and data path
            # TessBaseAPIInit3 returns 0 on success, non-zero on failure
            result = self._lib.TessBaseAPIInit3(self._api, datapath_bytes, lang_bytes)

            if result != 0:
                # При ошибке TessBaseAPIInit3, API instance был создан, но не инициализирован
                # Его нужно удалить с TessBaseAPIDelete. TessBaseAPIEnd НЕ вызывается.
                self._lib.TessBaseAPIDelete(self._api)
                self._api = None # Устанавливаем в None перед возбуждением исключения
                raise TesseractError(f"Tesseract API initialization failed for lang='{lang}', datapath='{datapath}' with code {result}.")

            log.info(f"Tesseract API initialized successfully for lang='{lang}'.")
            self._is_initialized = True

            #if self._config.default_whitelist is not None:
            #     self._set_variable("tesseract_char_whitelist", self._config.default_whitelist)
            self._set_variable("tessedit_pageseg_mode", str(self._config.default_psm))
            # Note: OEM is primarily controlled by the init3 parameter, SetVariable might not fully override it.

        except Exception as e:
            log.error(f"Error during TesseractWrapper initialization: {e}", exc_info=True)
            # Ensure API is cleaned up if it was created but initialization failed
            if self._api:
                # If init failed (result != 0), only delete is needed, not End
                self._lib.TessBaseAPIDelete(self._api)
                self._api = None
            raise TesseractError(f"Failed to initialize TesseractWrapper: {e}") from e

    @property
    def name(self) -> str:
        return "tesseract"

    def process_pil_image(
        self,
        image: Image.Image,
        details: bool = None,
        rectangle: Optional[Tuple[int, int, int, int]] = None,
        **params: Any
    ) -> OCRFrameResult | None:
        """
        Выполняет OCR на изображении PIL Image с опциональной предобработкой.

        Args:
            image: Исходное изображение PIL Image.
            details: Если True, возвращает список слов с bbox и уверенностью.
            image_processing_config: Конфигурация для предобработки изображения перед OCR.
            rectangle: Bbox (left, top, width, height) для установки области интереса в Tesseract.
            **params: Дополнительные параметры для движка (psm, whitelist, config_path, auto_orient_enabled etc.).

        Returns:
            Объект OCRResult, содержащий полный текст и (опционально) данные по словам.

        Raises:
            TesseractError: Если API не инициализирован или произошла ошибка OCR.
        """
        self._check_setup()

        start_time_total = time.perf_counter()

        processed_img = image.copy() # Начинаем с копии исходного изображения

        # Override default parameters with call-specific parameters (from **params)
        current_psm = int(params.get("psm", 3)) # Default to PSM_AUTO
        current_whitelist = params.get("whitelist", None) # Use None to indicate no override
        config_path = params.get("config_path", None)
        auto_orient_enabled = params.get("auto_orient_enabled", self._config.image_processing.auto_orient_enabled)

        # Указатели для освобождения памяти (итератор и текст)
        iterator = None
        text_ptr = None
        word_text_ptr = None

        try:
            # 1. Подготовка изображения данных для C API
            try:
                # Tesseract C API лучше работает с RGB или Greyscale.
                # Наш процессор может вернуть '1' (B&W). Конвертируем '1' в 'L' (Greyscale)
                # или 'RGB', так как PIL '1' mode может быть непрямо совместим с C API
                # ожидающим байты. Greyscale 'L' - хороший компромисс.
                if processed_img.mode == '1':
                     img_for_api = processed_img.convert("L") # Convert 1-bit B&W to 8-bit Greyscale
                     bytes_per_pixel = 1
                elif processed_img.mode == 'L':
                     img_for_api = processed_img # Use Greyscale directly
                     bytes_per_pixel = 1
                else: # Assume RGB or convert to it
                     img_for_api = processed_img.convert("RGB")
                     bytes_per_pixel = 3

                img_buffer = img_for_api.tobytes()
                img_width, img_height = img_for_api.size
                bytes_per_line = img_width * bytes_per_pixel

            except Exception as e:
                raise TesseractError(f"Failed to prepare image data for Tesseract API: {e}") from e


            # 2. Установка параметров Tesseract
            # Загружаем конфиг-файл, если указан
            if config_path:
                 self.load_config_file(config_path) # Вам нужно добавить метод load_config_file

            # Устанавливаем переменные (эти перекрывают настройки из конфиг-файла)
            if current_whitelist is not None:
                 if not self._set_variable("tesseract_char_whitelist", current_whitelist):
                    log.warning(f"Failed to set Tesseract variable 'tesseract_char_whitelist' to '{current_whitelist}'")

            if not self._set_variable("tessedit_pageseg_mode", str(current_psm)):
                 log.warning(f"Failed to set Tesseract variable 'tessedit_pageseg_mode' to '{current_psm}'")

            self._set_variable("user_words_suffix", "user-data")
            # Устанавливаем разрешение, если известно
            current_dpi = params.get("dpi", processed_img.info.get('dpi', (0, 0))[0]) # PIL DPI is tuple (x, y)
            if current_dpi and self._api and self._is_initialized:
                 # Убедитесь, что TessBaseAPISetSourceResolution портирована с корректной сигнатурой
                 if hasattr(self._lib, 'TessBaseAPISetSourceResolution'):
                    
                    self._lib.TessBaseAPISetSourceResolution(self._api, int(current_dpi))
                    log.debug(f"Set source resolution to {current_dpi} DPI.")
                 else:
                    log.warning("TessBaseAPISetSourceResolution not available in loaded Tesseract library.")


            # 3. Установка изображения в Tesseract API
            self._set_image(img_buffer, img_width, img_height, bytes_per_pixel, bytes_per_line)


            # 4. Установка области интереса (Rectangle), если указано
            if rectangle:
                 left, top, width, height = rectangle
                 # Basic validation
                 if 0 <= left < img_width and 0 <= top < img_height and \
                    width > 0 and height > 0 and \
                    left + width <= img_width and top + height <= img_height:
                     if hasattr(self._lib, 'TessBaseAPISetRectangle'):
                         self._lib.TessBaseAPISetRectangle(self._api, left, top, width, height)
                         log.debug(f"Set processing rectangle to: {rectangle}")
                     else:
                         log.warning("TessBaseAPISetRectangle not available in loaded Tesseract library.")
                 else:
                     log.warning(f"Invalid rectangle {rectangle} for image size {img_width}x{img_height}. Ignoring.")


            # 5. Явное выполнение распознавания
            log.debug("Starting Tesseract recognition...")
            recognition_start_time = time.perf_counter()
            # TessBaseAPIRecognize returns 0 on success
            recognition_result = self._lib.TessBaseAPIRecognize(self._api, None)
            recognition_time_ms = (time.perf_counter() - recognition_start_time) * 1000.0
            log.debug(f"Recognition finished in {recognition_time_ms:.2f} ms.")

            if recognition_result != 0:
                raise TesseractError(f"Tesseract recognition failed with code {recognition_result}.")


            # 6. Получение полного текста (по времени включается recognition)
            text_ptr = self._lib.TessBaseAPIGetUTF8Text(self._api) # Already includes recognition time if not called before

            full_text = ""
            if text_ptr:
                full_text_bytes = ctypes.string_at(text_ptr)
                full_text = full_text_bytes.decode('utf-8', errors='ignore').strip()
                # !!! Освобождаем память
                #self._lib.TessDeleteText(text_ptr)
                text_ptr = None # Устанавливаем в None для проверки в finally

            else:
                return None#log.warning("TesseractBaseAPIGetUTF8Text returned NULL.")


            # 7. Получение итератора, обход слов и bbox (если details=True)
            words: List[OCRWordResult] = []
            mean_conf: Optional[int] = None # Средняя уверенность
            
            if details:
                iterator = self._lib.TessBaseAPIGetIterator(self._api)
                
                if iterator:
                    log.debug("Iterating through words for details...")
                    left, top, right, bottom = ctypes.c_int(), ctypes.c_int(), ctypes.c_int(), ctypes.c_int()
                    print('0', full_text)
                    # TessResultIteratorNext returns True (non-zero) if successful
                    while self._lib.TessResultIteratorNext(iterator, self.TessPageIteratorLevel.RIL_WORD):
                        word_text_ptr = self._lib.TessResultIteratorGetUTF8Text(iterator, self.TessPageIteratorLevel.RIL_WORD)
                        word_text = ""
                        
                        if word_text_ptr:
                             word_text_bytes = ctypes.string_at(word_text_ptr)
                             word_text = word_text_bytes.decode('utf-8', errors='ignore').strip()
                             # !!! Освобождаем память
                             #self._lib.TessDeleteText(word_text_ptr)
                             word_text_ptr = None

                        bbox_success = self._lib.TessPageIteratorBoundingBox(
                            iterator, self.TessPageIteratorLevel.RIL_WORD,
                            ctypes.byref(left), ctypes.byref(top),
                            ctypes.byref(right), ctypes.byref(bottom)
                        )

                        word_conf: Optional[float] = None
                        # Убедимся, что функция Confidence портирована
                        if hasattr(self._lib, 'TessResultIteratorConfidence'):
                             word_conf = self._lib.TessResultIteratorConfidence(iterator, self.TessPageIteratorLevel.RIL_WORD)
                             word_conf = word_conf / 100.0 if word_conf >= 0 else -1.0


                        # Добавляем слово и его bbox в список
                        if bbox_success and word_text:
                            bbox_coords: Bbox = (left.value, top.value, right.value, bottom.value)
                            
                            log.debug(f"Creating OCRWordResult for text='{word_text[:30]}...' with confidence={word_conf} ")
                            words.append(OCRWordResult(text=word_text, bbox=bbox_coords, confidence=float(word_conf)))
                        elif word_text:
                            log.debug(f"Failed to get bounding box for word: '{word_text}'")


                    log.debug(f"Finished iterating through {len(words)} potential words.")

                    # Получаем среднюю уверенность для всего текста (только если детали запрошены и итератор был)
                    if hasattr(self._lib, 'TessBaseAPIMeanTextConf'):
                         mean_conf = self._lib.TessBaseAPIMeanTextConf(self._api)
                         log.debug(f"Mean text confidence: {mean_conf}%")
                    else:
                         log.warning("TessBaseAPIMeanTextConf not available in loaded Tesseract library.")

                else:
                     log.warning("TessBaseAPIGetIterator returned NULL. Cannot get word details.")


            # 8. Возвращаем результат
            time_total_ms = (time.perf_counter() - start_time_total) * 1000.0

            return OCRFrameResult( # КРИТИЧНОЕ ИЗМЕНЕНИЕ: Возвращаем OCRFrameResult
                full_text=full_text,
                words=words,
                mean_confidence=mean_conf,
                processing_time_ms=time_total_ms # Используем общее время для этого кадра
            )

        except TesseractError:
            raise # Re-raise TesseractError
        except Exception as e:
            log.error(f"Unexpected error during Tesseract processing: {e}", exc_info=True)
            raise TesseractError(f"An unexpected error occurred during processing: {e}") from e

        #finally:
            # 9. Освобождение ресурсов
            # Итератор, если он был создан
            #if iterator:
            #     self._lib.TessResultIteratorDelete(iterator)
            #     log.debug("Freed Tesseract result iterator.")

            # Указатели на текст (должны быть освобождены в теле try, но это запасной вариант)
            # if text_ptr:
            #      log.warning("Full text pointer not freed in try block!")
            #      self._lib.TessDeleteText(text_ptr)
            # if word_text_ptr:
            #      log.warning("Word text pointer not freed in try block!")
            #      self._lib.TessDeleteText(word_text_ptr)
            # if script_name_ptr: # Если вы портировали DetectOrientationScript
            #      log.warning("Script name pointer not freed in try block!")
            #      self._lib.TessDeleteText(script_name_ptr)


            # Очищаем внутреннее состояние Tesseract API
           # if self._api and self._is_initialized:
            #     self._lib.TessBaseAPIClear(self._api)
                 #log.debug("Tesseract API internal state cleared.")

    # --- Добавьте недостающие методы из capi.h, если еще не портированы ---
    # Например:
    def load_config_file(self, config_path: str) -> None:
        """Loads Tesseract variables from a config file."""
        self._check_setup()
        if not hasattr(self._lib, 'TessBaseAPIReadConfigFile'):
            log.warning("TessBaseAPIReadConfigFile not available in loaded Tesseract library. Cannot load config file.")
            return

        if not os.path.exists(config_path):
            log.warning(f"Tesseract config file not found at {config_path}")
            return

        config_path_bytes = config_path.encode('utf-8')
        log.info(f"Loading Tesseract config from: {config_path}")
        try:
            # TessBaseAPIReadConfigFile does not return success/failure indicator
            self._lib.TessBaseAPIReadConfigFile(self._api, config_path_bytes)
            log.debug(f"Config file '{config_path}' loaded successfully.")
        except Exception as e:
            log.error(f"Error loading Tesseract config file '{config_path}': {e}", exc_info=True)


    def _check_setup(self):
        """Внутренняя проверка инициализации."""
        if not self._lib:
            raise TesseractError('Tesseract library not loaded.')
        if not self._api:
            raise TesseractError('Tesseract API instance not created or initialized.')
        if not self._is_initialized:
             raise TesseractError('Tesseract API instance not fully initialized.')

    def _set_variable(self, key: str, value: str) -> bool:
        """
        Устанавливает параметр Tesseract API (внутренний).
        Возвращает True при успехе, False при неудаче.
        """
        self._check_setup() # Проверим инициализацию
        key_bytes = key.encode('utf-8')
        value_bytes = value.encode('utf-8')
        # SetVariable возвращает BOOL (int в C), 0 - неудача, non-zero - успех
        result = self._lib.TessBaseAPISetVariable(self._api, key_bytes, value_bytes)
        if result == 0: # C BOOL FALSE is 0
             log.warning(f"Failed to set Tesseract variable '{key}' to '{value}'")
             return False
        return True # C BOOL TRUE is non-zero

    def _set_image(self, imagedata: bytes, width: int, height: int,
                  bytes_per_pixel: int, bytes_per_line: Optional[int]=None):
        """Устанавливает изображение для распознавания (внутренний)."""
        self._check_setup()
        if bytes_per_line is None:
            bytes_per_line = width * bytes_per_pixel
        # Convert Python bytes to C void pointer
        imagedata_ptr = (ctypes.c_ubyte * len(imagedata)).from_buffer_copy(imagedata)

        self._lib.TessBaseAPISetImage(
            self._api,
            ctypes.cast(imagedata_ptr, ctypes.c_void_p), # Cast to void*
            width,
            height,
            bytes_per_pixel,
            bytes_per_line
        )
        # Note: imagedata_ptr is a local Python object; its memory is managed by Python GC.
        # Tesseract makes its own internal copy.

    def unload(self) -> None:
        """Освобождает ресурсы Tesseract API instance."""
        # Важно: unload вызывается кешем, когда экземпляр больше не нужен.
        # Он должен полностью очистить ресурсы ЭТОГО экземпляра API.
        if self._api: # Проверяем, что API instance существует
            log.info("Cleaning up Tesseract API instance.")
            if self._is_initialized:
                # Завершаем работу инициализированного API instance
                try:
                    # End should only be called if Init was successful
                    self._lib.TessBaseAPIEnd(self._api)
                    log.debug("TessBaseAPIEnd called.")
                except Exception as e:
                     log.error(f"Error calling TessBaseAPIEnd: {e}")

            # Удаляем сам API instance
            try:
                self._lib.TessBaseAPIDelete(self._api)
                log.debug("TessBaseAPIDelete called.")
            except Exception as e:
                 log.error(f"Error calling TessBaseAPIDelete: {e}")

            self._api = None # Устанавливаем в None, чтобы избежать повторной очистки
            self._is_initialized = False
            log.info("Tesseract API instance cleaned up.")
        else:
             log.debug("unload() called but Tesseract API instance was already cleaned up.")


    def __del__(self):
        """Деструктор как запасной вариант (не надежный)."""
        if self._api: # Проверяем только self._api, т.к. self._lib - это class variable
            log.warning("TesseractWrapper being garbage collected without explicit unload(). Potential resource leak.")
            self.unload()

    # Optional: Add context manager support
    def __enter__(self):
        self._check_setup()
        log.debug("Entering TesseractWrapper context.")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.unload()
        # Return False to propagate exceptions, or True to suppress
        return False # Propagate exceptions