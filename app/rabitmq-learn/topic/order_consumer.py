import pika
import time

RABBITMQ_HOST = "localhost"


def process_message(body):

    message = body.decode()

    print(f"Processing: {message}")

    # giả lập business logic
    time.sleep(2)

    # test error
    if "failed" in message.lower():
        raise Exception("Fake processing error")

    print(f"Done: {message}")


while True:

    try:

        print("Connecting to RabbitMQ...")

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=RABBITMQ_HOST,
                heartbeat=60,
            )
        )

        channel = connection.channel()

        channel.exchange_declare(
            exchange="events_exchange",
            exchange_type="topic",
            durable=True
        )

        result = channel.queue_declare(
            queue="order_events_queue",
            durable=True
        )

        queue_name = result.method.queue

        channel.queue_bind(
            exchange="events_exchange",
            queue=queue_name,
            routing_key="order.#"
        )

        # fair dispatch
        channel.basic_qos(prefetch_count=1)

        def callback(ch, method, properties, body):

            try:

                process_message(body)

                # ACK SUCCESS
                ch.basic_ack(
                    delivery_tag=method.delivery_tag
                )

                print("ACK sent")

            except Exception as e:

                print("Processing error:", e)

                # reject + requeue
                ch.basic_nack(
                    delivery_tag=method.delivery_tag,
                    requeue=True
                )

                print("Message requeued")

        channel.basic_consume(
            queue=queue_name,
            on_message_callback=callback,
            auto_ack=False
        )

        print("Waiting order events...")

        channel.start_consuming()

    except pika.exceptions.AMQPConnectionError:

        print("RabbitMQ disconnected. Reconnecting in 5 seconds...")

        time.sleep(5)

    except KeyboardInterrupt:

        print("Consumer stopped")

        break

    except Exception as e:

        print("Unexpected error:", e)

        time.sleep(5)