import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters("localhost")
)

channel = connection.channel()

channel.exchange_declare(
    exchange="logs_exchange",
    exchange_type="fanout"
)

result = channel.queue_declare(
    queue = "",
    exclusive=True
)

print('==========>', result.method)
queue_name = result.method.queue

channel.queue_bind(
    exchange="logs_exchange",
    queue=queue_name
)

def callback(ch, method, properties, body):

    print("Console logger:", body.decode())

channel.basic_consume(
    queue=queue_name,
    on_message_callback=callback,
    auto_ack=True
)

print("Waiting for logs...")

channel.start_consuming()