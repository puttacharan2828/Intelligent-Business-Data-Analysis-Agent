ANALYSIS_TYPES = {
    "aggregation": "aggregation",
    "comparison": "comparison",
    "trend": "trend",
    "distribution": "distribution",
    "relationship": "relationship",
    "summary": "summary",
    "unknown": "unknown"
}


def determine_analysis_type(intent, group_by=None):

    if intent == "aggregation":
        if group_by:
            return "grouped_aggregation"

        return "aggregation"

    return ANALYSIS_TYPES.get(intent, "unknown")