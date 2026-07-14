import pandas as pd
import numpy as np
import random
from ai_native.ML_foundation.data_visualization.mini_project_EDA_4.phase3_mini_generate_dirty_data.utils import (
    generate_random_rows,
)
from ai_native.ML_foundation.data_visualization.mini_project_EDA_4.phase3_mini_generate_dirty_data.business_ruls import (
    percent_duplicate,
)

# copy df
# ↓
# random N row
# (không trùng)
# ↓
# append
# ↓
# shuffle
# ↓
# reset index
# ↓
# return


def inject_duplicate(
    df: pd.DataFrame, percent: float, shuffle: bool = True, seed: int | None = None
) -> pd.DataFrame:

    if percent <= 0 or percent > percent_duplicate:
        raise ValueError(f"'percent' must be in the range (0, {percent_duplicate}].")

    duplicate_df = df.copy()

    total_rows = len(df)
    random_index_rows = generate_random_rows(
        0, total_rows, int(total_rows * percent), seed
    )

    duplicate_rows = duplicate_df.loc[random_index_rows]

    duplicate_df = pd.concat([duplicate_df, duplicate_rows], ignore_index=True)

    if shuffle:
        duplicate_df = duplicate_df.sample(frac=1, random_state=seed)

    duplicate_df.reset_index(drop=True, inplace=True)

    return duplicate_df
