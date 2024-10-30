import tornado
import tornado.ioloop
import tornado.web
import json
import pika


class SubmitHandler(tornado.web.RequestHandler):
    def post(self):
        data = {
            'last_name': self.get_argument('last_name'),
            'first_name': self.get_argument('first_name'),
            'middle_name': self.get_argument('middle_name'),
            'phone': self.get_argument('phone'),
            'message': self.get_argument('message'),
        }

        message = json.dumps(data)

        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        channel = connection.channel()
        channel.queue_declare(queue='appeals')
        channel.basic_publish(exchange='', routing_key='appeals', body=message)

        connection.close()

        self.write('Обращение отправлено')

def make_app():
    return tornado.web.Application([
        (r'/', SubmitHandler),
    ])

if __name__=='__main__':
    app = make_app()
    app.listen(5000)
    tornado.ioloop.IOLoop.current().start()