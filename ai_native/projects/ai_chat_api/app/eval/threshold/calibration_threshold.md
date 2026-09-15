1. Làm sao biết nên thử những threshold nào với một model bất kỳ?

Score của Ettin là continuous:
6.01
6.17
6.83
7.24
...

Nên việc thử:
[0, 1, 2, ..., 8] chỉ nhằm tìm vùng đáng quan tâm.

Với model khác, ta không có quyền giả định: 0 → 8 hay quyết định threshold = 6

Bởi vì score scale là model-specific.

Quy trình production đúng
    Ta đi theo 3 bước:
    1. Collect score distribution
            ↓
    2. Coarse sweep ( quét thô)
            ↓
    3. Fine sweep quanh vùng tốt ( quét mịn)


Bước 1 — Collect score distribution
relevant documents
non-relevant documents

Relevant:
    min = -1.2
    P25 = 2.7
    median = 4.8
    P75 = 7.1
    max = 12.4

Non-relevant:
    min = -5.0
    P25 = -0.8
    median = 1.2
    P75 = 3.4
    max = 8.2

Lúc này bạn đã biết score chủ yếu nằm trong khoảng nào.

Bước 2 — Coarse sweep
Ta thử những mốc rộng, ví dụ:
-2
0
2
4
6
8
10

Tìm vùng mà Recall/Precision bắt đầu trade-off mạnh.

threshold 2 → recall 99%, precision 22%
threshold 4 → recall 96%, precision 38%
threshold 6 → recall 87%, precision 52%
threshold 8 → recall 64%, precision 68%

Bước 3 — Fine sweep
Lúc đó mới test:
    4.0
    4.2
    4.4
    4.6
    4.8
    5.0
    5.2
    ...
    6.0


2. Vậy dựa vào đâu để tạo giả thuyết threshold cho model mới?
Không dựa vào tên model. Dựa vào score distribution trên validation/evaluation data của chính bài toán.