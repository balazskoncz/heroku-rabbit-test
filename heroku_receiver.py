
import pika 
import os
import urllib
from flask import Flask
from threading import Thread

print('Starting receiver & server')
app = Flask(__name__, static_folder='static') 
# connection = pika.BlockingConnection(
#     pika.ConnectionParameters(host=hostname, credentials=credentials))

url_str = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost//')
url = urllib.parse.urlparse(url_str)

print('total url: {}'.format(url_str))
print('host: {}'.format(url.hostname))
print('virtual host: {}'.format(url.path[1:]))

params = pika.ConnectionParameters(host=url.hostname, virtual_host=url.path[1:],
    credentials=pika.PlainCredentials(url.username, url.password))

connection = pika.BlockingConnection(params) # Connect to CloudAMQP

channel = connection.channel()

channel.queue_declare(queue='hello_r')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)


channel.basic_consume(
    queue='hello_r', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages On NEw Thread ...')
thread = Thread(channel.start_consuming())
#channel.start_consuming()

port = os.getenv('PORT', default=5000)
print('Starting server on port: {}'.format(port))

app.run(debug=False, port=port, host='0.0.0.0')