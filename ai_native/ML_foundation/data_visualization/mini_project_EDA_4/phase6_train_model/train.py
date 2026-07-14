import pandas as pd
import pathlib
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)

BASE_DIR = pathlib.Path(__file__).parent

csv_path = BASE_DIR / "employee_recruitment_backend_skill.csv"

df = pd.read_csv(csv_path)

FEATURES = [
    "Age",
    "English",
    "Experience",
    "Projects",
    "Education",
    "Python",
    "Docker",
    "Redis",
    "RabbitMQ",
    "AI",
    "BackendSkill",
    "ProjectCompletionExperience",
    "InternationalExperience",
]
TARGET = "Hired"

X = df[FEATURES]
y = df[TARGET]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


scaler = StandardScaler()

scaler.fit(X_train)

X_train_scalled = scaler.transform(X_train)
# print("\n \n X_train_scalled \n \n", X_train_scalled)
# print("\n \n type \n \n", type(X_train_scalled))

X_train_scaled = pd.DataFrame(
    X_train_scalled,
    columns=X_train.columns,
    index=X_train.index,
)

# print("\n \n X_train_scaled \n \n", X_train_scaled)
# print("\n \n type \n \n", type(X_train_scaled))

X_test_scalled = scaler.transform(X_test)
# print("\n \n X_test_scalled \n \n", X_test_scalled)

model = LogisticRegression()

model.fit(X_train_scalled, y_train)


y_pred = model.predict(X_test_scalled)

# So sanh với y_test
mask = y_test != y_pred

error_X = X_test[mask].copy()
y_prediction = y_pred[mask]
y_actual = y_test[mask]

error_X["Actual"] = y_actual
error_X["Prediction"] = y_prediction

# print(X_test.describe())
# print(error_X.describe())

# print(error_X.groupby(["Actual", "Prediction"]).mean(numeric_only=True))


accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)


# print(f"\n accuracy: {accuracy} \n")
# print(f"\n \n precision: {precision} \n \n")
# print(f"\n recall: {recall} \n")
# print(f"\n f1: {f1} \n")
print(model.coef_)
print(model.intercept_)
print(FEATURES)
