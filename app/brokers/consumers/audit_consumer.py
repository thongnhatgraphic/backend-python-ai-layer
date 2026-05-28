import json
import pika

from sqlmodel import Session

from app.database import engine
from app.models.auditlog_model import AuditLog
from app.models.user_model import UserModel
from app.config import settings

connection = pika.BlockingConnection(pika.URLParameters(settings.RABBITMQ_URL))

channel = connection.channel()

channel.exchange_declare(exchange="task_events", exchange_type="fanout", durable=True)

result = channel.queue_declare(queue="", exclusive=True)

queue_name = result.method.queue

channel.queue_bind(exchange="task_events", queue=queue_name)


def callback(ch, method, properties, body):

    payload = json.loads(body)

    print("\n\n\n\n AUDIT EVENT: \n\n\n\n ", payload)

    with Session(engine) as session:
        data = payload["data"]

        log = AuditLog(
            event_type=payload["event"],
            payload=data["task_name"],
            user_id=data["user_id"],
            entity_id=data["task_id"],
        )

        session.add(log)

        session.commit()

    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(queue=queue_name, on_message_callback=callback)

print("Audit consumer started...")

channel.start_consuming()
