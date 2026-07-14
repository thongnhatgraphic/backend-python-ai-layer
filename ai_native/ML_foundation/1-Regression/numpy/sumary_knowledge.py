# Vector
# Distance
# Dot Product
# Cosine Similarity
# Matrix
# Shape
# Sample
# Feature
# Target -->

# Bảng:

# age	salary	bought
# 25	1000	1
# 30	2000	0
# 22	1500	1

# -----------------Weight and Bias-----------------
# Weight chính là:
# Mức độ ảnh hưởng của Feature lên Target.

# Bias là Bias là tham số điều chỉnh giúp model dịch chuyển 
# kết quả dự đoán lên hoặc xuống để phù hợp hơn với dữ liệu thực tế.



# Columns age and salary is input ( Feature)
# Column bought is Target

# Dataset: Bộ dữ liệu

# Training set: Bộ dữ liệu học 
# Test set: Bộ dữ liệu test


# Train accuracy: Dữ liệu để Model học
# Test accuracy: Dữ lieu test de test Model học

Train accuracy = 100% thì Model nó chỉ đang học dữ liệu, không học được quy luật chung.
Test accuracy = 52% thì Model Khi nó gặp những dữ liệu mô hình nó học, nó không học được quy luật chung.


Với Train accuracy = 80% và Test accuracy = 82% thì Model nó học được quy luật chung. generalization cao

# Overfitting: Khớp hoàn toàn

# 1. Train Set
# Dữ liệu để model học.

# 2. Test Set
# Dữ liệu model chưa từng thấy.

# 3. Overfitting
# Model nhớ dữ liệu train.
# Không học được quy luật chung.

AI = Tìm quy luật trong dữ liệu
AI = Học bằng cách giảm sai số (Loss)

giả sử y = a1x1 + a2x2 + a3x3 + b
model.fit(X, y) thực chất đang tìm weight hệ số a1 a2 a3 b

Ta có: model.coef_ = [a1, a2, a3]
model.intercept_ = b
# coef_ is short for Coefficient ( hệ số )
# intercept_ is short for Intercept ( giao điểm )

------------------------------------------------------

NumPy

    Vector
    Matrix
    Shape
    Distance
    Dot Product
    Cosine Similarity
Pandas

    DataFrame
    Rows
    Columns
    Feature
    Target
Machine Learning Foundation

    Train
    Test
    Accuracy
    Overfitting
    Loss
    MSE
    Weight
    Bias
Linear Regression

    y = ax + b

    a = Weight
    b = Bias
Classification

    Probability
    Decision Boundary
    Logistic Regression

-----
    Progress
    ↓
    Probability
    ↓
    YES / NO

    
✅ Neuron

✅ ReLU 0 nếu < 0 và > 0 dữ nguyên ReLU(70) = 20 và ReLU(-20) = 0

✅ Hidden Layer

Backpropagation = Tìm Weight nào gây lỗi nhiều nhất

            a quan trọng hơn b
**  Toán học viết thành:
    Gradient của a lớn hơn Gradient của b

            thử tăng a xem Loss giảm không
**  Toán học viết thành:
    ∂Loss/∂a


************Logistic Regression************
Dùng cho classification = Phân loại
Probability -> 0 - 1 YES / NO
Sigmoid Function (Hàm Sigmoid)

# Nhìn lại:
Linear Regression:
    Input
    ↓
    wx+b
    ↓
    Salary

Neuron
    Input
    ↓
    wx+b
    ↓
    Activation Function
    ↓
    Output

Logistic Regression: quá trình này đưa dữ liệu thô thành probability
    Input
    ↓
    wx+b
    ↓
    Sigmoid
    ↓
    Probability 


Logistic Regression là 1 neuron hoàn chỉnh
---------------------------------------------
| Neuron = Linear Part + Activation Function|
---------------------------------------------

Phần tuyến tính và Activation Function = Hàm kích hoạt (Sigmoid, ReLU...)

Linear Regression
↓
Logistic Regression
↓
Neuron


Neural Network: ( Mạng lưới nơ-ron)
Ví dụ:

    Progress --------\
    Priority --------- > Neuron A
    Deadline --------/

    Progress --------\
    Priority --------- > Neuron B
    Deadline --------/

    Progress --------\
    Priority --------- > Neuron C
    Deadline --------/

Kết quả:
    Neuron A = 0.95

    Neuron B = 0.90

    Neuron C = 0.85