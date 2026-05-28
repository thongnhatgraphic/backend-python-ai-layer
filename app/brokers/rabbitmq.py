import pika
from app.config import settings

# Solution 1
# credentials = pika.PlainCredentials(
#     username="guest",
#     password="guest"
# )

# params = pika.ConnectionParameters(
#     host="172.17.0.3",
#     port=5672,
#     credentials=credentials
# )

# Solution 2

def get_rabbitmq_channel():
    params = pika.URLParameters(settings.RABBITMQ_URL)

    connection = pika.BlockingConnection(params)

    channel = connection.channel()

    channel.exchange_declare(
        exchange="task_events",
        exchange_type="fanout",
        durable=True
    )

    return channel, connection