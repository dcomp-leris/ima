import requests
import json
import thread

while(True):
    #URL endpoint
    slices = 2
    IP = ["200.136.191.111", "200.136.191.94"]
    i = 0
    while i < len(IP):
        URL = "http://%s:9090/api/v1/query?" % IP[i]
        print("Starting Collecting Metrics from Slice %s" % i)

        #METRIC 1: RECEIVE BYTES VIRTUAL ENVIRONMENT
        query = "sum(rate(container_network_receive_bytes_total{name=~\"slice1.*\"}[10s])) by (name)"
        PARAMS = {'query': query}

        request = requests.get(url = URL, params = PARAMS)

        print(json.loads(request.text))
        json_loaded = json.loads(request.text)
        time = json_loaded['data']['result'][0]['value'][0]

        #METRIC 2: TRANSMIT BYTES VIRTUAL ENVIRONMENT
        query = "sum(rate(container_network_transmit_bytes_total{name=~\"slice1.*\"}[10s])) by (name)"
        PARAMS = {'query': query, 'time': time}

        request = requests.get(url = URL, params = PARAMS)

        print(json.loads(request.text))
        i = i + 1

