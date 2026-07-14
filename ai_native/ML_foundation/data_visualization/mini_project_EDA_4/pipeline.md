🗺️ Mini Project: AI Recruitment System
                     AI Recruitment System

                            │
                            ▼
            ┌─────────────────────────────────┐
            │ Phase 1. Dataset Generation      │
            └─────────────────────────────────┘
                            │
                            ▼
      Sinh dữ liệu có quy luật giống ngoài đời
                            │
                            ▼
    Age
    English
    Experience
    Projects
    Education
    Python
    Docker
    Redis
    RabbitMQ
    AI
                            │
                            ▼
         Rule Engine (Business Rules)
                            │
                            ▼
                  Score Calculation
                            │
                            ▼
                  Hired (Target)

🎉 Phase 1 đã gần hoàn thành.

Phase 2 - EDA (Exploratory Data Analysis)
    1. Load Dataset

    2. Dataset Overview

    3. Data Quality Check
        ├── Missing Value 
                        ├── Missing?
                        │
                        ▼
                        Bao nhiêu %?
                            │
                            ▼
                        Feature quan trọng không?
                            │
                        ┌────┴────┐
                        Có         Không
                        │           │
                        ▼           ▼
                    Có thể      Có thể bỏ
                thu thâp lại
                        │ 
                        ├── Có → Thu thập thêm
                        │
                        └── Không
                            │
                            ▼
                        Mean / Median / Mode / Model-based Imputation
                                |
                                | df["Experience"].fillna(4)        
                                | df["Education"].mode()

        ├── Duplicate
                |_  Các dòng duplicate -> df[df.duplicated()]
                |_  Muốn xóa -> df.drop_duplicates()

        ├── Outlier

        ├── Wrong Type
                        |
                        Wrong Data Type
                        ↓
                        df.info()
                        ↓
                        Kiểm tra Data Type
                        ----------------------------
                        Invalid Value
                        ↓
                        df.describe()
                        ↓
                        Kiểm tra min/max
                        ↓
                        value_counts()
                        ↓
                        Đối chiếu Business Rule
        4. Invalid Values
                        ├── describe()
                        ├── value_counts()
                        └── Business Rule

        6. Target Imbalance (đã học)

    4. Statistics

    5. Target Analysis

        ├── GroupBy

        ├── Boxplot ❓ Hai nhóm có khác nhau không?

        ├── Histogram ❓Feature này phân bố ra sao? Có phân phối lạ không?

        ├── Scatter Plot ❓Hai biến có quy luật với nhau không?

        └── Violin Plot
            

    6. Correlation Analysis

        ├── Correlation Matrix ❓Mức độ liên quan tuyến tính là bao nhiêu?

        └── Heatmap

    7. Outlier Detection

    8. EDA Report

    🎯 Mục tiêu:

    Hiểu dataset trước khi train AI.

Phase 3 🟢🟢- Data Cleaning
        Load Dataset
            │
            ▼
        EDA
            │
            ▼
        Backup dataset gốc
            │
            ▼
        Liệt kê tất cả vấn đề
            │
            ▼
        Lập kế hoạch xử lý
            - Lập theo thứ tự:
                1. Duplicate ( -Nếu bạn fill Missing trước.
                Thì bạn sẽ fill tới 3 dòng. )
                2. Data types sai ( có cả number và string k tính được mean và median) Ví dụ: "abc' k xử lý được => chuyển thành NULL
                    Wrong Type
                    ↓
                    Convert
                    ↓
                    Missing
                    ↓
                    Fill
                3. Invalid value ( dựa vào rule business ) điều tra trước
                4. NULL. ( Check Outlier ) để biết liệu dùng mean hay median
            │
            ▼
        Thực hiện Data Cleaning
            │
            ▼
        Kiểm tra lại
            │
            ▼
        Dataset Ready

Phase 4 - Feature Engineering
Features
    │
    ▼

Tạo thêm Feature

    │
    ├── Experience × Python

    ├── AI + Python

    ├── Seniority

    ├── Skill Score

    └── Remove useless features

Đây là nơi Business Thinking cực kỳ quan trọng.

Phase 5 - Data Preprocessing
Dataset
    │
    ▼

Model Ready

    │
    ├── Train/Test Split

    ├── StandardScaler

    ├── Encoding

    ├── Balance Dataset

    └── Cross Validation

Đây là phần chúng ta đã học nhưng sẽ làm lại trên dataset thật.

Phase 6 - Model Training
Dataset

        │

        ▼

Model

    │

    ├── Logistic Regression

    ├── Decision Tree

    ├── Random Forest

    └── Gradient Boosting

🎯 Đây sẽ là lần đầu tiên chúng ta so sánh nhiều model trên cùng một dataset.

Phase 7 - Model Evaluation
Accuracy

Precision

Recall

F1

Confusion Matrix

ROC AUC (sau này)

Cross Validation

Đây chính là phần đọc "hồ sơ sức khỏe" của model mà bạn rất thích.

Phase 8 - Model Improvement
Tuning

↓

Feature Engineering

↓

Hyperparameter

↓

Retrain

↓

Compare

Lúc này chúng ta sẽ bắt đầu giống Data Scientist.

Phase 9 - Export Model
Model

↓

joblib

↓

model.pkl

Để Backend có thể dùng.

Phase 10 - FastAPI AI Service
Frontend

↓

FastAPI

↓

Load model.pkl

↓

Predict

↓

Response

Đây là lúc Backend AI Engineer xuất hiện.

Phase 11 - Docker
FastAPI

+

Model

+

Docker
Phase 12 - Production
Monitoring

Logging

Retraining

Model Version

Deployment

Đây là bức tranh đầy đủ của một AI Backend System.