import pandas as pd
import numpy as np
import pathlib

from ai_native.ML_foundation.data_visualization.mini_project_EDA_4.utils.utils import (
    validate_columns,
)


def create_ratio_feature(
    df: pd.DataFrame,
    feature_name: str,
    numerator: str,
    denominator: str,
) -> pd.DataFrame:
    validate_columns(df, [numerator, denominator])

    if not feature_name:
        raise ValueError("feature_name must not be empty")

    if feature_name in df.columns:
        raise ValueError(f"{feature_name} already exists in dataframe")

    feature_df = df.copy()
    feature_df[feature_name] = feature_df[numerator] / feature_df[denominator]

    return feature_df
