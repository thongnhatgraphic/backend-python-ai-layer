Đưa tất cả dữ liệu được trainning về thang đo 0 -> 1

----------------------Scaling features-------------------------


Min-Max Scaling
Công thức:
Khoảng cách từ Min
-------------------
Toàn bộ khoảng Min -> Max



- Interpolation: Nội suy ( Tức là giá trị test nó nhỏ hơn và ngoài vùng dữ liệu quá nhiều và không thực tế)
- Extrapolation: Ngoại suy ( Tức là giá trị test nó lớn hơn và ngoài vùng dữ liệu quá nhiều và không thực tế)

Standardization: Chuẩn hoá

- >                         Z-Score                         < -
Từ những Interpolation và Extrapolation chúng ta mở rộng bài toán thực tế khi gặp những dữ liệu bất thường này với "Z - Scores"

 - >    Z-Score sẽ hỏi 1 câu hỏi với giá trị bất thường:
        "Cách Mean bao nhiêu lần độ lệch chuẩn?"

Ví dụ: English:
700 750 800 850 900
Mean: 800 

Người A: English = 900

Người B:English = 1100

- # Mean = 800 Std = 100 Người A cách mean 900 - 800 = 100 và std = 100/100 = 1 Bình thường. Người B cách mean 1100 - 800 = 300 và std = 300/100 = 3 Bất thường. Người có khả năng là Outlier là B

English	Distance to Mean
700	-100
750	-50
800	0
850	50
900	100
Variance: (Phương sai) là đại lượng toán học rất đẹp để tính toán và tối ưu.
Standard Deviation: (Độ lệch chuẩn) là phiên bản "thân thiện với con người", vì nó quay về đúng đơn vị ban đầu.

mean = (700 + ...900) / 5 = 800


variance = (700 - 800)^2 + ... + (900 - 800)^2 = 25000 / 5 = 5000
std = sqrt(variance)

- > Standard Deviation không chỉ là một con số.
Nó mô tả:
        "Mức dao động bình thường của dữ liệu."

                        Data
                        │
                        ▼
                        Mean
                        │
                        ▼
                        Distance to Mean
                        │
                        ▼
                        Square
                        │
                        ▼
                        Variance
                        │
                        ▼
                        Square Root
                        │
                        ▼
                        Standard Deviation
                        │
                        ▼
                        Z-Score
                        │
                        ▼
                        StandardScaler