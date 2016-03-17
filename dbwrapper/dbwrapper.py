import requests
import json
import threading

class DbWrapper:

    debug = False
    __bufferMutex = threading.Lock()
    __countMutex = threading.Lock()
    __inBuffer = 0

    def __init__(self, api, username, password, tripid):
        self.api = api
        self.url = 'http://' + self.api + '/api/post_data'
        self.username = username
        self.password = password
        self.tripid = tripid
        self.retries = 5

    def send(self, data):
        self.saveLocal(data)
        sendThread = threading.Thread(target=self.__send, daemon=True, args=[data])
        sendThread.start()

    def __send(self, data):
        tries = 0
        while tries < self.retries:
            try:
                req = requests.post(self.url, json=data, auth=(self.username, self.password))
                if req.status_code == 200:
                    self.reSend()
                    return
            except:
                pass
            tries += 1

        self.dataBuffer(data)

    def saveLocal(self, data):
        jsondata = json.dumps(data, sort_keys=True)
        with open("trip_" + self.tripid+".txt", 'a') as f:
            f.write(jsondata + '\n')

    def dataBuffer(self, data):
        with self.__bufferMutex:
            self.__inBuffer += 1
            jsondata = json.dumps(data, sort_keys=True)
            with open("buffer" + self.tripid+".txt", 'a') as f:
                f.write(jsondata + '\n')

    def reSend(self):
        lines = None
        with self.__bufferMutex:
            if self.__inBuffer == 0:
                return

            with open("buffer" + self.tripid +".txt", 'r+') as f:
                lines = f.readlines()
                f.truncate(0)

            self.__inBuffer = 0

        for line in lines:
            self.send(json.load(data))

    def __DBG(self, *args):
        if self.debug:
            msg = " ".join([str(a) for a in args])
            print(msg)

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