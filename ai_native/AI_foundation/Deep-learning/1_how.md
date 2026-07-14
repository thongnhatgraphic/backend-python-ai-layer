Raw Data

↓

Layer 1 học Feature đơn giản

↓

Layer 2 học Feature phức tạp hơn

↓

Layer 3 học Concept

↓

Output
---------------------------------------------------------------------------------------

Neural Network không mạnh vì có nhiều Neuron.

Mà mạnh vì:
Nhiều Layer giúp nó học ra những biểu diễn (representations) ngày càng trừu tượng từ dữ liệu thô.
-------------------------------------------------------------------------------------------


1. > Nếu Neural Network tự học feature, thì ai dạy nó biết "tai mèo", "mắt mèo", "đầu mèo"?

    Hay nói cách khác:

    Neuron học từ đâu?

                                Machine Learning
                                │
                                ▼
                            Feature do Human tạo
                                │
                                ▼
                            Neural Network
                                │
                                ▼
                            Neuron
                                │
                                ▼
                            🔥 Neuron học như thế nào? (NOW)
                            
"Loss Function" Phân biệt được.Sai một chút. Sai rất nhiều.
AI dự đoán -> 0.49. Đáp án "1" Sai ít
AI khác. Dự đoán 0.0001 Đáp án "1" Sai nhiều

Neuron cần biết --> "Mình sai bao nhiêu."
Vì chỉ khi biết độ lớn của sai số, nó mới biết nên điều chỉnh trọng số mạnh hay nhẹ.

Deep Learning cải thiện bằng cách mô hình tự điều chỉnh weight để tạo ra representation (biểu diễn) tốt hơn.

                        AI chỉ biết.
                            Input
                            ↓
                            Neuron
                            ↓
                            Neuron
                            ↓
                            Neuron
                            ↓
                            Prediction
                            ↓
                            Loss ??????????????????????
                            ↓
                        AI biết mình sai
                            ↓                        
            AI không biết sai features nào ????

Backpropagation được phát minh để giải quyết vấn đề gì?

                            Prediction sai                    
                            ↓

                            Layer cuối biết

                            ↓

                            Báo Layer trước

                            ↓

                            Layer trước sửa

                            ↓

                            Báo Layer trước nữa

                            ↓

                            Layer trước nữa sửa

                            Loss

                ▲
                │
        *       │
      *         │
    *           │
  *             │
*               │
────────────────────────► Weight

Gradient Descent.

Công thức:
    W(old) (Weight hiện tại.)
    ∇L ( Hướng dốc nhất. )
    η (đọc là eta)

Learning Rate = 0 Không đi.
Gradient = 0 Đang ở đáy (hoặc một điểm mà bề mặt phẳng).
Learning Rate = 1000 bước 1 phát bỏ qua luôn đáy


RNN
"The animal didn't cross the street
because it was too tired." It là the animal

Word1  ←──────────────┐
Word2  ←──────┐       │
Word3         │       │
Word4 ───────►│──────►│
Word5 ───────►│──────►│
Word6 ───────►│──────►│

Machine Learning. 
                Human
                ↓
                Feature Engineering

Deep Learning.
                Raw Data
                ↓
                Feature Learning Representation( đại diện)

    Transformer.
                Memory
                ↓
                Attention
                ↓
                Context

---------------------------------------------------------------------------------------
                Machine Learning
                │
                ▼
            Neural Network
                │
                ▼
            Transformer
                │
                ▼
            Attention
                │
                ▼
            🔥 Embedding (Hôm nay)
                │
                ▼
                LLM ----------------
                                    Word
                                    ↓
                                    Embedding Vector

━━━━━━━━━━━━━━━━━━━━━━
🔥 LLM Foundation   ← NOW
━━━━━━━━━━━━━━━━━━━━━━
Tokenizer
Context Window
Prompt
Temperature
Hallucination
Function Calling
RAG
AI Agent


                    USER
                      │
                      ▼
            "Giải thích RabbitMQ"

                      │
                      ▼
- >             ① Tokenizer
                (Cắt câu thành token)
            là người phiên dịch đầu tiên.                
                    - Input: Hello ChatGPT
                    - Output: ["Hello", "Chat", "GPT"]
                    Tokenizer vừa cắt được Token.
                    Nhưng Computer không đọc chữ. Nó đọc số
                    Tokenizer tra trong một bảng.
                        ✔ Cắt Text
                        ✔ Sinh Token
                        ✔ Đếm Token

                      │
                      ▼
- >                  ② Token IDs
            (Đổi token thành số)
                    Ví dụ: Hello → 15496 Chat → 7421 GPT → 38
                            Output: [15496,7421,38]

                      │
                      ▼
- >                  ③ Embedding
        (Đổi số thành vector ý nghĩa)
                    - "15496 chẳng có nghĩa gì."
                    - Nó chuyển đổi thành [0.31,
                                        -0.81,
                                        ...
                                        768 số]
                    - Nghĩa là Đổi Token ID thành một biểu diễn mà Transformer có thể hiểu                   


                      │
                      ▼
- >                  ④ Transformer 
            (Hiểu ngữ cảnh + suy luận)
                    - Transformer nhận rất nhiều vector
                    - Ví dụ. Hello Chat GPT -> 3 vector.
                    - Không sinh câu trả lời ngay. 
                    - Nó chỉ làm một việc => "Hiểu ngữ cảnh."
                                                    │
                                                    ▼
                                            Attention diễn ra
                                                    │
                                                    ▼                           
                                                Embedding
                                                    ↓
                                                Hiểu Context

                      │
                      ▼
- >              ⑤ Predict Next Token
            (Đoán token tiếp theo)
                    - Nó chỉ đoán 1 Token tiếp theo.
                    Ví dụ: The capital of France is ...
                    Transformer nghĩ "Paris"
                    Input 1 token mới ví dụ Transformer vừa sinh: 4832

                      │
                      ▼
- >            ⑥ Detokenizer
            (Đổi token thành chữ)
                    - Người dùng đâu đọc được 4832
                    - Detokenizer Tra ngược. 4832 -> Paris
                      │
                      ▼
- >                USER THẤY

        "RabbitMQ là một Message Broker..."


- >  Tokenizer
        Vai trò:
        Cắt Text thành Token và đếm Token.

        Input:
        Text

        Output:
        Token

        Output dùng bởi:
        Token IDs Generator

- > Token IDs
        Vai trò:
        Đổi Token thành số 

        Input:
        Token

        Output:
        Token IDs

        Output dùng bởi:
        Embedding

- > Embedding
        Vai trò:
        Đổi Token ID thành Vector

        Input:
        Token ID

        Output:
        Vector

        Output dùng bởi:
        Transformer

- > "Đây gọi là Dependency. 1 Component luôn phục vụ Component kế tiếp"

| Thành phần | Vai trò              | Input     | Output    | Ai dùng Output?  | Nếu lỗi thì sao?               |
| ---------- | -------------------- | --------- | --------- | ---------------- | ------------------------------ |
| Tokenizer  | Cắt text thành token | Text      | Token     | Token ID Encoder | Không cắt được text            |
| Token IDs  | Đổi token thành số   | Token     | Token IDs | Embedding        | Embedding không chạy           |
| Embedding  | Đổi ID thành vector  | Token IDs | Vector    | Transformer      | Transformer không hiểu dữ liệu |

① Tokenizer không hiểu ngôn ngữ.
    Nó chỉ chuẩn hóa đầu vào.

② Tokenizer tạo ra Token.
    Không phải câu trả lời.
    Không phải Vector.

③ Tokenizer là nơi AI Engineer thường gặp khi:
    Đếm Token
    Tính chi phí API
    Chia Chunk cho RAG
    Kiểm tra Context Window



| Thuộc tính     | Giá trị                                |
| -------------- | -------------------------------------- |
| Vai trò        | Đổi Token ID thành Vector mang ý nghĩa |
| Input          | Token IDs                              |
| Output         | Embedding Vector                       |
| Ai dùng Output | Transformer                            |
| Nếu lỗi        | Transformer hiểu sai ngữ cảnh          |
| Khi đi làm     | RAG, Vector Database, Semantic Search  |
