import pandas as pd

from ai_native.ML_foundation.data_visualization.mini_project_EDA_4.utils.utils import (
    validate_columns,
)


def create_weighted_feature(
    df: pd.DataFrame, feature_name: str, columns: list[str], weights: list[float]
) -> pd.DataFrame:
    validate_columns(df, columns)

    if not feature_name:
        raise ValueError("feature_name must not be empty")

    if len(columns) != len(weights):
        raise ValueError("columns and weights must have the same length")

    if feature_name in df.columns:
        raise ValueError(f"{feature_name} already exists in dataframe")

    total = sum(weights)
    if int(total) != 1:
        weights = [w / total for w in weights]

    feature_df = df.copy()
    score = pd.Series(0.0, index=feature_df.index)

    for column, weight in zip(columns, weights):
        score += feature_df[column] * weight

    feature_df[feature_name] = score

    return feature_df
