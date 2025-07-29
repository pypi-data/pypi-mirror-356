"""
Мини-тест синхронного клиента Sensory Detector API.
Запускайте после поднятия сервера, например, через Docker Compose:

    poetry run python tests/test_sync_client_script.py
"""

from pathlib import Path
from typing import List, Union, Tuple, Mapping, Any

# Импортируем синхронный клиент
from sensory_detector.yolo_client.client import SensoryAPIClientSync

# Импортируем модели ответов для типизации и более удобной работы
from sensory_detector.models.models import (
    ModelsResponse,
    CacheStatsResponse,
    UnloadModelResponse,
    EnvelopeResponse, # Включаем EnvelopeResponse, хотя клиент его обрабатывает внутри
    DetectionSeries,
    OCRSeries,
    EmbeddingSeries,
    ObjectDetectionResult, # Frame-level result, может понадобиться для проверки деталей
    OCRFrameResult,        # Frame-level result
    EmbeddingFrameResult   # Frame-level result
)

# ──────────────────  КОНФИГУРАЦИЯ  ──────────────────
SERVER_URL = "http://localhost:8003" # Убедитесь, что сервер запущен на этом адресе

# --- Пути к локальным тестовым файлам (для загрузки на сервер - upload mode) ---
# Эти пути должны быть доступны на машине, с которой запускается данный скрипт.
LOCAL_TEST_IMAGE_PATH = Path("/home/fox/Services/Yolo/src/sensory_detector/yolo_server/detectors/tesseract_wrapper/tmp.png").resolve() 
LOCAL_TEST_VIDEO_PATH = Path("/mnt/nfs/servers/AromaBank/f&f.mp4").resolve()

# Дополнительные изображения из тестовой папки проекта (для разнообразия в батч-запросах)
# Используем ту же картинку, как было запрошено в исходном коде пользователя
ADDITIONAL_LOCAL_IMAGE_JPG = str(LOCAL_TEST_IMAGE_PATH)
ADDITIONAL_LOCAL_IMAGE_PNG = str(LOCAL_TEST_IMAGE_PATH)


SERVER_PATH_FOR_IMAGE = LOCAL_TEST_IMAGE_PATH # ПРИМЕР! Адаптируйте под вашу конфигурацию Docker volume.
SERVER_PATH_FOR_VIDEO = "/data/AromaBank/f&f.mp4" # ПРИМЕР! Адаптируйте под вашу конфигурацию Docker volume.
#SERVER_PATH_FOR_VIDEO = '/mnt/nfs/servers/AromaBank/f&f.mp4'

# Пример ROI (Region of Interest) - ((x1, y1), (x2, y2))
TEST_ROI: Union[Tuple[Tuple[int, int], Tuple[int, int]], None] = ((100, 100), (400, 300))
# TEST_ROI = None # Используйте эту строку, если не хотите применять ROI
# Ключи соответствуют полям OCRImageProcessingConfig (используются для всех задач).
DEFAULT_PROC_CFG = {
    'enabled':False,
    'resize_enabled':True,
    'resize_mode':"scale_factor",
    'resize_scale_factor': 1,
    'resize_filter':"LANCZOS",
    'borders_enabled':True,
    'border_size':20,
    'background_processing_enabled':True,
    'background_lightness_threshold':100,
    'bw_threshold':110,
    'background_sample_size':100,
    'auto_orient_enabled':True
}

# Инициализация синхронного клиента API
client = SensoryAPIClientSync(SERVER_URL)

# Тест 3.2: Множество локальных JPG/PNG (upload) с моделью 'easyocr' без детализации
print("\n--- Тест 3.2: Множество локальных JPG/PNG (upload) с моделью 'easyocr' без детализации ---")
try:
    # Ожидаем `List[OCRSeries]` для списка файлов
    result_list: List[OCRSeries] = client.recognize_texts(
        images=[LOCAL_TEST_IMAGE_PATH, ADDITIONAL_LOCAL_IMAGE_PNG], # Список путей
        model_name="easyocr",
        details=False, # Отключить детализацию
        proc_cfg=DEFAULT_PROC_CFG,
        path_mode=False
    )
    print(f"  [УСПЕХ] OCR для {result_list} изображений (каждая в своей серии).")
    for i, series in enumerate(result_list): # Итерируемся по сериям
        # Каждая серия содержит список результатов по кадрам (здесь 1 кадр на серию)
        print(f"    - Серия {i+1}: '{series}' (детализация: {series is not None})")
except Exception as e:
    print(f"  [ОШИБКА] В Тесте 3.2: {e}")


# ──────────────────  ОБЩИЕ ЭНДПОИНТЫ (СТАТУС СЕРВЕРА)  ──────────────────
print("\n" + "="*80)
print("                   ОБЩИЕ ЭНДПОИНТЫ: СТАТУС СЕРВЕРА                   ")
print("="*80 + "\n")

print("\n--- Проверка доступных моделей (/api/available_models) ---")
try:
    available_models: ModelsResponse = client.get_available_models()
    print(f"  Получен список доступных моделей:\n{available_models.model_dump_json(indent=2)}")
except Exception as e:
    print(f"  [ОШИБКА] При получении доступных моделей: {e}")

print("\n--- Проверка загруженных моделей (/api/loaded_models) ---")
try:
    loaded_models: List[CacheStatsResponse] = client.get_loaded_models()
    if loaded_models:
        print("  Текущий статус кэша моделей:")
        for model_stat in loaded_models:
            print(f"    - Модель: {model_stat.model_name} | Задача: {model_stat.task_type} | "
                  f"Используется: {model_stat.use_count} раз | Простаивает: {model_stat.idle_seconds:.1f} сек")
    else:
        print("  В кэше нет загруженных моделей.")
except Exception as e:
    print(f"  [ОШИБКА] При получении загруженных моделей: {e}")


# ──────────────────  ТЕСТИРОВАНИЕ API: /api/embeddings (CLIP Embeddings)  ──────────────────
print("\n" + "="*80)
print("               ТЕСТИРОВАНИЕ API ЭНДПОИНТА: /api/embeddings              ")
print("                  (Генерация эмбеддингов с CLIP)                      ")
print("="*80 + "\n")

# Тест 1.1: Единичный локальный JPG (upload) с моделью по умолчанию
print("\n--- Тест 1.1: Единичный локальный JPG (upload) ---")
try:
    # Специальные настройки препроцессинга для CLIP (часто 224x224)
    clip_proc_cfg = DEFAULT_PROC_CFG.copy()
    clip_proc_cfg['resize_target_dim'] = 224

    # Ожидаем `EmbeddingSeries` для одиночного файла/байтов
    result: EmbeddingSeries = client.get_embeddings(
        model_name='clip-base', # Или 'clip-ViT-B-32-laion2b_s34b_b79k'
        images=LOCAL_TEST_IMAGE_PATH, # Это одиночный путь, клиент вернет EmbeddingSeries
        proc_cfg=clip_proc_cfg,
        path_mode=False
    )
    # Доступ к данным теперь через .results[0]
    print(f"  [УСПЕХ] Эмбеддинг для '{LOCAL_TEST_IMAGE_PATH}': {len(result)} измерений.")
except Exception as e:
    print(f"  [ОШИБКА] В Тесте 1.1: {e}")

# Тест 1.2: Множество локальных JPG/PNG (upload) с указанием модели и ROI
print("\n--- Тест 1.2: Множество локальных JPG/PNG (upload) с моделью и ROI ---")
try:
    # Ожидаем `List[EmbeddingSeries]` для списка файлов
    result_list: List[EmbeddingSeries] = client.get_embeddings(
        images=[LOCAL_TEST_IMAGE_PATH, ADDITIONAL_LOCAL_IMAGE_JPG], # Список путей
        model_name="clip-base", # Укажем конкретную модель
        roi=TEST_ROI,
        proc_cfg=clip_proc_cfg,
        path_mode=False
    )
    print(f"  [УСПЕХ] Эмбеддинги для {len(result_list)} изображений (каждая в своей серии).")
    for i, series in enumerate(result_list): # Итерируемся по сериям
        # Каждая серия содержит список результатов по кадрам (здесь 1 кадр на серию)
        print(f"    - Серия {i+1} (модель: {series.model_name})")
except Exception as e:
    print(f"  [ОШИБКА] В Тесте 1.2: {e}")

# Тест 1.3: Серверное видео (path_mode) с препроцессингом и пользовательской моделью
print("\n--- Тест 1.3: Серверное видео (path_mode) с препроцессингом и моделью ---")
try:
    # Убедитесь, что SERVER_PATH_FOR_VIDEO реально доступен на сервере!
    # Ожидаем `EmbeddingSeries` для одиночного видео
    result_series: EmbeddingSeries = client.get_embeddings(
        images=SERVER_PATH_FOR_VIDEO, # Одиночный путь к видео, клиент вернет EmbeddingSeries
        model_name="clip-base", # Другая модель CLIP
        proc_cfg=clip_proc_cfg,
        path_mode=True
    )
    print(f"  [УСПЕХ] Эмбеддинги для видео '{SERVER_PATH_FOR_VIDEO}'")
    if result_series:
        print(f"    - Пример первого эмбеддинга (модель: {result_series.model_name}, размер: {result_series})")
except Exception as e:
    print(f"  [ОШИБКА] В Тесте 1.3 (проверьте SERVER_PATH_FOR_VIDEO и доступность на сервере): {e}")

# Тест 1.4: Единичный JPG в байтах (upload) с ROI
print("\n--- Тест 1.4: Единичный JPG в байтах (upload) с ROI ---")
try:
    image_bytes = Path(LOCAL_TEST_IMAGE_PATH).read_bytes() # Используем вашу картинку в байтах
    # Ожидаем `EmbeddingSeries` для одиночных байтов
    result: EmbeddingSeries = client.get_embeddings(
        model_name="clip-base", # Укажем конкретную модель
        images=image_bytes,
        roi=((0, 0), (150, 150)), # Специфичный ROI для этого теста
        proc_cfg=clip_proc_cfg,
        path_mode=False
    )
    # Доступ к данным теперь через .results[0]
    print(f"  [УСПЕХ] Эмбеддинг для JPG в байтах с ROI: {len(result)} измерений. Модель: {result}")
except Exception as e:
    print(f"  [ОШИБКА] В Тесте 1.4: {e}")


# ──────────────────  ТЕСТИРОВАНИЕ API: /api/objects (Object Detection)  ──────────────────
print("\n" + "="*80)
print("               ТЕСТИРОВАНИЕ API ЭНДПОИНТА: /api/objects                ")
print("                    (Детекция объектов с YOLO)                         ")
print("="*80 + "\n")

# Тест 2.1: Единичный локальный PNG (upload) с моделью по умолчанию
print("\n--- Тест 2.1: Единичный локальный PNG (upload) ---")
try:
    # Настройки препроцессинга для YOLO (обычно 640x640)
    yolo_proc_cfg = DEFAULT_PROC_CFG.copy()
    yolo_proc_cfg['resize_target_dim'] = 640

    # Ожидаем `DetectionSeries` для одиночного файла
    result: DetectionSeries = client.detect_objects(
        model_name="yolov8s", # Укажем YOLOv8s
        images=LOCAL_TEST_IMAGE_PATH, # Одиночный путь
        proc_cfg=yolo_proc_cfg,
        path_mode=False
    )
    # Доступ к данным теперь через .results[0]
    print(f"  [УСПЕХ] Обнаружения для '{LOCAL_TEST_IMAGE_PATH}': Найдено {len(result.results)} объектов на первом кадре. Модель: {result}")
except Exception as e:
    print(f"  [ОШИБКА] В Тесте 2.1: {e}")

# Тест 2.2: Множество локальных JPG/PNG (upload) с указанием модели и ROI
print("\n--- Тест 2.2: Множество локальных JPG/PNG (upload) с моделью и ROI ---")
try:
    # Ожидаем `List[DetectionSeries]` для списка файлов
    result_list: List[DetectionSeries] = client.detect_objects(
        images=[LOCAL_TEST_IMAGE_PATH, ADDITIONAL_LOCAL_IMAGE_PNG], # Список путей
        model_name="yolov8s", # Укажем YOLOv8s
        roi=TEST_ROI,
        proc_cfg=yolo_proc_cfg,
        path_mode=False
    )
    print(f"  [УСПЕХ] Обнаружения для {result_list} изображений (каждая в своей серии).")
    for i, series in enumerate(result_list): # Итерируемся по сериям
        # Каждая серия содержит список результатов по кадрам (здесь 1 кадр на серию)
        print(f"    - Серия {i+1} (модель: {series})"
              f"Кадр 0: {len(series)} объектов.")
except Exception as e:
    print(f"  [ОШИБКА] В Тесте 2.2: {e}")

# Тест 2.3: Серверное видео (path_mode) с ROI
print("\n--- Тест 2.3: Серверное видео (path_mode) с ROI ---")
try:
    # Убедитесь, что SERVER_PATH_FOR_VIDEO реально доступен на сервере!
    # Ожидаем `DetectionSeries` для одиночного видео
    result_series: DetectionSeries = client.detect_objects(
        model_name="yolov8s",
        images=SERVER_PATH_FOR_VIDEO,
        roi=TEST_ROI,
        proc_cfg=DEFAULT_PROC_CFG, # Preprocessing also applies to video frames
        path_mode=True
    )
    print(f"  [УСПЕХ] Обнаружения для видео '{SERVER_PATH_FOR_VIDEO}': {(result_series.results)} кадров обработано.")
    if result_series: # Проверяем, есть ли результаты по кадрам
        print(f"    - Пример первого кадра из видео (модель: {result_series.model_name}): "
              f"Найдено {result_series} объектов.")
except Exception as e:
    print(f"  [ОШИБКА] В Тесте 2.3 (проверьте SERVER_PATH_FOR_VIDEO и доступность на сервере): {e}")
    
# Тест 2.4: Единичный JPG в байтах (upload) с пользовательским ROI
print("\n--- Тест 2.4: Единичный JPG в байтах (upload) с пользовательским ROI ---")
try:
    image_bytes = Path(LOCAL_TEST_IMAGE_PATH).read_bytes() # Используем вашу картинку в байтах
    # Ожидаем `DetectionSeries` для одиночных байтов
    result: DetectionSeries = client.detect_objects(
        model_name="yolov8s", # Укажем YOLOv8s
        images=image_bytes,
        roi=((0, 0), (100, 100)), # Очень маленький ROI
        proc_cfg=yolo_proc_cfg,
        path_mode=False
    )
    # Доступ к данным теперь через .results[0]
    print(f"  [УСПЕХ] Обнаружения для JPG в байтах с ROI: Найдено {result} объектов.")
except Exception as e:
    print(f"  [ОШИБКА] В Тесте 2.4: {e}")


# ──────────────────  ТЕСТИРОВАНИЕ API: /api/texts (OCR Text Recognition)  ──────────────────
print("\n" + "="*80)
print("               ТЕСТИРОВАНИЕ API ЭНДПОИНТА: /api/texts                 ")
print("                     (Распознавание текста OCR)                         ")
print("="*80 + "\n")

# Тест 3.1: Единичный локальный JPG (upload) с моделью 'tess' и полной детализацией
print("\n--- Тест 3.1: Единичный локальный JPG (upload) с моделью 'tess' и детализацией ---")
try:
    # Настройки препроцессинга для OCR (например, можно отключить ресайз, если OCR сам ресайзит)
    ocr_proc_cfg = DEFAULT_PROC_CFG.copy()
    ocr_proc_cfg['resize_enabled'] = False # Некоторые OCR модели предпочитают исходный размер
    ocr_proc_cfg['background_processing_enabled'] = True # Специфично для OCR

    # Ожидаем `OCRSeries` для одиночного файла
    result: OCRSeries = client.recognize_texts(
        images=LOCAL_TEST_IMAGE_PATH, # Одиночный путь
        model_name="tess",
        details=True, # Включить детализацию по словам
        proc_cfg=ocr_proc_cfg,
        path_mode=False
    )
    # Доступ к данным теперь через .results[0]
    print(f"  [УСПЕХ] OCR для '{LOCAL_TEST_IMAGE_PATH}' (tess, details=True): Распознано '{result.results[0].full_text}'")
    if result.results[0].words: # Доступ к деталям слов
        print(f"    - Пример первых 3-х деталей слов: {[d.model_dump() for d in result.results[0].words[:3]]}")
    else:
        print("    - Детализация слов не получена (возможно, текст не найден или модель не вернула).")
except Exception as e:
    print(f"  [ОШИБКА] В Тесте 3.1: {e}")


# Тест 3.3: Серверное видео (path_mode) с ROI и препроцессингом для OCR
print("\n--- Тест 3.3: Серверное видео (path_mode) с ROI и препроцессингом ---")
try:
    # Убедитесь, что SERVER_PATH_FOR_VIDEO реально доступен на сервере!
    # Ожидаем `OCRSeries` для одиночного видео
    #SERVER_TEST_VIDEO_PATH = Path().resolve()
    result_series: OCRSeries = client.recognize_texts(
        model_name="easyocr",
        images=SERVER_PATH_FOR_VIDEO,
        roi=TEST_ROI,
        proc_cfg=DEFAULT_PROC_CFG,
        path_mode=True
    )
    print(f"  [УСПЕХ] OCR для видео '{SERVER_PATH_FOR_VIDEO}': {result_series} кадров обработано.")
    if result_series.results:
        print(f"    - Пример текста из первого кадра видео (модель: {result_series.model_name}): '{result_series.results[0].full_text}'")
except Exception as e:
    print(f"  [ОШИБКА] В Тесте 3.3 (проверьте SERVER_PATH_FOR_VIDEO и доступность на сервере): {e}")



# Тест 3.4: Единичный JPG в байтах (upload) с ROI без детализации
print("\n--- Тест 3.4: Единичный JPG в байтах (upload) с ROI без детализации ---")
try:
    image_bytes = Path(LOCAL_TEST_IMAGE_PATH).read_bytes() # Используем вашу картинку в байтах
    # Ожидаем `OCRSeries` для одиночных байтов
    result: OCRSeries = client.recognize_texts(
        model_name="easyocr",
        images=image_bytes,
        roi=((20, 20), (100, 80)), # Очень специфичный ROI
        details=False,
        proc_cfg=ocr_proc_cfg,
        path_mode=False
    )
    # Доступ к данным теперь через .results[0]
    print(f"  [УСПЕХ] OCR для JPG в байтах с ROI (details=False): Распознано '{result.results[0].full_text}'")
except Exception as e:
    print(f"  [ОШИБКА] В Тесте 3.4: {e}")

# ──────────────────  УПРАВЛЕНИЕ МОДЕЛЯМИ  ──────────────────
print("\n" + "="*80)
print("             УПРАВЛЕНИЕ МОДЕЛЯМИ (/api/unload_model/{name})           ")
print("="*80 + "\n")

# Пример выгрузки модели (например, yolov8s)
# Важно: если модель не была загружена, этот запрос вызовет 404 ошибку.
UNLOAD_MODEL_NAME = "yolov8s" # Замените на имя модели, которую хотите выгрузить

print(f"\n--- Попытка выгрузить модель '{UNLOAD_MODEL_NAME}' ---")
try:
    unload_response: UnloadModelResponse = client.unload_model(UNLOAD_MODEL_NAME)
    print(f"  [УСПЕХ] Выгрузка модели '{UNLOAD_MODEL_NAME}': {unload_response.detail}")
    # После выгрузки, можно снова проверить загруженные модели
    print("\n--- Проверка загруженных моделей после попытки выгрузки ---")
    loaded_models_after_unload: List[CacheStatsResponse] = client.get_loaded_models()
    if loaded_models_after_unload:
        print("  Текущий статус кэша моделей:")
        for model_stat in loaded_models_after_unload:
            print(f"    - Модель: {model_stat.model_name} | Задача: {model_stat.task_type} | "
                  f"Используется: {model_stat.use_count} раз | Простаивает: {model_stat.idle_seconds:.1f} сек")
    else:
        print("  В кэше нет загруженных моделей.")
except Exception as e:
    print(f"  [ОШИБКА] При выгрузке модели '{UNLOAD_MODEL_NAME}': {e}")


print("\n" + "="*80)
print("                   Все синхронные тесты завершены.                    ")
print("="*80 + "\n")