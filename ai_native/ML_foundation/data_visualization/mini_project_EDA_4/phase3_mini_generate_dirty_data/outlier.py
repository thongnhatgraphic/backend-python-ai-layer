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
    percent_outlier,
    outlier_rules,
)


def inject_outlier(
    df: pd.DataFrame,
    columns: list[str],
    percent: float,
    seed: int | None = None,
) -> pd.DataFrame:
    validate_columns(df, columns)
    validate_percent(percent, percent_outlier)

    outlier_df = df.copy()

    num_rows = len(df)
    amount = int(num_rows * percent)

    cells = generate_random_cells(num_rows, columns, amount, seed)

    direction_indices = generate_random_indices(
        0,
        2,
        amount,
        seed,
    )

    for (row, column), direction in zip(cells, direction_indices):

        outlier_value = outlier_rules[column][direction]
        outlier_df.loc[row, column] = outlier_value

    return outlier_df
