[[ 0.02298243  0.91172046  0.21797961  4.31880106 -0.02109342  1.43395756
   0.83392999  0.94699788  0.97847265  1.21481655  1.46878321 -1.24777641
   0.88533182]]
[-10.67711984]
['Age', 'English', 'Experience', 'Projects', 'Education', 'Python', 'Docker', 'Redis', 'RabbitMQ', 'AI', 'BackendSkill', 'ProjectCompletionExperience', 'InternationalExperience']

| Feature                     |     Weight |
| --------------------------- | ---------: |
| Age                         |  **0.023** |
| English                     |  **0.912** |
| Experience                  |  **0.218** |
| Projects                    |  **4.319** |
| Education                   | **-0.021** |
| Python                      |  **1.434** |
| Docker                      |  **0.834** |
| Redis                       |  **0.947** |
| RabbitMQ                    |  **0.978** |
| AI                          |  **1.215** |
| BackendSkill                |  **1.469** |
| ProjectCompletionExperience | **-1.248** |
| InternationalExperience     |  **0.885** |

Nếu Projects tăng (sau khi đã StandardScaler), xác suất Hired tăng rất mạnh.

Age 0.023 Gần như bằng 0.
Education -0.021 Gần như bằng 0.
Age Education Không giúp model nhiều.

BackendSkill 1.469 khá cao. 

Intercept = -10.677 nó như là Điểm xuất phát. Nếu mọi feature sau khi scale đều ở mức trung bình (xấp xỉ 0), thì: z ≈ -10.677 Điều đó có nghĩa là model có xu hướng mặc định dự đoán "không được tuyển", và chỉ khi tổng đóng góp từ các feature đủ lớn thì mới vượt qua ngưỡng để dự đoán "được tuyển".