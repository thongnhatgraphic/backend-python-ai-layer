from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import numpy as np

import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).parent

csv_path = BASE_DIR / "employee_salary.csv"

df = pd.read_csv(csv_path)


X = df[["Age", "English", "Experience"]]
y = df["Hired"]
print("X", X)
model = LogisticRegression()

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)

scaler = StandardScaler()

# scaler.fit is used to calculate the mean and standard deviation
# of the training data
# And transform is used to normalize the training data by subtracting the mean
# and dividing by the standard deviation
X_train_scalled = scaler.fit_transform(X_train)

X_test_scalled = scaler.transform(X_test)

model.fit(X_train_scalled, y_train)


y_predict_test = model.predict(X_test_scalled)
y_predict_proba_test = model.predict_proba(X_test_scalled)

print("y_predict_test", y_predict_test)
print("y_predict_proba_test", y_predict_proba_test)

# But if you want custom decision boundary,
# you need to change the decision_boundary value
decision_boundary = 0.1  # You can change this value


y_predict_with_decision_boundary = [
    "YES" if y >= decision_boundary else "No"
    for y in np.array(y_predict_proba_test[:, 1])
]

print(
    "\n \n y_predict_with_decision_boundary\n \n ",
    y_predict_with_decision_boundary,
)

print("\n \n model.classes_ \n \n", type(model.classes_))
# <!-- Loop từng phần tử y_predict_test:  -->


# [
#     [0.82601781 0.17398219]
#     [0.93381504 0.06618496]
# ]
