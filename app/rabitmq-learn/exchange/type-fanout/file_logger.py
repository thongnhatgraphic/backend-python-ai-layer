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
    queue="",
    exclusive=True # queue will be deleted when connection is closed
)

queue_name = result.method.queue
print('==========>', queue_name)
channel.queue_bind(
    exchange="logs_exchange",
    queue=queue_name
)

def callback(ch, method, properties, body):

    print("File logger:", body.decode())

channel.basic_consume(
    queue=queue_name,
    on_message_callback=callback,
    auto_ack=True
)

print("Waiting for logs...")

channel.start_consuming()