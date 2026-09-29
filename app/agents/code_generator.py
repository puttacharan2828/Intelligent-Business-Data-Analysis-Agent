def generate_code(plan):
    analysis_type = plan["analysis_type"]
    target_column = plan["target_column"]
    group_by = plan.get("group_by")
    operation = plan.get("operation")
    filter_condition = plan.get("filter")
    time = plan.get("time")

    data = "df"

    # Apply filter
    if filter_condition is not None:
        filter_column = filter_condition["column"]
        filter_value = filter_condition["value"]

        data = f'df[df["{filter_column}"] == "{filter_value}"]'

    # Apply time filter
    if time is not None:
        data = f'{data}[df["Year"] == {time}]'

    if analysis_type == "summary":
        return f'{data}["{target_column}"].describe()'

    elif analysis_type == "distribution":
        return f'{data}["{target_column}"].describe()'

    elif analysis_type == "aggregation":

        if group_by is not None:
            if operation == "sum":
                return f'{data}.groupby("{group_by}")["{target_column}"].sum()'

            elif operation == "mean":
                return f'{data}.groupby("{group_by}")["{target_column}"].mean()'

            elif operation == "min":
                return f'{data}.groupby("{group_by}")["{target_column}"].min()'

            elif operation == "max":
                return f'{data}.groupby("{group_by}")["{target_column}"].max()'

            elif operation == "count":
                return f'{data}.groupby("{group_by}")["{target_column}"].count()'

        else:
            if operation == "sum":
                return f'{data}["{target_column}"].sum()'

            elif operation == "mean":
                return f'{data}["{target_column}"].mean()'

            elif operation == "min":
                return f'{data}["{target_column}"].min()'

            elif operation == "max":
                return f'{data}["{target_column}"].max()'

            elif operation == "count":
                return f'{data}["{target_column}"].count()'

        raise ValueError("Unsupported aggregation operation.")

    elif analysis_type == "relationship":
        if group_by is None:
            raise ValueError("Relationship analysis requires two columns.")

        return f'{data}[["{target_column}", "{group_by}"]].corr()'

    else:
        raise ValueError("Unsupported analysis type.")