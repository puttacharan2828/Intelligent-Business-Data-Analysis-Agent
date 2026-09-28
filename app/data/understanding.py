from .profiler import profile_dataset
from .numerical import analyze_numerical_columns
from .categorical import analyze_categorical_columns
from .quality import check_data_quality
from .classifier import classify_columns


def understand_dataset(df):
    understanding = {
        "profile": profile_dataset(df),
        "numerical_analysis": analyze_numerical_columns(df),
        "categorical_analysis": analyze_categorical_columns(df),
        "quality": check_data_quality(df),
        "column_classification": classify_columns(df)
    }

    return understanding