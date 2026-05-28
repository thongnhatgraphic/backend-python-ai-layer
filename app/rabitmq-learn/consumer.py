import pika
import time
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)
RABBITMQ_HOST = "localhost"
QUEUE_NAME = "tasks_queue"

retry_delay = 1
max_retry_delay = 30

while True:
    try:
        logging.info("Connecting to RabbitMQ...")

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=RABBITMQ_HOST
            )
        )

        channel = connection.channel()

        channel.queue_declare(
            queue=QUEUE_NAME,
            durable=True
        )

        # FAIR DISPATCH
        channel.basic_qos(
            prefetch_count=1
        )
        logging.info("Connected successfully")

        # reset retry delay sau khi connect thành công
        retry_delay = 1

        def callback(ch, method, properties, body):

            message = body.decode()

            logging.info(f"Received: {message}")

            # giả lập task nặng
            time.sleep(5)

            logging.info(f"Done: {message}")

            ch.basic_ack(
                delivery_tag=method.delivery_tag
            )

        channel.basic_consume(
            queue=QUEUE_NAME,
            on_message_callback=callback,
            auto_ack=False
        )

        logging.info("Waiting for tasks...")

        channel.start_consuming()

    except KeyboardInterrupt:

        logging.info("Worker stopped manually")
        break

    except Exception as e:

        logging.error(f"Connection error: {e}")

        logging.info(
            f"Reconnecting in {retry_delay} seconds..."
        )

        time.sleep(retry_delay)

        # exponential backoff
        retry_delay = min(
            retry_delay * 2,
            max_retry_delay
        )