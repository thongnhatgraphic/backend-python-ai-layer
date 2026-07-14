 * Logistic Regression dùng để Classification


Logistic regression làm việc y hệt linear regression
    ex: y = a1X1 + a2x2 + a3x3 + b

ví dụ: logistic tính
z = 30×(-0.2) + 700×0.01 + 5×2 - 5 = 6

Thay vì trả value  = 6. Nó đưa 6 vào Sigmoid biến -> 0.997

Features
    │
    ▼
Age × w₁

English × w₂

Experience × w₃
    │
    ▼
Cộng Bias
    │
    ▼
z
    │
    ▼
Sigmoid
    │
    ▼
Probability
    │
    ▼
Decision Boundary
    │
    ▼
0 hoặc 1