import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters("localhost")
)

channel = connection.channel()

channel.exchange_declare(
    exchange='events_exchange',
    exchange_type='topic'
)

events = [
    ("user.created", "User creted"),
    ("user.updated", "User updated"),
    ("user.deleted", "User deleted"),
    ("order.created", "Order created"),
    ("order.payment.failded", "Order payment failded")
]

for routing_key, message in events:
    channel.basic_publish(
        exchange='events_exchange',
        routing_key=routing_key,
        body=message.encode()
    )
    print(f"Sent [{routing_key}]")
    print(f"Sent {message} to {routing_key}")

connection.close()