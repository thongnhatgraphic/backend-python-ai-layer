Khi Train/Test được chia khác nhau, tập dữ liệu dùng để đánh giá model cũng thay đổi. Một model có thể được kiểm tra trên một tập test dễ hơn hoặc khó hơn model khác. Vì vậy sự khác biệt về Accuracy có thể đến từ việc chia dữ liệu, chứ không phải do chất lượng thực sự của model. Giữ nguyên Train/Test bằng random_state giúp đảm bảo các model được đánh giá trên cùng một bộ dữ liệu, từ đó việc so sánh trở nên công bằng hơn.              
              
              Dataset

          X             y

          │             │

     Train/Test     Train/Test

          │             │

          ▼             ▼

     X_train       y_train
     X_test        y_test

          │
          ▼

model.fit(X_train, y_train)

          │
          ▼

model.predict(X_test)

          │
          ▼

So sánh với

y_test


Pipeline thường là:

Raw Data
      │
      ▼
Data Cleaning
      │
      ▼
Feature Engineering
      │
      ▼
Train Set
      │
      ▼
Train Model
      │
      ▼
Validation
      │
      ▼
Điều chỉnh Hyperparameter
      │
      ▼
Train lại
      │
      ▼
Validation lại
      │
      ▼
(Repeat nhiều lần)
      │
      ▼
Model cuối cùng
      │
      ▼
Test đúng 1 lần
      │
      ▼
Deploy



----------------------------------------------------
----------------------------------------------------
----------------------------------------------------
CSV
↓
Pandas
↓
Review Data
↓
Clean Data
↓
Feature Engineering
↓
Train/Test Split
↓
Train
↓
Predict
↓
Evaluate ( đánh giá)



--------------Iteration (vòng lặp cải tiến)-------------
Machine Learning ngoài đời gần như luôn là:

Train
↓
Evaluate
↓
Chưa tốt
↓
Sửa
↓
Train lại
↓
Evaluate
↓
...
↓
Đạt yêu cầu
↓
Deploy


<=========Pipeline Perfect:============>

                CSV
                  │
                  ▼
          Review dữ liệu
                  │
                  ▼
         Check NULL / Clean
                  │
                  ▼
        Chọn Feature và Target
                  │
                  ▼
      Train / Validation / Test
                  │
                  ▼
            model.fit()
                  │
                  ▼
             model.predict()
                  │
                  ▼
          Đánh giá kết quả
                  │
          ┌───────┴────────┐
          │                │
      Chưa tốt          Đủ tốt
          │                │
          ▼                ▼
   Điều chỉnh Model      Deploy
          │
          └───────────────▲