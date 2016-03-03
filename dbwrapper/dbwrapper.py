import requests


class DbWrapper:
    def __init__(self, ip, port, username, password):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password

    def send(self, data):
        url = 'http://' + self.ip + ':' + self.port + "/api/post_data"
        requests.post(url, json=data, auth=(self.username, self.password))

"""
test = DbWrapper('10.20.80.193', '8080', 'Admin', '1234')
test.send({'adsas': 1233})

i=0

while(i<20):
    i+=1
    test.send({'adsas': i})
"""

