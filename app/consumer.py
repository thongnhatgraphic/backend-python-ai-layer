import pika
import time

connection = pika.BlockingConnection(
    pika.ConnectionParameters("localhost")
)

channel = connection.channel()

channel.queue_declare(queue="tasks_queue")

def callback(ch, method, properties, body):
    message = body.decode()

    print("Received:", message)
    # Simulate task is Complicated
    time.sleep(3)

    print("Done", message)

    # Send ACK
    ch.basic_ack(
        delivery_tag=method.delivery_tag
    )

channel.basic_consume(
    queue="tasks_queue",
    on_message_callback=callback,
    auto_ack=False
)

print("Waiting for tasks...")


channel.start_consuming()