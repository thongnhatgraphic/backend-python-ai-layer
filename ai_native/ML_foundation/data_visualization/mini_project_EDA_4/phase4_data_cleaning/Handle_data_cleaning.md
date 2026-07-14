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