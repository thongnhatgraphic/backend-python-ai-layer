import pika
import json

connection = pika.BlockingConnection(
    pika.ConnectionParameters("localhost")
)

channel = connection.channel()

channel.queue_declare(queue="tasks_queue")

list_range = range(1, 21)

for i in  list_range:
    message = f"Task #{i}"

    encode = message.encode()
    print('----------encode----------', encode)

    channel.basic_publish(
        exchange ="",
        routing_key = "tasks_queue",
        body= message.encode()
    )
    print("Sent: ", message)


connection.close()

