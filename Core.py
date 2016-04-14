from gpswrapper import gpspoller
from dbwrapper import dbwrapper
from config.config import Config
#from car import carsim as car
from car import car
from rfid import state
import datetime, time, json, argparse
import traceback, os

class Core:

    def __init__(self, configFile=None, debug=False):
        self.configFile = 'core.config' if configFile is None else configFile
        self.debug = debug
        self.tripId = None
        self.start_time = None
        self.config = Config(self.configFile)
        self.error = []
        self.errorPollingInterval = self.config.tryGetWithDefault('errorPollingInterval', 15)
        self.pollingInterval = self.config.tryGetWithDefault('pollingInterval', 2)

    def __enter__(self):
        self.gpsd = gpspoller.GpsPoller()
        self.obd = car.Car(self.config.tryGetWithDefault('obdConfigFile', 'obd.config'), self.debug)
        self.obdFetchEnabled = False
        if not self.obd.connected:
            self.__DBG('OBD not connected on startup.')

        if self.tripId is None:
            self.__startTrip()

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def __startTrip(self):
        self.start_time = str(datetime.datetime.now())
        self.tripId = '{0}:{1}'.format(self.config.reg,self.start_time)
        self.dbWrapper = dbwrapper.DbWrapper(self.config.api, self.config.user, self.config.password, self.tripId)
        self.dbWrapper.debug = self.debug
        self.identity = state.Identity()

        startTripMessage = {
            'type': 'trip',
            'id': self.tripId,
            'car_id': self.config.reg,
            'start_time': self.start_time
        }
        self.__DBG(json.dumps(startTripMessage, sort_keys=True))
        self.dbWrapper.sendPriorityMessage(startTripMessage)

    def run(self):
        start = time.time()
        while True:
            pollingStart = time.time()
            if not self.obdFetchEnabled and self.obd.connected:
                self.obd.enableFetch(self.obd.getSupportedDataTypes())
                self.obdFetchEnabled = True

            remain = start + self.errorPollingInterval - time.time()
            if remain <= 0.0:
                if self.obd.connected:
                    self.error = self.obd.checkForCarErrors()
                start = time.time()

            carDataList = {}
            if self.obd.connected:
                carDataList = self.obd.fetchData()

            position = self.gpsd.getPosition()
            dataPoint = {
                'type': 'data',
                'trip_id': self.tripId,
                'registration_time': str(datetime.datetime.now()),
                'latitude': position[0],
                'longitude': position[1],
                'errors': self.error,       
            }

            for dataType, value in carDataList.items():
                dataPoint[self.obd.pidToVariableName[str(dataType)]] = value[0]

            driver_id = self.identity.get_id()
            if driver_id:
                credentials = {
                    'type': 'user',
                    'user_id': driver_id,
                    'trip_id': self.tripId,
                }
                self.dbWrapper.send(credentials)
                self.__DBG('RFID Card: ' + driver_id)

            self.__DBG(json.dumps(dataPoint, sort_keys=True))
            self.dbWrapper.send(dataPoint)
            self.__DBG("Data sent!")

            if not self.obd.connected:
                self.obd.Reconnect()
            timeToSleep = pollingStart + self.pollingInterval - time.time()
            self.__DBG('Time to sleep', timeToSleep)
            if timeToSleep > 0.0:
                time.sleep(timeToSleep)

    def close(self):
        self.obd.close()
        self.gpsd.disconnect()

    def __DBG(self, *args):
        if self.debug:
            msg = " ".join([str(a) for a in args])
            print(msg)

def logException(ex, tb):
    with open('exceptions.log', 'a+') as f:
                f.write('=====================EXCEPTION======================\n')
                f.write(str(datetime.datetime.now())+'\n'+str(ex)+'\n\n')
                f.write(tb)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', help='Path to config file', type=str, metavar='<path>')
    parser.add_argument('-d', help='Enable debug output', action='store_true')
    args = parser.parse_args()
    core = None
    try:
        core = Core(args.c, args.d)
    except Exception as e:
        logException(e, traceback.format_exc())
        raise

    while True:
        try:
            with core:
                core.run()
        except Exception as e:
            if isinstance(e, KeyboardInterrupt):
                os._exit(0)
            logException(e, traceback.format_exc())
