
import pika 
import os
import urllib
print('Starting receiver')

# hostname = 'fish.rmq.cloudamqp.com'
# user = 'lftilnno'
# passpword = '8wBK2bkZI-etTBvCgYZgiXBq8qwwbQ-T' 

# credentials = pika.credentials.PlainCredentials(user, passpword)

# print(hostname)
# print(credentials)

# connection = pika.BlockingConnection(
#     pika.ConnectionParameters(host=hostname, credentials=credentials))

url_str = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost//')
url = urllib.parse.urlparse(url_str)

print('total url: {url}'.format(url))
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

print(' [*] Waiting for messages On heroku :)')
channel.start_consuming()