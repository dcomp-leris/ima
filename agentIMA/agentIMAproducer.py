import pika, sys


class agentIMAproducer():
    file = open(sys.argv[1], 'r')
    line = file.read().splitlines()

    def __init__(self):
        self.user = self.line[1]
        self.password = self.line[3]
        self.ip = self.line[5]
        self.port = self.line[7]
        self.vhost = self.line[9]
        self.sliceID = self.line[11]
        self.slicePartID = self.line[13]
        self.monitoring_agent = self.line[15]
        self.monitoring_ip = self.line[17]


    def connection(self, message):
        credentials = pika.PlainCredentials(self.user, self.password)

        connection = pika.BlockingConnection(pika.ConnectionParameters(self.ip, self.port, self.vhost, credentials))
        channel = connection.channel()

        channel.queue_declare(queue='distribution')

        channel.basic_publish(exchange='', routing_key='distribution', body=str(message))
        print(" [x] Sent Metrics Message to Queue'")
        connection.close()







