from pprint import pprint
from influxdb import InfluxDBClient
import json

class database():

    def insert_data(self, user, data):
        client = InfluxDBClient(host='localhost', port=8086)
        client.switch_database(str(user))


        print(client.get_list_database())

        data = str(data,'utf-8')
        data = data.replace('\'','\"')

        print(data)
        json_array = json.loads(str(data))
        print(json_array)

        client.write_points(json_array)

        query = 'select * from network_receive;'
        print("Querying data: " + query)
        result = client.query(query)
        print(result)

        print(client.get_list_measurements())

    def create_database(self, user):
        client = InfluxDBClient(host='localhost', port=8086)
        client.create_database(str(user))


