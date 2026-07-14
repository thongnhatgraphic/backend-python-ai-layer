1. Business Understanding
    Ví dụ:
    🟢Business Goal🟢
        - Xây dựng AI dự đoán ứng viên có được tuyển hay không.
    Problem Type
        - Binary Classification
    Target
        - Hired
    Business Rules
    - Candidate đạt từ 65 điểm trở lên sẽ được Hired.

2. Dataset Summary
    Samples
    10000 Features
    10
    Target
    1

    Missing -> Không có

    Duplicate -> Không có

    Wrong Data Type -> Không có

    Invalid Value -> Không có

3. Target Analysis

    Ví dụ.
    Target Distribution
        Hired = 8.2%
        Not Hired = 91.8%

Insight

Dataset có hiện tượng mất cân bằng.
Điều này phản ánh đúng bài toán tuyển dụng.
Khi đánh giá Model cần chú ý Precision Recall F1 thay vì Accuracy.

4. Feature Analysis
Experience

★★★★★

Có khả năng phân biệt rất mạnh.

Projects

★★★★★

Có khả năng phân biệt rất mạnh.

Python

★★★★☆

Khá mạnh.

English

★★☆☆☆

Yếu.

5. Correlation Analysis
Ví dụ: Experience và Projects
    Correlation = 0.99
    Hai Feature gần như cùng mang một lượng thông tin.
    Sau này cần cân nhắc Multicollinearity.

6. Data Quality

Ví dụ.
    Current Dataset

    Không có Missing.

    Không Duplicate.

    Không Wrong Type.

    Không Invalid Value.

    Dataset sạch.

    Có thể dùng cho Machine Learning.

7. Recommendation
    Recommendation
    Dataset đủ chất lượng để chuyển sang Feature Engineering.
    Cần chú ý Target Imbalance khi train Model.
    Experience và Projects có Correlation rất cao.
    Sau này cần xem có nên giữ cả hai hay không.


    
------------------------------------------
    Step 1: EDA

Liệt kê thì bạn đã liệt kê phía trên rồi. 

Có 150 samples

15~20 dòng NULL trên / 150 samples 

8~10 record duplicate( có 1 số không trùng candidateID nên giả sử còn lại tâm khoảng 4 ~ 5 samples thật sự bị duplicate thật) => 4~5 / 150 samples 

Data Type Wrong 3 samples => 3/150 samples

7 samples bị invalid values => 7/150

1 Outlier => 1/150



Step2 và 3: Back-Up dataset (Giữ lại 1 bản gốc)

Đầu tiên: Deplicatiate -> Drop

Thứ 2: Data types sai -> Convert -> Missing và không xử lý được -> đưa về Null -> Fill

Thứ 3: Invalid Value 

 Sử dụng kiến thức điều kiện để lấy ra tất cả cá giá trị sai ví dụ: (df["Age"] so sánh với rule) | (df["English"] so sánh với rule) | (df["Project"] so sánh với rule) |( df["Python"] so sánh với rule) |  (df["Education"] so sánh với rule) Nếu không có rule thì không cần đưa vào điều kiện. Sau lấy được xong thì điều tra hoặc confirm lại với cấp trên hoặc làm gì đó mình chưa biết

Thứ 4: Check Null. Nếu ít quá 1 or 2 samples thì df.drop_duplicates() luôn cho nhanh vì nó cũng không ảnh hưởng mấy, Còn nếu có số lượng tương đối ( xem xét outlier ) vì chỉ có 150 samples tương đối ít nên đôi khi outlier bất thường sẽ kéo giá trị mất cân bằng nên cân nhắc sử dụng median thay vì mean fillna(mean) hay fillna(median) tuỳ trường hợp. Median và mean mở df.describe() lên để lấy thôi


Step 4: Kiểm trả lại df.info() df.describe()df.isnull().sum()  và đối chiếu business rule  nếu không có gì bất thường thì đi tiếp còn có thì focus vào những trace đó để tìm giá trị bất thường xử lý tiếp như bước 3

Step 5: Viết kết luận sau khi clean tổng hợp

Dataset Ready.
No Missing.
No Wrong Type.
No Duplicate.
Invalid Values handled.
Ready for Feature Engineering.

