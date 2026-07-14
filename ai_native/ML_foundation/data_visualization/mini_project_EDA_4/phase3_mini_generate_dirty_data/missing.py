import pandas as pd
import numpy as np
import random

from ai_native.ML_foundation.data_visualization.mini_project_EDA_4.phase3_mini_generate_dirty_data.utils import (
    validate_columns,
    validate_percent,
    generate_random_cells,
)
from ai_native.ML_foundation.data_visualization.mini_project_EDA_4.phase3_mini_generate_dirty_data.business_ruls import (
    percent_missing,
)


def inject_missing(
    df: pd.DataFrame, columns: list[str], percent: float, seed: int | None = None
) -> pd.DataFrame:
    validate_columns(df, columns)
    validate_percent(percent, percent_missing)

    missing_df = df.copy()
    num_rows = len(df)
    amount = int(num_rows * percent)

    cells = generate_random_cells(num_rows, columns, amount, seed)
    print("cells", cells)

    for row, column in cells:
        missing_df.loc[row, column] = np.nan

    return missing_df
