import pika
import json

# ✅ Work Queue
# ✅ ACK
# ✅ Durable Queue ( it means the queue will survive a server restart )
# ✅ Persistent Message ( it means the message will survive a server restart )
# ✅ Reconnect
# ✅ Exponential Backoff ( it means the producer will retry to send the message after a certain time interval )
# ✅ Fair Dispatch ( it means the producer will send the message to the broker in a round-robin fashion )
# ✅ Backpressure


# Tóm tắt DIRECT
# Dùng khi:

# ✅ biết target logic
# ✅ cần route chính xác
# ✅ task-specific workers
# ✅ command-style messaging


# FANOUT EXCHANGE
# Mindset:
# "Tôi publish event thôi.
# Ai follow thì đều biết."

# DIRECT = "Tao chọn người nhận"
# FANOUT = "Tao chỉ phát thông báo"

# DIRECT
# # Hãy tự hỏi:
# # "Tôi có đang chọn người xử lý không?"
# # Nếu CÓ:
# # => DIRECT

# FANOUT
# Hãy tự hỏi:
# "Tôi chỉ đang thông báo một sự kiện?"

connection = pika.BlockingConnection(
    pika.ConnectionParameters("localhost")
)

channel = connection.channel()

# # Create direct message exchange
# channel.exchange_declare(
#     exchange='notification_exchange',
#     exchange_type='direct'
# )

# # send message email
# channel.basic_publish(
#     exchange = 'notification_exchange',
#     routing_key='email',
#     body='Send email to user'.encode()
# )

# print("[✅] Message sent to email queue")

# # send message sms
# channel.basic_publish(
#     exchange= 'notification_exchange',
#     routing_key='sms',
#     body='Send sms to user'.encode()
# )

# print("[✅] Message sent to sms queue")


# -----logs exchange , exchange_type = "fanout"
channel.exchange_declare(
    exchange="logs_exchange",
    exchange_type="fanout"
)
message = "User created successfully"

channel.basic_publish(
    exchange="logs_exchange",
    routing_key="",
    body=message.encode()
)

print("Log message sent successfully")


connection.close()

