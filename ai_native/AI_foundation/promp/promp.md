
Prompt chính là...
Tham số (input) để "lập trình" cách Transformer suy luận.


Prompt chỉ nói với Transformer:
- > "Trong lần suy luận này, hãy làm theo cách này."

1. Prompt là cách AI Engineer "lập trình" Transformer mà không cần train lại model.
2. Cùng một model nhưng Prompt khác có thể cho kết quả rất khác.
3. Trong dự án thật, Prompt được quản lý như source code, không phải viết ngẫu hứng mỗi lần.


- > Một Prompt tốt thường có 3 thành phần.
    ① AI là ai?
        Đây gọi là. Role.
        Ví dụ: Bạn là Senior Backend Engineer, Bạn là Technical Lead.

    ② Nhiệm vụ là gì?
        Ví dụ: Giải thích.
                So sánh.
                Dịch.
                Viết code.
                Review code.

    ③ Kết quả mong muốn
        Ví dụ:
            - Ngắn gọn.

            - Có ví dụ.

            - Có code.

            - Không quá 300 từ.

            - Trả về JSON.


- * Một Prompt thực tế
    Ví dụ:
    Bạn là Senior Backend Engineer.

    Nhiệm vụ:

    Giải thích cho Junior Developer.

    Yêu cầu:

    - Dễ hiểu.
    - Có ví dụ thực tế.
    - Có code Python nếu phù hợp.
    - Không dùng thuật ngữ quá hàn lâm.

    Câu hỏi:
    Redis dùng để làm gì?

Đây là điều thực tế họ làm:
    SYSTEM_PROMPT = """
            Bạn là Senior Backend Engineer.
            Giải thích dễ hiểu.
            Có ví dụ.
            Có code.
        """

        response = client.responses.create(
            model="gpt-5",
            input=f"{SYSTEM_PROMPT}\n\n{user_question}"
        )