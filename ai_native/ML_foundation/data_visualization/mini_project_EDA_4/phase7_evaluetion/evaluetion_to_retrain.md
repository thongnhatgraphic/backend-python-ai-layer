🔥 Phase 7 Evaluation

    ✅ Accuracy

    ✅ Confusion Matrix

    ✅ Precision

    ✅ Recall

    🔥 NOW → F1 Score

    Error Analysis:

        Export Error Cases
        ↓
        EDA trên Error Cases


---------------------------------------------
Model sai
            ↓
            Lọc Error Cases
            ↓
            Đọc từng record
            ↓
            Grouping
            ↓
            Tìm Pattern
            ↓
            Business Discussion
            ↓
            Feature Engineering
                                ↓
                                Agreegation
                                Ratio.
                                Interaction.
                                Threshold.
            
            ↓
            Retrain


| Quan sát                            | Bằng chứng                | Giả thuyết                                                                 |
| ----------------------------------- | ------------------------- | -------------------------------------------------------------------------- |
| Error có Experience cao hơn dataset | Mean 11.8 vs 6.5          | Model xử lý nhóm senior chưa tốt hoặc feature chưa phản ánh đúng seniority |
| Error có Python cao hơn dataset     | Mean 80.7 vs 74.5         | Model chưa tận dụng tốt kỹ năng mạnh về Python                             |
| BackendSkill không chứa Experience  | Thiết kế feature hiện tại | Có thể cần một feature mới kết hợp Experience với BackendSkill             |
  Error có Projects cao hơn dataset   | mean 12.1 vs 7.4          | Model xử lý nhóm nhiều project chưa tốt
  Error có Docker cao hơn dataset     | mean 0.3 vs 0.2           | Model chưa tận dụng tốt những người có thêm kỹ năng biết về docker
  Error có Redis cao hơn dataset      | mean 0.41 vs 0.2          | Model chưa tận dụng tốt những người có thêm kỹ năng biết về Redis
  Error có AI cao hơn dataset         | mean 0.35 vs 0.14         | Model chưa tận dụng tốt những người có thêm kỹ năng biết về AI
