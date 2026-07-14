import pandas as pd
import numpy as np
import random

from ai_native.ML_foundation.data_visualization.mini_project_EDA_4.phase3_mini_generate_dirty_data.utils import (
    generate_random_indices,
    validate_columns,
    validate_percent,
    generate_random_cells,
)
from ai_native.ML_foundation.data_visualization.mini_project_EDA_4.phase3_mini_generate_dirty_data.business_ruls import (
    percent_wrong_type,
)


def inject_wrong_type(
    df: pd.DataFrame,
    columns: list[str],
    wrong_values: list[str],
    percent: float,
    seed: int | None = None,
) -> pd.DataFrame:

    validate_columns(df, columns)
    validate_percent(percent, percent_wrong_type)

    if not wrong_values:
        raise ValueError("wrong_values must not be empty")

    wrong_type_df = df.copy()

    num_rows = len(df)
    amount = int(num_rows * percent)
    num_wrong_values = len(wrong_values)

    cells = generate_random_cells(num_rows, columns, amount, seed)

    # list wrong values
    list_wrong_values = generate_random_indices(0, num_wrong_values, amount, seed)

    for column in columns:
        wrong_type_df[column] = wrong_type_df[column].astype(object)

    for row, column, wrong_idx in zip(cells, list_wrong_values):
        wrong_value = wrong_values[wrong_idx]
        wrong_type_df.loc[row, column] = wrong_value

    return wrong_type_df
