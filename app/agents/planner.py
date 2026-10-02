from app.agents.analysis_plan import AnalysisPlan
from app.agents.analysis_types import determine_analysis_type


def create_analysis_plan(nlu_result):
    intent = nlu_result["intent"]
    target_column = nlu_result["metric"]
    group_by = nlu_result["group_by"]
    operation = nlu_result["operation"]
    filter_condition = nlu_result["filters"]
    time = nlu_result["time"]

    analysis_type = determine_analysis_type(intent, group_by)

    plan = AnalysisPlan(
        analysis_type=analysis_type,
        target_column=target_column,
        group_by=group_by,
        operation=operation,
        filter=filter_condition,
        time=time
    )

    return plan
    analysis_type = determine_analysis_type(intent, group_by)

    plan = AnalysisPlan(
        analysis_type=analysis_type,
        target_column=target_column,
        group_by=group_by,
        operation=operation,
        filter=filter,
        time=time
    )

    return plan