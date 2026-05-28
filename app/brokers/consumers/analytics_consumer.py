import json
import pika

from sqlmodel import Session, text
from app.database import engine
from app.config import settings
from app.models.analytic_model import AnalyticModel
from datetime import datetime, timezone

connection = pika.BlockingConnection(pika.URLParameters(settings.RABBITMQ_URL))

channel = connection.channel()

channel.exchange_declare(exchange="task_events", exchange_type="fanout", durable=True)

result = channel.queue_declare(queue="", exclusive=True)

queue_name = result.method.queue

channel.queue_bind(exchange="task_events", queue=queue_name)


def callback(ch, method, properties, body):
    try:
        payload = json.loads(body)

        print("\nAnalytics EVENT:\n", payload)

        data = payload["data"]
        with Session(engine) as session:
            get_analytic_statement = text("""
                Select * from analyticmodel
                where user_id=:user_id
            """).bindparams(user_id=data["user_id"])

            analytic = session.exec(get_analytic_statement).first()

            print("\n analytic \n", analytic)

            if analytic is None:
                count_task_statemen = text("""
                    Select count(*) from task
                    where user_id=:user_id
                """).bindparams(user_id=data["user_id"])
                result_count = session.exec(count_task_statemen).first()


                print("\n result_count \n", result_count[0])

                total_tasks_created = (
                    result_count[0] if result_count is not None else 0
                )

                insert_statement = text("""
                    INSERT INTO analyticmodel(user_id, total_tasks_created, updated_at)
                    VALUES(:user_id, :total_tasks_created, :updated_at)
                """).bindparams(
                    user_id=data["user_id"],
                    total_tasks_created=total_tasks_created,
                    updated_at=datetime.now(timezone.utc),
                )
                session.exec(insert_statement)
            else:
                print("\n This case \n")
                update_statement = text("""
                    UPDATE analyticmodel
                    SET
                        total_tasks_created =
                            total_tasks_created + 1,
                        updated_at = :updated_at
                    WHERE user_id = :user_id
                """).bindparams(
                    user_id=data["user_id"], updated_at=datetime.now(timezone.utc)
                )

                session.exec(update_statement)
            
            session.commit()

        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print("\nAnalytics consumer error:\n", e)
        # message quay lại queue
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)


channel.basic_consume(queue=queue_name, on_message_callback=callback)

print("Analytics consumer started...")

channel.start_consuming()
