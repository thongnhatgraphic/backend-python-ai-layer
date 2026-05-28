import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters("localhost")
)

channel = connection.channel()

channel.exchange_declare(
    exchange="notification_exchange",
    exchange_type="direct"
)

channel.queue_declare(
    queue="sms_queue"
)

channel.queue_bind(
    exchange="notification_exchange",
    queue="sms_queue",
    routing_key="sms"
)

def callback(ch, method, properties, body):

    print("SMS:", body.decode())

channel.basic_consume(
    queue="sms_queue",
    on_message_callback=callback,
    auto_ack=True
)

print("Waiting for sms messages...")

channel.start_consuming()