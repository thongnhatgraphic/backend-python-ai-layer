| Công cụ      | Trả lời câu hỏi gì?                             |
| ------------ | ----------------------------------------------- |
| `describe()` | Trung bình, min, max, quartile là gì?           |
| `groupby()`  | Hai nhóm khác nhau thế nào?                     |
| Boxplot      | Dữ liệu tập trung ở đâu? Có Outlier không?      |
| Histogram    | Toàn bộ phân phối của Feature trông ra sao?     |
| Correlation  | Feature có quan hệ tuyến tính với Target không? |


| Câu hỏi cần trả lời                  | Biểu đồ phù hợp              |
| ------------------------------------ | ---------------------------- |
| Feature phân bố thế nào?             | Histogram                    |
| Hai nhóm có khác nhau không?         | Boxplot                      |
| Hai biến có quy luật không?          | Scatter Plot                 |
| Liên quan tuyến tính mạnh bao nhiêu? | Correlation Matrix / Heatmap |


        Business Question
                │
                ▼
        Chọn Visualization phù hợp
                │
                ▼
        Matplotlib / Seaborn vẽ biểu đồ
                │
                ▼
        Con người đọc biểu đồ
                │
                ▼
        Business Insight

-------------------------------------------------------------
Bắt đầu 1 vấn đề: 
1. Hiểu Business
↓
2. Đọc Dataset
↓
3. Hiểu cấu trúc dữ liệu
    - Shape
    - Columns
    - Dtype
↓
4. Kiểm tra chất lượng dữ liệu
    - Missing Values
    - Duplicate
    - Invalid Values
↓
5. Statistics
    - Mean
    - Median
    - Std
    - Min
    - Max
↓
6. Hiểu Target
    - Có cân bằng không?
↓
7. Hiểu từng Feature
    - Histogram
    - Boxplot
↓
8. Hiểu mối quan hệ
    - Scatter Plot
    - Correlation
    - Heatmap
↓
9. Kiểm tra Outlier
↓
10. Kết luận
↓
11. Quyết định có train model hay không