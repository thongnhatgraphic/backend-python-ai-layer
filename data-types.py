import numpy as np

name = "john"
age = 20
price = 10.5
is_student = True

print(type(name))
print(type(age))
print(type(price))
print(type(is_student))


y_predict_test = np.array([[0.1, 0.2, 0.3], [0.2, 0.4, 0.5], [0.1, 0.2, 0.3]])

prob_yes = y_predict_test[:, 1]  # Lấy mọi hàng của cột 1

print(prob_yes)

# convert list new_y_great_5 to YES OR NO IF each value is greater than 5
new_y_great_dot2 = ["YES" if y >= 0.2 else "NO" for y in prob_yes]

print(new_y_great_dot2)
