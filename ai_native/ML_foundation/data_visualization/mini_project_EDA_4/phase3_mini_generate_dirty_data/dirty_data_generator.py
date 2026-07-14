import pandas as pd
import numpy as np
from pathlib import Path

from ai_native.ML_foundation.data_visualization.mini_project_EDA_4.phase3_mini_generate_dirty_data.missing import (
    inject_missing,
)
from ai_native.ML_foundation.data_visualization.mini_project_EDA_4.phase3_mini_generate_dirty_data.duplicate import (
    inject_duplicate,
)
from ai_native.ML_foundation.data_visualization.mini_project_EDA_4.phase3_mini_generate_dirty_data.wrong_type import (
    inject_wrong_type,
)
from ai_native.ML_foundation.data_visualization.mini_project_EDA_4.phase3_mini_generate_dirty_data.invalid import (
    inject_invalid_value,
)
from ai_native.ML_foundation.data_visualization.mini_project_EDA_4.phase3_mini_generate_dirty_data.outlier import (
    inject_outlier,
)

# Tool will helpful to generate dirty data
# inject_missing(df, ...)
# inject_duplicate(df, ...)
# inject_wrong_type(df, ...)
# inject_invalid_value(df, ...)
# inject_outlier(df, ...)


BASE_DIR = Path(__file__).parent
csv_path = BASE_DIR / "employee_recruitment.csv"

df = pd.read_csv(csv_path)

inject_missing(df, columns=["Age", "English"], percent=0.05, seed=42)
inject_duplicate(df, percent=0.05, shuffle=True, seed=42)
inject_wrong_type(
    df,
    columns=["Age", "English"],
    wrong_values=["abc", "N/A", "-", "unknown"],
    percent=0.05,
    seed=42,
)
inject_invalid_value(df, columns=["Age", "English", "Python"], percent=0.05, seed=42)
inject_outlier(
    df, columns=["Age", "English", "Python", "Experience"], percent=0.05, seed=42
)
