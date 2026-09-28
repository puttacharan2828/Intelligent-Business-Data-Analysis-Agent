def analyze_categorical_columns(df):
    categorical_df = df.select_dtypes(include=["object", "string", "category"])

    analysis = {}

    for column in categorical_df.columns:
        analysis[column] = {
            "unique_values": categorical_df[column].nunique(),
            "value_counts": categorical_df[column].value_counts().to_dict()
        }

    return analysis