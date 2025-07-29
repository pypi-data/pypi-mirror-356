"""
Единый «конверт» для ответов + вспомогательный make_response.
"""
from __future__ import annotations
import time
from typing import Any, Dict, List, Union, Optional
from sensory_detector.models.models import EnvelopeResponse, TaskType, DetectionSeries, OCRSeries, EmbeddingSeries

def make_response(
    task_type: TaskType,
    model_name: str,
    results_list: Union[List[Any], Any], # Может быть списком результатов на уровне кадра, или одной серией, если она уже структурирована
    started_at: float,
    message: str | None = None,
    total_items_processed: Optional[int] = None, # Добавлено для упрощения создания серии
    total_processing_time_ms: Optional[float] = None, # Добавлено для серии
) -> Dict:
    """
    Создает стандартизированный ответ API с использованием модели EnvelopeResponse.

    Args:
        task_type: Тип выполненной задачи (например, DETECTION, OCR, EMBEDDING).
        model_name: Имя модели, используемой для задачи.
        results_list: Фактические данные полезной нагрузки на уровне кадра (например, List[ObjectDetectionResult], List[OCRFrameResult], List[EmbeddingFrameResult]).
                      Может также быть предварительно сформированным объектом Series или списком объектов Series.
        started_at: Временная метка (time.time()), когда началась обработка запроса.
        message: Необязательное дополнительное сообщение для ответа.
        total_items_processed: Общее количество обработанных элементов/кадров в серии.
        total_processing_time_ms: Общее время обработки для серии.

    Returns:
        Словарь, представляющий JSON-ответ, соответствующий схеме EnvelopeResponse.
    """
    overall_runtime_ms = round((time.time() - started_at) * 1000, 1)

    # Если results_list уже является Series или List[Series], используйте его напрямую
    if isinstance(results_list, (DetectionSeries, OCRSeries, EmbeddingSeries)):
        final_data = results_list
    elif isinstance(results_list, list) and results_list and \
         all(isinstance(r, (DetectionSeries, OCRSeries, EmbeddingSeries)) for r in results_list):
        final_data = results_list
    else:
        # В противном случае, оберните список результатов уровня кадра в объект Series
        # Нам нужно знать тип, чтобы выбрать правильную модель Series
        if task_type == TaskType.DETECTION:
            final_data = DetectionSeries(
                model_name=model_name,
                total_items=total_items_processed if total_items_processed is not None else len(results_list),
                total_processing_time_ms=total_processing_time_ms if total_processing_time_ms is not None else overall_runtime_ms, # Если не указано, используем общее время
                results=results_list # Ожидается List[ObjectDetectionResult]
            )
        elif task_type == TaskType.OCR:
            final_data = OCRSeries(
                model_name=model_name,
                total_items=total_items_processed if total_items_processed is not None else len(results_list),
                total_processing_time_ms=total_processing_time_ms if total_processing_time_ms is not None else overall_runtime_ms,
                results=results_list # Ожидается List[OCRFrameResult]
            )
        elif task_type == TaskType.EMBEDDING:
            final_data = EmbeddingSeries(
                model_name=model_name,
                total_items=total_items_processed if total_items_processed is not None else len(results_list),
                total_processing_time_ms=total_processing_time_ms if total_processing_time_ms is not None else overall_runtime_ms,
                results=results_list # Ожидается List[EmbeddingFrameResult]
            )
        else:
            raise ValueError(f"Unknown task type for series creation: {task_type}")

    return EnvelopeResponse(
        task_type=task_type,
        model_name=model_name,
        total_runtime_ms=overall_runtime_ms,
        data=final_data,
        message=message,
    ).model_dump()