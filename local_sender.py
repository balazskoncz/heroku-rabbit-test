import pika

hostname = 'fish.rmq.cloudamqp.com'
user = 'lftilnno'
passpword = '8wBK2bkZI-etTBvCgYZgiXBq8qwwbQ-T' 

credentials = pika.credentials.PlainCredentials(user, passpword)

print(hostname)
print(credentials)

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=hostname, virtual_host='lftilnno', credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='hello_r')

channel.basic_publish(exchange='',
                      routing_key='hello_r',
                      body='123')
print(" [x] Message sent!'")