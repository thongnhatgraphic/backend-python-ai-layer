Bây giờ hãy nhìn toàn bộ bức tranh

Đây là điều mình muốn bạn thấy.

Layer 1
dot_product()

↓

tính độ giống nhau.

Layer 2
attention_scores()

↓

điểm số Attention.

Layer 3
softmax()

↓

chuyển thành xác suất.

Layer 4
weighted_sum()

↓

tạo output vector.

Layer 5
attention()

↓

xử lý 1 Query.

Layer 6
self_attention()

↓

xử lý toàn bộ câu.

Đến đây chúng ta đã hoàn thành Single Head Self-Attention.


Multi-Head Attention (1 câu nhiều góc nhìn)
Cùng một câu đi vào nhiều Head.
Mỗi Head có bộ WQ, WK, WV riêng.
Mỗi Head tạo ra một cách biểu diễn (representation) khác nhau cho từng token.
Concatenate: ghép các representation của cùng một token lại.
Output Projection (WO): học cách kết hợp chúng thành một vector cuối cùng.

Self Attention
        │
        ▼
Head 1      |

Head 2      | -> Multi-head Attention

Head 3      |
        │
        ▼
Concatenate
        │
        ▼
WO
        │
        ▼
Representation mới

Nếu bỏ WO đi, các Head gần như chỉ đứng cạnh nhau mà chưa tương tác để tạo thành một biểu diễn thống nhất.

                    Input
                      │
                      ▼
      ✅ Multi-Head Attention
                      │
                      ▼
             ⬜ Add & Norm
                      │
                      ▼
          ⬜ Feed Forward
                      │
                      ▼
             ⬜ Add & Norm
                      │
                      ▼
                    Output

Add là gì?
input "X" Sau Multi-Head ta có "attention_output"
output = x + attention_output
Đây chính là Residual Connection

result = old_data + new_data
    - giữ lại thông tin gốc
    - giúp gradient truyền tốt hơn khi train rất nhiều layer.
Norm là gì?
    x + attention_output sau đó ra 
    [   1000,
        0.0002,
        -500
    ] chuẩn hoá lại 
    [-1.2,
    0.3,
    0.9] Layer Normalization

Feed Forward là gì?
    để mỗi token tự tinh chỉnh biểu diễn của chính nó dựa trên ngữ cảnh vừa thu được.

Sumary:
    Attention trả lời câu hỏi:
    "Token này nên học gì từ các token khác?"

    Sau khi đã có câu trả lời đó...

    Feed Forward trả lời câu hỏi:
    "Bây giờ mình nên biểu diễn token này như thế nào?"
