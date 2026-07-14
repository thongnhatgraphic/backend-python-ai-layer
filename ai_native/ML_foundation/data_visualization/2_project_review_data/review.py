from pandas import read_csv
from pathlib import Path

BASE_DIR = Path(__file__).parent

csv_path = BASE_DIR / "employee_salary.csv"

df = read_csv(csv_path)


print(df.describe())


print("\n \n check null \n \n", df.isnull().sum())

print(df.corr(numeric_only=True))
