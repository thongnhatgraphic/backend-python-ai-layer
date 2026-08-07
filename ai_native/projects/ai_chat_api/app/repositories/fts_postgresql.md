1. to_tsvector
Chuyển văn bản trong database thành dữ liệu có thể tìm kiếm.
exp: to_tsvector(content)

2. plainto_tsquery
Chuyển câu hỏi của user thành query.
exp: plainto_tsquery('Tên tôi là gì')


3. @@ Toán tử kiểm tra có match hay không.
exp: to_tsvector(content)
@@
plainto_tsquery(...)

4. ts_rank
Quan trọng nhất.
Cho điểm mức độ liên quan.
Tên tôi là Nhất
★★★★★

Thích Python
★