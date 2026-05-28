import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters("localhost")
)

channel = connection.channel()

channel.exchange_declare(
    exchange = ' notification_exchange',
    exchange_type='direct'
)

# declare queue
channel.queue_declare(
    queue='email_queue'
)

# binding queue to exchange
channel.queue_bind(
    exchange='notification_exchange',
    queue='email_queue',
    routing_key='email'
)

def callback(ch, method, properties, body):
    print("Email", body.decode())
    
    
channel.basic_consume(
    queue='email_queue',
    on_message_callback=callback,
    auto_ack=True
)

print("Waiting for email messages...")

channel.start_consuming()