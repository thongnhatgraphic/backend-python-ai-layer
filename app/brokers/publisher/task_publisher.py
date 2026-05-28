import pika
import json
from app.brokers.rabbitmq import get_rabbitmq_channel

def publish_task_event(event_type: str, data: dict):
    channel, connection = get_rabbitmq_channel()

    payload = {
        "event": event_type,
        "data": data
    }
    
    print("\n\n\n\n payload is \n\n\n\n", payload)
    print("\n\n\n\n payload is dumps \n\n\n\n", json.dumps(payload, default=str).encode())

    channel.basic_publish(
        exchange="task_events",
        routing_key="",
        body=json.dumps(payload, default=str).encode(),
        properties=pika.BasicProperties(
            delivery_mode=2
        )
    )

    connection.close()