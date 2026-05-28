import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters("localhost")
)

channel = connection.channel()

channel.exchange_declare(
    exchange="events_exchange",
    exchange_type="topic"
)

result = channel.queue_declare(
    queue="",
    exclusive=True
)
queue_name = result.method.queue

channel.queue_bind(
    exchange="events_exchange",
    queue=queue_name,
    routing_key="user.*"
)

def callback(ch, method, properties, body):

    print("USER EVENT:", body.decode())

channel.basic_consume(
    queue=queue_name,
    on_message_callback=callback,
    auto_ack=False
)

print("Waiting user events...")

channel.start_consuming()