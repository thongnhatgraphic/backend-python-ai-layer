import pandas as pd
from ai_native.ML_foundation.data_visualization.mini_project_EDA_4.utils.utils import (
    validate_columns,
)


def create_interaction_feature(
    df: pd.DataFrame,
    feature_name: str,
    column_a: str,
    column_b: str,
) -> pd.DataFrame:
    validate_columns(df, [column_a, column_b])

    if not feature_name:
        raise ValueError("feature_name must not be empty")

    if feature_name in df.columns:
        raise ValueError(f"{feature_name} already exists in dataframe")

    feature_df = df.copy()
    feature_df[feature_name] = feature_df[column_a] * feature_df[column_b]

    return feature_df
