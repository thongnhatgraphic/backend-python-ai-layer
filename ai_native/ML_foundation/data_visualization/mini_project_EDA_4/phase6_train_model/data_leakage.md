Bản chất của Data_leakage 
Ví dụ StandardScaler.fit()

↓

StandardScaler.transform()

↓

LogisticRegression.fit()

1 Cách Vô tình: "Quá trình chuẩn bị dữ liệu (data preprocessing process) đã sử dụng thông tin của Test Set."

Ví dụ thật:
scaler = StandardScaler()

X = scaler.fit_transform(X)

Sau đó.
train_test_split(...)

Thì khi vô tình làm điều này StandardScaler đã vô tình StandardScaler.fit() để tính mean và standard deviation và vô tình leak data

Giả sử dataset của ta có 20 30 40 50 60 70 80 90
Ta viết scaler.fit(dataset) thì nó vô tình tính luôn mean = 55

sau đó chia train_test_spit thì lúc này mean đã bị nhiễm thông tin từ sự vô tình đó rồi.
