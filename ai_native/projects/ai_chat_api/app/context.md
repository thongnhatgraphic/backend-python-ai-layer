1. Persona Context
Ví dụ:
Tên là Nhất
Là Backend Developer
Đang học AI
Thích Python
Không thích giải thích quá dài

Thông tin về người dùng.

2. Conversation Context
5 message gần nhất.

Ngữ cảnh hiện tại.

3. Task Context ( Bối cảnh nhiệm vụ)
Đang debug RabbitMQ.

Mục tiêu hiện tại.

- > "Một AI tốt sẽ luôn có ít nhất ba tầng context này." < -
System
Persona Context
Task Context
Conversation Context

=====================Ứng dụng trong dự án 

Hiện tại:
ConversationMemory
↓
Conversation Context

MemoryStore.search()
↓
Persona Context

Tool Calling
↓
Task Context

Lúc ghép lại:
            System
            |
            Persona
            |
            Task
            |
            Conversation
            |
            Current User Message


1. Identity Memory      ⭐⭐⭐⭐⭐ Bộ nhớ nhận dạng
2. Preference Memory    ⭐⭐⭐⭐☆ 
3. Project Memory       ⭐⭐⭐☆☆
4. Temporary Memory     ⭐☆☆☆☆

