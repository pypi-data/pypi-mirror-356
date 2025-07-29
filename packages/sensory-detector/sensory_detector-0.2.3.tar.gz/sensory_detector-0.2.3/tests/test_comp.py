import asyncio
import numpy as np
import matplotlib
# Явно указываем Matplotlib использовать бэкенд 'Agg' перед импортом pyplot.
# 'Agg' предназначен для создания изображений в файл без GUI.
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import logging
from pathlib import Path
from typing import List, Tuple

# Импортируем наш клиент и модели данных
from sensory_detector.yolo_client.client import SensoryAPIClient
from sensory_detector.models.models import EmbeddingSeries, EmbeddingFrameResult

# Настройка логирования для клиента
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

def calculate_cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """Вычисляет косинусное сходство между двумя векторами."""
    np_vec1 = np.array(vec1)
    np_vec2 = np.array(vec2)
    
    dot_product = np.dot(np_vec1, np_vec2)
    norm_vec1 = np.linalg.norm(np_vec1)
    norm_vec2 = np.linalg.norm(np_vec2)
    
    if norm_vec1 == 0 or norm_vec2 == 0:
        return 0.0 # Избегаем деления на ноль для нулевых векторов
    
    return dot_product / (norm_vec1 * norm_vec2)

def calculate_dissimilarity(cosine_similarity: float) -> float:
    """
    Преобразует косинусное сходство (от -1 до 1) в шкалу несхожести (от 0 до 100).
    0 = идентичные, 100 = максимально не похожи.
    """
    # Clamp cosine_similarity to be within [-1, 1] to handle potential floating point inaccuracies
    cosine_similarity = max(-1.0, min(1.0, cosine_similarity))
    return (1 - cosine_similarity) * 75

def moving_average(data: List[float], window_size: int) -> np.ndarray:
    """Применяет простое скользящее среднее к данным."""
    if window_size <= 1:
        return np.array(data)
    if not data:
        return np.array([])
    
    # Pad the data to handle edges
    # We want the smoothed value at point N to represent the average of N and window_size-1 points before it.
    # To avoid shifting the smoothed curve significantly, we can use 'same' mode which pads symmetrically
    # or pad manually for 'valid' mode. 'valid' mode returns only points where window fully overlaps.
    # Let's use 'valid' mode for clarity and mention it means the smoothed data is shorter.
    
    # Or, use 'full' and slice it for 'same' effect:
    # np.convolve(data, np.ones(window_size)/window_size, mode='same')
    # For now, let's stick with 'valid' as it's straightforward.
    
    # Ensure data is numpy array for convolution
    data_np = np.array(data)
    weights = np.ones(window_size) / window_size
    return np.convolve(data_np, weights, mode='valid')


async def main():
    # Используйте ваш IP и порт
    client = SensoryAPIClient(base_url="http://10.10.0.128:8000") # Используйте ваш IP и порт
    
    # Путь к тестовому видео.
    # Если вы монтируете ./tests/data в контейнер как /app/data,
    # то для сервера путь будет /app/data/test.avi
    video_filename = "padington_1_min.mp4" # Имя видеофайла, которое будет использоваться в имени графика
    video_path_on_server = f"/data/AromaBank/{video_filename}" # Ваш путь к видео
    
    
    # Параметр для сглаживания: размер окна скользящего среднего
    # Чем больше значение, тем сильнее сглаживание. Поэкспериментируйте.
    smoothing_window_size = 25 
    
    log.info(f"Начинаем извлечение эмбеддингов для видео: {video_path_on_server}")
    
    try:
        results: EmbeddingSeries | List[EmbeddingSeries] = await client.get_embeddings(
            images=video_path_on_server,
            model_name="clip-base",
            path_mode=True
        )

        # get_embeddings для одиночного видеофайла должен вернуть один EmbeddingSeries
        if isinstance(results, list):
            if not results:
                log.error("Сервис вернул пустой список результатов для видео.")
                return
            log.warning("Сервис вернул список результатов, ожидался один. Используем первый.")
            video_series = results[0]
        else:
            video_series = results

        if not video_series.results:
            log.warning(f"Не удалось получить результаты эмбеддингов для видео: {video_path_on_server}. Возможно, видео пустое или нечитаемо.")
            return

        log.info(f"Получено {len(video_series.results)} эмбеддингов кадров.")
        log.info("Начинаем расчет несхожести между соседними кадрами...")

        dissimilarity_scores: List[float] = []
        labels: List[str] = [] # Кадры (индексы) для меток на оси X

        # Сравниваем соседние кадры
        for i in range(len(video_series.results) - 1):
            frame1_result = video_series.results[i]
            frame2_result = video_series.results[i+1]

            if not frame1_result.embedding or not frame2_result.embedding:
                log.warning(f"Пропущены кадры {frame1_result.frame_index} и {frame2_result.frame_index} из-за отсутствия эмбеддингов.")
                continue

            sim = calculate_cosine_similarity(frame1_result.embedding, frame2_result.embedding)
            dissim = calculate_dissimilarity(sim)
            dissimilarity_scores.append(dissim)
            
            # Сохраняем индекс начала пары кадров для меток
            labels.append(str(frame1_result.frame_index)) 
            
            log.debug(f"Кадр {frame1_result.frame_index} vs {frame2_result.frame_index}: Сходство={sim:.4f}, Несхожесть={dissim:.2f}")

        if not dissimilarity_scores:
            log.warning("Недостаточно кадров для сравнения или все сравнения пропущены.")
            return

        log.info("Расчет несхожести завершен. Начинаем построение графика.")
        
        # Применяем сглаживание
        smoothed_dissimilarity = moving_average(dissimilarity_scores, smoothing_window_size)
        
        # Определяем диапазон для сглаженных данных (они короче из-за mode='valid')
        smoothed_x_range = np.arange(len(smoothed_dissimilarity)) + (smoothing_window_size - 1) / 2
        
        # Построение графика
        # Увеличиваем размер фигуры для лучшей читаемости при большом количестве точек
        plt.figure(figsize=(20, 8)) # Шире, чем раньше
        
        # 1. График несглаженных данных (тонкая линия, светлый цвет)
        plt.plot(dissimilarity_scores, linestyle='-', color='gray', alpha=0.7, linewidth=1, label='Исходная несхожесть (покадрово)')

        # 2. График сглаженных данных (толстая линия, выразительный цвет)
        plt.plot(smoothed_x_range, smoothed_dissimilarity, linestyle='-', color='red', linewidth=2, label=f'Сглаженная несхожесть (окно {smoothing_window_size})')
        
        plt.title(f'Динамика несхожести соседних кадров для {video_filename} (Всего кадров: {len(video_series.results)})')
        plt.xlabel('Индекс начального кадра пары (N)')
        plt.ylabel('Несхожесть (0 = идентичные, 100 = максимально не похожи)')
        
        # Адаптивные метки на оси X: показываем только небольшое количество меток
        # Выбираем количество меток для отображения, например, не более 10-15
        num_labels_to_show = 15
        if len(labels) > num_labels_to_show:
            step = len(labels) // (num_labels_to_show - 1)
            # Убедимся, что step не 0
            if step == 0: step = 1
            
            # Выбираем индексы и соответствующие им метки
            x_ticks_indices = np.arange(0, len(labels), step)
            x_tick_labels = [labels[i] for i in x_ticks_indices]
            
            # Добавляем последнюю метку, если она не была включена
            if len(labels) - 1 not in x_ticks_indices and len(labels) > 0:
                x_ticks_indices = np.append(x_ticks_indices, len(labels) - 1)
                x_tick_labels.append(labels[-1])
            
            plt.xticks(x_ticks_indices, x_tick_labels, rotation=45, ha='right', fontsize=9)
        else:
            plt.xticks(range(len(labels)), labels, rotation=45, ha='right', fontsize=9)


        plt.grid(True, linestyle='--', alpha=0.7)
        plt.ylim(-5, 25) # Шкала от 0 до 100 с небольшими отступами
        plt.legend(loc='upper right') # Размещаем легенду
        plt.tight_layout() # Автоматически регулирует параметры подграфика для плотной компоновки
        
        # --- Изменения для сохранения файла ---
        output_dir = Path(__file__).parent if '__file__' in locals() else Path.cwd()
        plot_filename = f"dissimilarity_plot_{Path(video_filename).stem}_smoothed.png"
        output_path = output_dir / plot_filename
        
        log.info(f"Попытка сохранения графика в: {output_path}")
        try:
            plt.savefig(output_path, dpi=300) # Увеличиваем DPI для лучшего качества
            log.info(f"График успешно сохранен в: {output_path}")
        except Exception as save_e:
            log.error(f"Ошибка при сохранении графика в {output_path}: {save_e}", exc_info=True)
        finally:
            plt.close() # Важно закрыть фигуру Matplotlib после сохранения, чтобы освободить память

    except FileNotFoundError as e:
        log.error(f"Ошибка: Файл не найден на сервере. Проверьте путь и монтирование томов: {e}")
    except Exception as e:
        log.error(f"Произошла ошибка при обработке видео: {e}", exc_info=True)

if __name__ == "__main__":
    asyncio.run(main())

