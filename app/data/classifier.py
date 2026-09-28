def classify_columns(df):
    classification = {}

    for column in df.columns:

        if df[column].dtype == "bool":
            column_type = "boolean"

        elif df[column].dtype == "object":
            column_type = "categorical"

        elif df[column].dtype == "string":
            column_type = "categorical"

        elif df[column].dtype == "category":
            column_type = "categorical"

        elif str(df[column].dtype).startswith("datetime"):
            column_type = "datetime"

        elif str(df[column].dtype).startswith(("int", "float")):
            column_type = "numerical"

        else:
            column_type = "other"

        classification[column] = column_type

    return classification