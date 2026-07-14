from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import MinMaxScaler, StandardScaler


import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).parent

csv_path = BASE_DIR / "employee_salary.csv"

df = pd.read_csv(csv_path)

# print("\n \ndata head \n \n", df.head(), "\n \n")
# df.info()
# print("\n \n data describe \n \n", df.describe())

X = df[["Age", "English", "Experience"]]
y = df["Salary"]

model = LinearRegression()


# =========Excercise 1: Train model and train test

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)
model.fit(X_train, y_train)

print(type(model.coef_))
print("\n \n model.coef_ \n \n", model.coef_)
# # print(model.coef_[0])
# # print(model.coef_[1])
# print("\n \n model.intercept_ \n \n", model.intercept_)

# y_pred = model.predict(X_test)
# print(y_test)
# print("\n \n y_pred \n \n", y_pred)

# =========Excercise 2: Cross validation
# scores = cross_val_score(model, X, y, cv=4)

# print("\n \n type scores \n \n", type(scores))
# print("\n \n scores \n \n", scores)
# print("\n \n scores.mean() \n \n", scores.mean())
# print("\n \n scores.std() \n \n", scores.std())

# ========Excercise 3: MinMaxScaler And StandardScaler

# --------- MinMaxScaler ---------
scaler = MinMaxScaler()

model2 = LinearRegression()
# # print("\n \n X_train \n \n", X_train)

# scaler.fit(X_train)
# print("\n \n scaler \n \n", scaler.data_min_)
# print("\n \n scaler \n \n", scaler.data_max_)
# print("\n \n scaler \n \n", scaler.data_range_)

# X_train_scalled = scaler.transform(X_train)
# print("\n \n X_train_scalled \n \n", X_train_scalled)

# print("\n \n X_test \n \n", X_test)

# X_test_scalled = scaler.transform(X_test)
# print("\n \n X_test_scalled \n \n", X_test_scalled)


# -------------StandardScaler-------------
# scaler = StandardScaler()

# model3 = LinearRegression()

# X_train_scalled = scaler.fit_transform(X_train)
# print("\n \n X_train_scalled \n \n", X_train_scalled)

# X_test_scalled = scaler.transform(X_test)
# print("\n \n X_test_scalled \n \n", X_test_scalled)


# # -----------Trainning----------------
# model3.fit(X_train_scalled, y_train)
# print("\n \n model3.coef_ \n \n", model3.coef_)
# print("\n \n model3.intercept_ \n \n", model3.intercept_)
# print("\n \n y_train.mean() \n \n", y_train.mean())

# y_predict_test = model3.predict(X_test_scalled)
# print("\n \n y_predict_test \n \n", y_predict_test)
# print("\n \n y_test \n \n", y_test)

# # ================ Training Model after transform data =============
# model2.fit(X_train_scalled, y_train)

# print("\n \n model2.coef_ \n \n", model2.coef_)
# print("\n \n model2.intercept_ \n \n", model2.intercept_)


# y_predict_1 = model.predict(X_test)

# y_predict_2 = model2.predict(X_test_scalled)

# print("\n \n y_predict_1 \n \n", y_predict_1)
# print("\n \n y_predict_2 \n \n", y_predict_2)
