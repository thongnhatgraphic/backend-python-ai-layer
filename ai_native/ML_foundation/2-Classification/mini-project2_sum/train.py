from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)


import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).parent

csv_path = BASE_DIR / "employee_salary.csv"

df = pd.read_csv(csv_path)

X = df[["Age", "English", "Experience"]]
y = df["Hired"]

print("\n \n X \n \n", X)
df.info()
print("\n \n describe \n \n", df.describe())

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)
print("\n \n X_train \n \n", X_train)
print("\n \n y_test \n \n", y_test)

scaler = StandardScaler()

X_train_scalled = scaler.fit_transform(X_train)
print("\n \n X_train_scalled \n \n", X_train_scalled)

X_test_scalled = scaler.transform(X_test)
print("\n \n X_test_scalled \n \n", X_test_scalled)

model = LogisticRegression()

model.fit(X_train_scalled, y_train)

print("\n \n model.coef_ \n \n", model.coef_)
print("\n \n model.intercept_ \n \n", model.intercept_)

y_predict = model.predict(X_test_scalled)

print("\n \n y_predict \n \n", y_predict)
print("\n \n type y_predict \n \n", type(y_predict))
print("\n \n type y_test \n \n", type(y_test))
print("\n \n y_test \n \n", y_test)


accuracy_score = accuracy_score(y_test, y_predict)
print("\n \n accuracy_score \n \n", accuracy_score)
precision_score = precision_score(y_test, y_predict)
print("\n \n precision_score \n \n", precision_score)
recall_score = recall_score(y_test, y_predict)
print("\n \n recall_score \n \n", recall_score)
f1_score = f1_score(y_test, y_predict)
print("\n \n f1_score \n \n", f1_score)
confusion_matrix = confusion_matrix(y_test, y_predict)
print("\n \n confusion_matrix \n \n", confusion_matrix)

y_predict_probability = model.predict_proba(X_test_scalled)

print(
    "\n \n y_predict_probability\n \n ",
    y_predict_probability,
)

# scores = cross_val_score(model, X, y, cv=3)
# print("\n \n scores \n \n", scores.mean())
