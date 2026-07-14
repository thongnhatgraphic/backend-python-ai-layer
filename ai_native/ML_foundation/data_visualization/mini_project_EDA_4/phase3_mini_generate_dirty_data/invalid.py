import pandas as pd
import numpy as np
import random

from ai_native.ML_foundation.data_visualization.mini_project_EDA_4.phase3_mini_generate_dirty_data.utils import (
    generate_random_rows,
    generate_random_indices,
    validate_columns,
    validate_percent,
    generate_random_cells,
)
from ai_native.ML_foundation.data_visualization.mini_project_EDA_4.phase3_mini_generate_dirty_data.business_ruls import (
    percent_invalid_value,
    invalid_rules,
)


def inject_invalid_value(
    df: pd.DataFrame, columns: list[str], percent: float, seed: int | None = None
) -> pd.DataFrame:
    validate_columns(df, columns)
    validate_percent(percent, percent_invalid_value)

    # check key in columns if exist valid_rules
    invalid_columns_in_valid_rules = set(columns) - set(invalid_rules.keys())
    if invalid_columns_in_valid_rules:
        raise ValueError(
            f"Columns not found in valid_rules: {sorted(invalid_columns_in_valid_rules)}"
        )

    invalid_df = df.copy()
    num_rows = len(df)
    amount = int(num_rows * percent)

    cells = generate_random_cells(num_rows, columns, amount, seed)

    for row, column in cells:
        if pd.isna(invalid_df.loc[row, column]):
            continue
        invalid_df.loc[row, column] = invalid_rules[column]

    return invalid_df
