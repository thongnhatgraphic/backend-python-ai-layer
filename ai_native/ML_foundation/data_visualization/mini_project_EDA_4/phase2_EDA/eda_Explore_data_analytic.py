import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
import seaborn as sns

BASE_DIR = Path(__file__).parent

csv_path = BASE_DIR / "employee_recruitment.csv"

df = pd.read_csv(csv_path)


# df.info()

# print("\n \n data describe \n \n", df.describe())
# print(df["Education"].value_counts())

# print("\n \n data head \n \n", df.head(), "\n \n")
# print("\n \n data tail \n \n", df.tail(), "\n \n")


# print("\n \n shape \n \n", df.shape)

# print("\n \n Collumn \n \n", df.columns)
# print("\n \n df types \n \n", df.dtypes)

# ---------------- 🟢 DataSet Overview --------------
# print("\n \n Hired \n \n", df["Hired"].value_counts())

# print("\n \n Hired \n \n", df["Hired"].value_counts(normalize=True))

# print("\n \n Education \n \n", df["Education"].value_counts(normalize=True))

# print("\n \n Docker \n \n", df["Docker"].value_counts(normalize=True))


# ---------------- 🟢 Target Analysis-------------------
# print(df.groupby("Hired").mean())
# Columns docker chỉ có value 1 or 0 ( biết docker or không biết)
# 1 0 1 1 0 => (1+0+1+1+0)/5 = 0.6 => 60% biết docker trong cột hire = 1 or 0


#              Age     English  Experience   Projects  Education     Python    Docker     Redis  RabbitMQ        AI
# Hired
# 0      33.345023  699.344696    6.071008   7.044326   0.798519  73.518514  0.190264  0.193313  0.195056  0.096058
# 1      36.019560  729.916870   12.090465  12.959658   0.815403  84.932763  0.289731  0.322738  0.332518  0.523227


# ---------------- 🟢 Feature Analysis -------------------
# 🟢 analytic feature - target 🟢
# df.boxplot(column="Experience", by="Hired")  # Draw plot

# df.boxplot(column="Python", by="Hired")
# df.boxplot(column="English", by="Hired")
# df.boxplot(column="Projects", by="Hired")
# plt.show()
# 1. Median( trung vị) Có khác không?
# ---------------
# 2. Box Có chồng nhiều không?
# ---------------
# 3. Outlier Có nhiều không? giá trị nằm ngoài phạm vi cơ bản nhiều k?
# ---------------
# 4. Nhóm nào Phân bố Đồng đều hơn?
# ---------------
# 5. Feature Có phân biệt được Target không?


# ---------------- 🟢 Correlation Analysis -------------------
# print(df.corr(numeric_only=True))
correlation_table = df.corr(numeric_only=True)
correlation_column = correlation_table["Hired"]
# print(correlation_column)
# focus on 3 relationships ① Feature ↔ Target ② Feature ↔ Feature ③ single feature


# ---------------- 🟢 Histogram -------------------
# 🟢 analytic single feature 🟢
# Feature này đang phân bố như thế nào?

# Base on Checklist ( dựa vào checklist ) trả lời 5 câu hỏi:
# ① Đỉnh của Histogram nằm ở khoảng nào?
# ② Có giống hình chuông (Bell Shape) không?
# ③ Có nhiều đỉnh không?
#   Unimodal Distribution ( 1 đỉnh )
#   Bimodal Distribution ( 2 đỉnh )
# ④ Có giá trị nào bất thường không?
# ⑤ Có đúng với logic generate không?

# df["Experience"].hist(bins=21)  # bins ở đây gọi là khoảng hay vùng
# plt.title("Experience distribution")
# plt.xlabel("Experience of years")
# plt.ylabel("Count")
# plt.show()

# df["Projects"].hist(bins=10)  # bins ở đây gọi là khoảng hay vùng
# plt.title("Projects distribution")
# plt.xlabel("Projects Score")
# plt.ylabel("Count")
# plt.show()

# df["Python"].hist(bins=10)  # bins ở đây gọi là khoảng hay vùng
# plt.title("Python distribution")
# plt.xlabel("Python Score")
# plt.ylabel("Count")

# plt.show()


# ---------------- 🟢 Scatter Plot -------------------
# 🟢 feature <-> feature 🟢
# plt.scatter(df["Experience"], df["Projects"], alpha=0.2)

# plt.xlabel("Experience")
# plt.ylabel("Projects")
# plt.show()


# ---------------- 🟢 Heatmap  -------------------
# pip install seaborn
sns.heatmap(correlation_table, annot=True, cmap="coolwarm")

# plt.show()


# ---------------- 🟢🟢 Data cleaning 🟢🟢 -------------------
# 🟢 1. Missing Values
print("\n\n is Null \n\n", df.isnull())
