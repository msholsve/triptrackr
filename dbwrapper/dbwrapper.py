import requests
import json


class DbWrapper:
    def __init__(self, ip, port, username, password, tripid):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.tripid = tripid

    def send(self, data):
        url = 'http://' + self.ip + ':' + self.port + "/api/post_data"
        return requests.post(url, data=data, auth=(self.username, self.password))

    def dataBuffer(self, data, response):
        buffer = open("tripdata" + self.tripid+".txt", 'a')
        jsondata = json.dumps(data)
        buffer.write(jsondata + response + "\n")
        buffer.close()

    def reSend(self):
        buffer = open("tripdata" + self.tripid +".txt", 'r')
        lines = buffer.readlines()
        buffer.close()
        buffer = open("tripdata" + self.tripid + ".txt", 'w')
        for line in lines:
            if line[-3:] is not "200":
                data = line[:-4]
                response = self.send(data)
                buffer.write(data + response + "\n")
        buffer.close()

"""
test = DbWrapper('10.20.111.213', '8001', 'Admin', '1234')
test.send({'adsas': 1233})

i=0

while(i<20):
    i += 1
    test.send({'test': i})
    test.reSend(test.dataBuffer({'adsas': 1233}, test.send({'adsas': 1233})))

test = DbWrapper('10.20.111.213', '8001', 'Admin', '1234', '1')
test.dataBuffer({'adsas': 1233}, "200")
test.dataBuffer({'adsas': 144433}, "404")
test.dataBuffer({'sads': 333}, "300")
test.reSend()
"""