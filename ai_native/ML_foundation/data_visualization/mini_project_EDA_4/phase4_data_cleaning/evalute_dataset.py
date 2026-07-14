from pathlib import Path
import pandas as pd
import numpy as np

# quy tắc của Pandas:

# df["Tên_cột"] → lấy cột.
# df[điều_kiện] → lọc các dòng.

BASE_DIR = Path(__file__).parent

csv_path = BASE_DIR / "dataset_bad.csv"

df = pd.read_csv(csv_path)

# Step1: Check null
# print(df.isnull().sum())

# # Step2: ----------Fill null----------
# # Thay tất cả NULL bằng giá trị mình chỉ định.
# print("Before fill", df["Age"])
# df["Age"] = df["Age"].fillna(28)
# print("After fill", df["Age"])

# # Nếu chỉ có vài dòng NULL. df = df.dropna() (xoá lun)
# print(df["English"].mean())


df2 = pd.DataFrame(
    {
        "Age": [25, 25, np.nan, 30, 40],
        "English": [700, 700, 650, np.nan, 800],
        "Python": [80, 80, 90, 70, np.nan],
    }
)


# print(df2.isnull())

# mask = df2["Python"] > 30
# print("mask", mask)
# Show tất cả giá trị thoả điều kiện trong mask
# print(df2[mask])

# tìm ra dòng NULL
# print(" \n\n get samples has null \n\n", df2[df2["Age"].isnull()])


# Lấy ra tất cả những samples có ít nhất 1 giá trị NULL
# print(
#     " \n\n get samples has at least one null \n\n",
#     df2[df2.isnull().any(axis=1)],
# )

# maskEng = df2["English"].isnull()
# print(" \n\n maskEng \n\n", df2[maskEng])


# Kết hợp nhiều điều kiện
# mask_eng_py = mask = df["English"].isnull() & (df["Python"] >= 90)
# print(" \n\n mask_eng_py \n\n", df2[mask_eng_py])


print(" \n\n df2 \n\n", df2)
print(" \n\n df2.duplicated() \n\n", df2[df2.duplicated()])

df2 = df2.drop_duplicates()
print(" \n\n df2 \n\n", df2)
