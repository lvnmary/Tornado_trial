import pika
import json
import psycopg2

def save_to_db(data):
    conn = psycopg2.connect('dbname=appeals_db user=postgress password=yourpassword host=db')
    cursor = conn.cursor()
    query = """
    INSERT INTO appeals (last_name, first_name, middle_name, phone, message)
    VALUES (%s, %s, %s, %s, %s);
    """
    cursor.execute(query, (data['last_name'], data['first_name'], data['middle_name'], data['phone'], data['message']))
    cursor.commit()
    cursor.close()
    conn.close()

connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()
channel.queue_declare(queue='appeals')

def callback(ch, method, properties, body):
    data = json.loads(body)
    save_to_db(data)

channel.basic_consume(queue='appeals', on_message_callback=callback, auto_ack=True)
channel.start_consuming()