def validate_analysis_plan(plan):
    if plan.analysis_type is None:
        return False

    if plan.analysis_type == "grouped_aggregation":
        if plan.target_column is None or plan.group_by is None:
            return False

    if plan.analysis_type == "aggregation":
        if plan.target_column is None or plan.operation is None:
            return False

    valid_types = [
        "aggregation",
        "grouped_aggregation",
        "comparison",
        "trend",
        "distribution",
        "relationship",
        "summary"
    ]

    if plan.analysis_type not in valid_types:
        return False

    return True