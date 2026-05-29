import json
import pika
from datetime import datetime, timezone

from sqlmodel import Session, text
from app.database import engine
from app.config import settings

from app.models.notification_model import NotificationModel
from app.websocket.connection_manager import manager

connection = pika.BlockingConnection(
        pika.URLParameters(settings.RABBITMQ_URL)
    )

channel = connection.channel()

channel.exchange_declare(
        exchange="task_events", 
        exchange_type="fanout",
        durable=True
    )

result = channel.queue_declare(
        queue="notification_queue", 
        durable=True
    )

queue_name = result.method.queue

channel.queue_bind(
        exchange="task_events",
        queue=queue_name
    )

def callback(ch, method, properties, body):

    try:
        payload = json.loads(body)

        data = payload["data"]
        print('\n \n \n data \n \n \n ' , data)

        with Session(engine) as session:
            statement_insert = text("""
                INSERT INTO notificationmodel
                (user_id, title, message, is_read, created_at)
                VALUES
                (:user_id, :title, :message, :is_read, :created_at)
            """).bindparams(
                user_id=data["user_id"],
                title=data["title"],
                message=data["task_name"],
                is_read=False,
                created_at= datetime.now(timezone.utc)
            )

            session.exec(statement_insert)
            session.commit()
        print(
            "\nNotification saved"
        )
        ch.basic_ack(
            delivery_tag=method.delivery_tag
        )

    except Exception as e:

        print(
            "\nNotification consumer error:\n",
            e
        )

        ch.basic_nack(
            delivery_tag=method.delivery_tag,
            requeue=True
        )


channel.basic_consume(
        queue=queue_name,
        on_message_callback=callback
    )

print("Notification consumer started...")

channel.start_consuming()