Kiến thức cũ:


Loss = | Thật - Dự Đoán |

Ví dụ:

Thật	Dự đoán
100	    90

Sai số: | 100 - 90 | = 10

****Giả sử bài toán:

Model A: Có sai số 10  10 10 10 10 tổng loss = 50

Model B: Có sai số 0 0 0 0 50 tổng loss = 50
-----------------------
A = 50
B = 50
AI sẽ nghĩ:
Hai model tốt như nhau.
Nếu là con người Model B có 1 lỗi cực lớn. Mà 1 lỗi cực lớn thì nguy hiểm hơn nhiều lỗi nhỏ.

Vì vậy: Thay vì loss = | error |
 ------------------------
| Người ta dùng | error² | Bình phương sai số
 ------------------------

Ví dụ Model A: 100 + 100 + 100 + 100 + 100 = 500
Ví dụ Model A: 0 + 0 + 0 + 0 + 2500 = 2500

Ta thấy: A < B
- AI lập tức thấy:
    Model B tệ hơn rất nhiều.

=> Ý tưởng Cốt lõi MSE ra đời. ( Sai cực lớn phạt cực nặng )

M:  Mean  Lấy Trung Bình (Tổng / số lượng mẫu)
S:  Squared Bình phương (error²)
E:  Sai số ( Thật - Dự Đoán)

Ví dụ: Sai số: 2    4   6
S -> 4 + 16 + 36 = 56 
Mean -> 56 / 3 = 18.6666

Điều cực kỳ quan trọng
Trong AI thực tế:
            --------------------------
            loss = MSE(y_true, y_pred)
            --------------------------
-   Thường là thứ model đang cố giảm.

    model.fit(X, y)
    Đoán
    ↓
    Tính MSE
    ↓
    Sửa tham số
    ↓
    Tính MSE
    ↓
    Sửa tiếp
    ↓
    MSE nhỏ hơn

Lúc trước:
Feature
↓
Model
↓
Prediction
↓
Error
↓
Loss

Bây giờ sẽ là: 
Error
↓
Error²
↓
Mean
↓
MSE

Experience	Salary
1	        15
2	        25
3	        35
4	        45

Model A:
15 - 10 = 5 => 25
25 - 18 = 7 => 49
35 - 26 = 9 => 81
45 - 34 = 11 => 121
MSE: 276 / 4 = 69

y = 9x + 2
Model B:
15 - 11 = 4 => 16
25 - 20 = 5 => 25
35 - 29 = 6 => 36
45 - 38 = 7 => 49
MSE: 126 / 4 = 31.5


15/1 + 25/2 + 35\x3 + 45/4 = 12.53
a = 12

(15 - 12) + (25 - 24) + (35 - 36) + ( 45 - 48 )
3 + 1 -1 - 3 = 0 / 0

81
169
289
441