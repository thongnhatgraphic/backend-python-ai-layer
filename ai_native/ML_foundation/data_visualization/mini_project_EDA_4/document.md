employee_recruitment.csv

1. Business
    - Target là hired. Thực tế trên file có tận 15% trên tổng số 10000 ứng viên được Hired.
    - Bài toán ML là Classification
    - Business muốn tuyển dụng những ứng viên có profiles đạt trên 65 điểm dựa trên business rules

2. Dataset Overview ( Trong trường hợp mình chưa làm với data NULL và duplication mình giả sử dataset của chúng ta đều có giá trị)
    - Có 10k samples
    - Có 10 features
    - Không missing dữ liệu
    - không có dữ liệu duplicate
    - data type đúng



3. Target Analysis
    - Kiểm tra dữ liệu df.describe() nhận thấy thông tin Target có mean() 0.0818 trung bình 1000 ứng viên sẽ có ~ 82 người pass
    - Hired có tỉ lệ khoảng 8.2% so với business rules và thực tế là 15% Mất cân bằng với thực tế.
    - Chú ý khi train ( Không biết)

4. Feature Analyis
    Ví dụ Experience, Projects, Python, ... 
    Ở 3 features này ta thống kê được

                Experience    Projects        Python
    count       10000.00000   10000.0000      10000.000000
    mean        6.56340       7.5282          74.452200
    std         4.65787       4.3157          9.909023
    min         1.00000       2.0000          40.000000
    25%         3.00000       4.0000          68.000000
    50%         4.00000       6.0000          74.000000
    75%         12.00000      12.0000         81.000000
    max         14.00000      15.0000         100.000000

    1. Dùng công cụ boxplot
        - Sử dụng boxplot để xem sự khác biệt giữa các features với Hired
        - Sau khi dùng thì ta thấy Experience, Projects, Python là 3 Features có sự phân biệt rõ ràng nhất vì "Experience - Hired" "Projects - Hired" "Python - Hired" Box không chồng nhau đường trung vị khác nhau tuy nhiên vẫn có 1 số ít trường hợp Outlier nhưng không sao vì sẽ có 1 features mạnh bù vào cho trường hợp pass và 1 số features yếu kéo xuống cho trường hợp ứng viên không pass.
    2. Histogram
        Phần này không biết báo cáo thế nào ( mục tiêu muốn xem thử số lượng phân bố trên các khoảng như thế nào mà mình không biết phải đưa tham số bins = bao nhiêu để biểu đồ dễ đọc )
5.  Correlation Analysis
    Sử dụng heatmap:

    - Feature Experience và Projects 2 features này có tương quan mạnh đến nhau vì chỉ số tương quan 0.9 ( trực quan vì có màu rất đậm) và cặp features AI và Python có liên quan tương đối mạnh vì chỉ số 0.48 ( Màu grey sáng)
    - feature yếu Education, Docker, Redis, RabbitMQ vì thấy nó ít liên quan tuyến tính với khác feature khác chỉ số thấp và có màu xanh đậm
    - Có mulicollinear không ? ( không biết)

6. Outlier Analysis
    - Có Outlier ở 1 nhiều nơi nhưng có thể chấp nhận được
    ( Còn nhiều điều chưa biết )

7. Kết Luận:
    Chưa làm được

    
