import pika
import os
import urllib

# Parse CLODUAMQP_URL (fallback to localhost)
url_str = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost//')
url = urllib.parse.urlparse(url_str)
print(url)
params = pika.ConnectionParameters(host=url.hostname, virtual_host=url.path[1:],
    credentials=pika.PlainCredentials(url.username, url.password))

connection = pika.BlockingConnection(params) # Connect to CloudAMQP
channel = connection.channel() # start a channel
channel.queue_declare(queue='hello') # Declare a queue
# send a message
channel.basic_publish(exchange='', routing_key='hello', body='Hello CloudAMQP!')
print(" [x] Sent Hello World!")

# create a function which is called on incoming messages
def callback(ch, method, properties, body):
  print(" [x] Received: {}".format(body))

# set up subscription on the queue
channel.basic_consume(queue='hello', on_message_callback=callback)

channel.start_consuming() # start consuming (blocks)

connection.close()
