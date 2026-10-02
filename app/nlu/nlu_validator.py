def validate_nlu(parsed_result, columns):
    errors = []

    if parsed_result["intent"] == "unknown":
        errors.append("Could not understand the question intent.")

    if parsed_result["metric"] is None:
        errors.append("Metric is missing.")

    if parsed_result["group_by"] is None and any(
        word in parsed_result["question"].lower()
        for word in ["by", "per", "each"]
    ):
        errors.append("Grouping column is missing.")

    if parsed_result["intent"] == "aggregation":
        if parsed_result["operation"] is None:
            errors.append("Aggregation operation is missing.")

    if parsed_result["group_by"] is not None:
        if parsed_result["group_by"] not in columns:
            errors.append("Group-by column not found in dataset.")

    if parsed_result["filters"] is not None:
        filter_column = parsed_result["filters"]["column"]

        if filter_column not in columns:
            errors.append("Filter column not found in dataset.")

    return {
        "valid": len(errors) == 0,
        "errors": errors
    }

