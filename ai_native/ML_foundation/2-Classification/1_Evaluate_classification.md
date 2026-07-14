Accuracy: Sự chính xác
Precision: Độ chính xác
Recall: Nhớ lại
F1-score: 

-------------tư duy quan trọng nhất khi xây AI:-------------
"Đừng tối ưu một chỉ số trước khi hiểu chi phí của từng loại sai lầm.

 --------------------------------------------------
| True Positive (TP)    |      False Positive (FP) |
|-----------------------|--------------------------|
| False Negative (FN)   |       True Negative (TN) |
 --------------------------------------------------

Recall = TP / (TP + FN)   
<!-- Recall nhìn cột -->

Precision = TP / (TP + FP)
<!-- Precision nhìn hàng -->

F1-score: F1 thích sự cân bằng.














X = df[["Age", "English", "Experience"]]
y = df["Hired"]

model = LogisticRegression()

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state = 42
)

scaler = StandardScaler()

decision_boundary = 0.5

X_train_scalled = scaler.fit_transform(X_train)

X_test_scalled = scaler.transform(X_test)

model.fit(X_train_scalled, y_train)


y_predict_test = model.predict(X_test_scalled)

<!-- Loop từng phần tử y_predict_test:  -->
    result_y_test = [ "YES" if y > decision_boundary else "NO" for y in y_predict_test ]