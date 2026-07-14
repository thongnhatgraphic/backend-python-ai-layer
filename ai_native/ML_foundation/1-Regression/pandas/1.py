from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).parent


csv_path = BASE_DIR / "employee_salary.csv"

# data = {
#     "Age": [25, 30, 35, 40],
#     "Salary": [50000, 60000, 70000, 80000]
# }

# data = {
#     "Age": [25, 30, 35, 40],
#     "Salary": [50000, 60000, 70000, 80000]
# }

df = pd.read_csv(csv_path)

# print(df)

print(df.describe())

# print(type(df))
# list_age =df["Age"] > 30

# print('list', list_age) -> ouput -> list
# 0    False
# 1    False
# 2     True
# 3     True


# ---------------Pandas dùng để làm gì?--------------------
# Pandas giúp mình làm việc với dữ liệu dạng bảng bằng tên cột thay vì index, 
# đồng thời tự động xử lý rất nhiều thao tác như lọc, chọn, thống kê...
# mà không cần tự viết vòng lặp.

