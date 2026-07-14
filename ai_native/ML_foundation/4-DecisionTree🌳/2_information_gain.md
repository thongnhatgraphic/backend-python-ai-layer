Bạn có 100 CV.

Bạn hỏi. Experience >= 3?
- Nếu sau câu hỏi này.

Nhóm trái.                  Nhóm phải.

NO NO NO NO NO              YES YES YES YES

1 câu hỏi giải quyết luôn được vấn đề


Ví dụ khác: YES NO YES NO YES NO YES NO

* Có những câu hỏi:
    Hỏi xong là xong.
* Có những câu hỏi:
    Hỏi xong vẫn chẳng biết gì.

    - # Information Gain hỏi: "Câu hỏi này giúp giảm hỗn loạn được bao nhiêu?"
            Entropy
                ↓
        Đo độ hỗn loạn

        Information Gain
                ↓
        Đo lượng hỗn loạn bị giảm

Information Gain luôn là: Entropy trước - Entropy sau

| Logistic Regression   | Decision Tree               |
| --------------------- | --------------------------- |
| Tối thiểu hóa Loss    | Tối đa hóa Information Gain |
| Chỉnh Weight          | Chọn Feature + Ngưỡng chia  |
| Dùng Gradient Descent | Thử tất cả các cách chia    |

- Hai thuật toán rất khác nhau về cách làm.
- Nhưng mục tiêu đều giống nhau: Giảm sai và tạo ra mô hình dự đoán tốt hơn.

Ví dụ:
        | Feature    | Information Gain |
        | ---------- | ---------------: |
        | Age        |             0.18 |
        | English    |             0.42 |
        | Experience |             0.29 |


                 English >= 750?
                  /            \
               No               Yes
              /                  \
     Age >= 25?              Experience >= 5?
        /     \                /           \
      ...     ...            ...          ...