from ai_native.ML_foundation.data_visualization.mini_project_EDA_4.phase5_feature_engineering.create_weighted_feature import (
    create_weighted_feature,
)
from ai_native.ML_foundation.data_visualization.mini_project_EDA_4.phase5_feature_engineering.create_ratio_feature import (
    create_ratio_feature,
)
from ai_native.ML_foundation.data_visualization.mini_project_EDA_4.phase5_feature_engineering.create_interaction_feature import (
    create_interaction_feature,
)

import pandas as pd
import pathlib

BASE_DIR = pathlib.Path(__file__).parent

csv_path = BASE_DIR / "employees_recruitment.csv"

df = pd.read_csv(csv_path)

# df = create_weighted_feature(
#     df, "BackendSkill", ["Python", "Docker", "Redis"], [0.5, 0.3, 0.2]
# )
df = create_ratio_feature(df, "ProjectCompletionExperience", "Projects", "Experience")
df = create_interaction_feature(df, "InternationalExperience", "English", "Experience")

df.to_csv(BASE_DIR / "employees_recruitment.csv", index=False)
