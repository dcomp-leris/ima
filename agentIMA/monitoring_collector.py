import sys
import time
import requests
import json
from agentIMAproducer import agentIMAproducer
from datetime import timedelta, datetime


class monitoring_collector():
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

    def collectMetrics(self):
        if self.monitoring_agent == 'prometheus':
            URL = "http://%s:9090/api/v1/query?" % self.monitoring_ip
            print(URL)

            # Métrica 1: Virtual network receive
            query = 'sum(rate(container_network_receive_bytes_total{name=~"[0-z]*-%s"}[10s])) by (name)' % self.sliceID
            timestamp = datetime.now().timestamp()
            PARAMS = {'query': query, 'time': timestamp}
            print("Timestamp ", timestamp)
            request = requests.get(url=URL, params=PARAMS)
            metricV1 = json.loads(request.text)
            print("Métrica 1: %s\n" % metricV1)

            # Métrica 2: Virtual network transmit
            query = 'sum(rate(container_network_transmit_bytes_total{name=~"[0-z]*-%s"}[10s])) by (name)' % self.sliceID
            PARAMS = {'query': query, 'time': timestamp}

            request = requests.get(url=URL, params=PARAMS)
            metricV2 = json.loads(request.text)
            print("Métrica 2: %s\n" % metricV2)

            # Métrica 3: Virtual CPU
            query = 'sum(rate(container_cpu_usage_seconds_total{name=~"[0-z]*-%s"}[10s])) by (name) * 100' % self.sliceID
            # query = 'sum(container_memory_rss{name=~"%s.*"}) by (name)' % self.sliceID
            PARAMS = {'query': query, 'time': timestamp}

            request = requests.get(url=URL, params=PARAMS)
            metricV3 = json.loads(request.text)
            print("Métrica 3: %s\n" % metricV3)

            # Métrica 4: Virtual RAM
            query = 'sum(container_memory_usage_bytes{image!="",name=~"[0-z]*-%s"}) by (name)' % self.sliceID
            PARAMS = {'query': query, 'time': timestamp}

            request = requests.get(url=URL, params=PARAMS)
            metricV4 = json.loads(request.text)
            print("Métrica 4: %s\n" % metricV4)

            # Métrica 5: Virtual Disk Bytes Reads
            query = 'sum(rate(container_fs_reads_bytes_total{name=~"[0-z]*-%s"}[10s])) by (name)' % self.sliceID
            PARAMS = {'query': query, 'time': timestamp}

            request = requests.get(url=URL, params=PARAMS)
            metricV5 = json.loads(request.text)
            print("Métrica 5: %s\n" % metricV5)

            # Métrica 6: Virtual Disk Bytes Writes
            query = 'sum(rate(container_fs_writes_bytes_total{name=~"[0-z]*-%s"}[10s])) by (name)' % self.sliceID
            PARAMS = {'query': query, 'time': timestamp}

            request = requests.get(url=URL, params=PARAMS)
            metricV6 = json.loads(request.text)
            print("Métrica 6: %s\n" % metricV6)

            virtualMetrics = [metricV1, metricV2, metricV3, metricV4, metricV5, metricV6]

            return virtualMetrics

    def parser_metrics(self, virtualMetrics):
        nMetrics = len(virtualMetrics)
        nResources = len(virtualMetrics[0]['data']['result'])
        print(nMetrics)
        print(nResources)
        dict = {}

        string = list()
        h = 0
        for i in range(nMetrics):
            for j in range(nResources):
                resource_id = virtualMetrics[i]['data']['result'][j]['metric']['name']
                resource_type = str(virtualMetrics[i]['data']['result'][j]['metric']['name']).split("-")[0]
                value = virtualMetrics[i]['data']['result'][j]['value'][1]
                timestamp = virtualMetrics[i]['data']['result'][j]['value'][0]
                timestamp = datetime.fromtimestamp(timestamp).isoformat()

                if i == 0:
                    kpi_name = "network_receive"
                elif i == 1:
                    kpi_name = "network_transmited"
                elif i == 2:
                    kpi_name = "virtual_cpu"
                elif i == 3:
                    kpi_name = "virtual_ram"
                elif i == 4:
                    kpi_name = "disk_reads"
                elif i == 5:
                    kpi_name = "disk_writes"

                string.append({"measurement": kpi_name, "tags": {"resource_id": resource_id, "resouce_type": resource_type, "slice_id": self.sliceID, "slice_part_id": self.slicePartID}, "time": timestamp, "fields": {"value": value}})

        return string


while True:
    agent = monitoring_collector()
    virtualMetrics = agent.collectMetrics()
    message = agent.parser_metrics(virtualMetrics)

    producer = agentIMAproducer()
    producer.connection(message)
    time.sleep(10)





