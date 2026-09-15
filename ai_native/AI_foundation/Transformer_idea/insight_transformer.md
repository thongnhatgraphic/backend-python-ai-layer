Redis
   │
   ▼
Query

   │
   ▼
Dot Product với mọi Key

   │
   ▼
Attention Scores

   │
   ▼
Chia √dk

   │
   ▼
Softmax

   │
   ▼
Attention Weights

   │
   ▼
Nhân với các Value

   │
   ▼
Cộng lại

   │
   ▼
Representation mới
Một Query (1 token) sẽ Attention với toàn bộ Key của câu, rồi lấy Weighted Sum trên toàn bộ Value của câu.
----------------------------------------------------------
sentence = [
    [2, 1],   # Redis
    [1, 1],   # is
    [0, 2],   # fast
]

    Embedding Dimension
             2
      ┌────────────┐
Token │ 2    1     │
Token │ 1    1     │
Token │ 0    2     │
      └────────────┘

Trong AI người ta gọi nó là
    Embedding Matrix

Matrix là gì? 

ví dụ: redis = [2, 1] là  1 vector
sentence là 1 matrix 3 hàng 2 cột

Viết theo dạng bảng.

          Dim1   Dim2
Redis     2      1
is        1      1
fast      0      2


1. Một Query:
Ví dụ. Redis sau khi nhân WQ.

Ta có -> Qredis [0.5 0.8]
Shape ->(1,2)

Hay nếu coi là vector thì thường chỉ nói là: -> (2,)

2. Nhưng cả câu thì sao?
Có ba token ví dụ: Redis

                    is

                    fast
Thì cả ba đều phải biến thành Query.
                    Qredis

                    Qis

                    Qfast
ghép lại
        [
        [0.5 0.8],
        [0.2 0.4],
        [0.9 0.1]
        ]

        Đây mới gọi là

Query Matrix Q
💡 Đây là điểm rất quan trọng:
    Một token → một Query vector.
    Một câu → một Query matrix.


    ----------------------------------------
1. Ma trận Q @ K.T lưu Attention Scores (điểm attention), chưa phải Attention cuối cùng.
Q @ K.T

↓
Attention Scores
↓
chia √dk
↓
Softmax
↓
Attention Weights

2. Row ≡ Query
Giả sử 3 token: "Redis is fast"
Sau khi tạo Q.
[
 qRedis
 qis
 qfast
] ta có shape ( 3, 2)

- Sau đó: Scores = Q @ K.T
    Q có shape (3,2)
    K.T có shape (2,3)

    Kết quả: (3,3)

Điều này có nghĩa.

Mỗi hàng của Scores không còn là vector embedding nữa.
Nó là:
Redis
↓
[
 score(Redis,Redis),
 score(Redis,is),
 score(Redis,fast)
]

3. Column ≡ Key
        Redis   is   fast

             Keys
          R     I     F

Q(R)      4     3     2

Q(I)      2     5     3

Q(F)      1     2     4

Mỗi ô biểu diễn Attention Score giữa Query của một token và Key của một token khác.

Ý nghĩa: 
1. Chuyển đổi các từ trong câu ("Redis", "is", "fast") thành các vector số học có nghĩa e_{Redis}, e_{is}, e_{efast}.
2. Nhân W_{Q} và W_{K}
   Ý nghĩa: Biến các vector Embedding ban đầu thành hai không gian mới là Query (\(Q\)) và Key (\(K\)) thông qua việc nhân với các ma trận trọng số học được (\(W_{Q}\) và \(W_{K}\)).
   
   - \(Q\) (Query): Đóng vai trò là từ "đang đặt câu hỏi" (Từ hiện tại cần tìm sự liên quan).
   - \(K\) (Key): Đóng vai trò là từ "được hỏi" (Mọi từ trong câu để đối chiếu).
