def check_data_quality(df):
    quality = {
        "missing_values": df.isnull().sum().to_dict(),
        "duplicate_rows": df.duplicated().sum(),
        "empty_columns": [],
        "constant_columns": []
    }

    for column in df.columns:

        if df[column].isnull().all():
            quality["empty_columns"].append(column)

        if df[column].nunique(dropna=False) <= 1:
            quality["constant_columns"].append(column)

    return quality