from sklearn.linear_model import LinearRegression
import numpy as np
# Weight là chân ga. Bias là vị trí xuất phát.
# model.fit()
# ↓
# Học quy lý chung.

# model.predict()
# ↓
# Sử dụng kiến thức đã học

# Coefficient
# +
# Khoảng dao động của feature
# ↓
# Mức ảnh hưởng thực tế

model = LinearRegression()

X = np.array([
    [1],
    [2],
    [3],
    [4]
])

y = np.array([15, 27 , 34, 50])

model.fit(X, y)
print(model.coef_)
print(model.intercept_)
print(model.predict([[5]]))