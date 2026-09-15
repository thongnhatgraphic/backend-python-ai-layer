X = [
    [2,1],
    [1,1],
    [0,2]
]

Trong PyTorch. Không ai gọi X là list, Không ai gọi X là matrix
==> Họ gọi là "Tensor"

Scalar ( Vô hướng)
↓
Vector
↓
Matrix
↓
Tensor

Ví dụ: 
- Scalar = 5 Shape = ()
- Vector = [2,1] Shape = (2,)
- Matrix = [
 [2,1],
 [1,1],
 [0,2]
] Shape = (3,2)

Tensor 3 chiều: 
Ví dụ: 
Batch
Sentence
Embedding

Shape (4,3,2):
Nghĩa là: 
        4 câu

        Mỗi câu 3 token

        Mỗi token embedding 2 chiều
Shape.
(batch_size,
 sequence_length,
 embedding_dim)

Q = X @ WQ

WQ không làm tăng số token.

    Nó cũng không giảm số token.

    Nó chỉ biến đổi cách biểu diễn của từng token.

    Đây chính là điều chúng ta đã nói từ những bài đầu:

    Embedding là "bản mô tả" của token.

    Sau khi qua WQ:

    Token vẫn là token đó.

    Nhưng bây giờ nó mang vai trò Query.


---------------------------------------------------------------------
Multi-Head Attention
Roadmap
Embedding
    ✅
    ↓
    Q, K, V
        ✅
    ↓
    Attention
        ✅
    ↓
    Matrix
        ✅
    ↓
    Tensor
        ✅
    ↓
    ⭐⭐ Head là gì? ⭐⭐
    ↓
    Multi-Head Attention
    ↓
    Transformer Block

Head là gì?
Đến đây mình mới đưa định nghĩa.
Một Head là một cơ chế Self-Attention độc lập, có bộ trọng số Q, K, V riêng và học một cách nhìn riêng về cùng một chuỗi token.

"Transformer có 12 heads."

Một người
        ↓
        Làm mọi việc
    ||
So với
    ||
12 người
        ↓
        Mỗi người giỏi một phần
        ↓
        Ghép kết quả lại