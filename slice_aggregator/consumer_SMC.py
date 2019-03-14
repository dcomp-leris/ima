import pika, sys
from slice_aggregator import slice_database


class consumer_smc():
    file = open(sys.argv[1], 'r')
    line = file.read().splitlines()

    def __init__(self):
        self.user = self.line[1]
        self.password = self.line[3]
        self.ip = self.line[5]
        self.port = self.line[7]
        self.vhost = self.line[9]
        self.slice_id = self.line[11]

    def rabbitconnection(self):
        credentials = pika.PlainCredentials(self.user, self.password)

        connection = pika.BlockingConnection(pika.ConnectionParameters(self.ip, self.port, self.vhost, credentials))
        channel = connection.channel()

        return channel

    def createQueue(self, channel, db):
        db.create_database(self.slice_id)

        def callback(ch, method, properties, body):
            print(" [x] Received data ")
            db.insert_data(self.slice_id, body)

        channel.queue_declare(queue='distribution')

        channel.basic_consume(callback, queue='distribution', no_ack=True)

        print(' [*]Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()


consumer = consumer_smc()
channel = consumer.rabbitconnection()
db = slice_database.database()

consumer.createQueue(channel, db)



