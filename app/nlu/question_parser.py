from .intent_detector import detect_intent
from .entity_extractor import (
    extract_metric,
    extract_group_by,
    extract_operation,
    extract_filter,
    extract_time
)

def parse_question(question, columns):
    intent = detect_intent(question)
    metric = extract_metric(question, columns)
    group_by = extract_group_by(question, columns)
    operation = extract_operation(question)
    filter_condition = extract_filter(question, columns)
    time = extract_time(question)

    return {
        "intent": intent,
        "metric": metric,
        "operation": operation,
        "group_by": group_by,
        "filters": filter_condition,
        "time": time
    }
