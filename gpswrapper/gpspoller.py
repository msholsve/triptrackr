__author__ = 'Max'


# GPSPpller is a (thread) object that constantly updates a global variable
# (in this case gpsd) with the current GPS data. The core software can now access the current
# location through the global variable 'gpsd'. For example: gpsd.fix.latitude
import os, time, sys
import threading
sys.path.append(os.path.dirname(os.path.abspath(__file__)) +'/gps-python3')
from gps import *

dataStabilizationDelay = 2

class GpsPoller(threading.Thread):

    __mutex = threading.Lock()
    __gpsd = None  # seting the global variable

    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.__gpsd = GPS(mode=WATCH_ENABLE)  # starting the stream of info
        self.current_value = None
        self.running = True  # setting the thread running to true
        self.start()
        time.sleep(dataStabilizationDelay)

    def run(self):
        while self.running:
            time.sleep(1)
            with self.__mutex:
                self.__gpsd.next()  # this will continue to loop and grab EACH set of gpsd info to clear the buffer

    def getPosition(self):
        with self.__mutex:
            return self.__gpsd.fix.latitude, self.__gpsd.fix.longitude

    def getTime(self):
        with self.__mutex:
            return str(self.__gpsd.utc)

    def gotSatLink(self):
        with self.__mutex:
            return str(self.__gpsd.fix.mode) != "1"

    def disconnect(self):
        with self.__mutex:
            self.running = False
        self.join()  # wait for the thread to finish what it's doing


# Example on how to use a GpsPoller object:
#
# if __name__ == '__main__':
#     gpsp = GpsPoller()  # create a GpsPoller thread
#     try:
#         gpsp.start()  # start the thread
#         print("Thread starting, please wait...")
#         while True:
#             # it may take a second or two to get good data
#             time.sleep(2)
#
#             os.system('clear')
#
#             print(" GPS reading") # Note, the data bellow is only some of the avalialbe GPS data
#             print("----------------------------------------")
#             print("latitude       " + str(gpsd.fix.latitude)) # Example: (latitude     63.431156667)
#             print("longitude      " + str(gpsd.fix.longitude)) # Example: ('longitude  10.393918333)
#             print("time utc       " + str(gpsd.utc)) # Example: (time utc    2016-02-25T00:40:03.000Z)
#             print("altitude (m)   " + str(gpsd.fix.altitude)) # Example (altitude (m)   47.5)
#             print("speed (m/s)    " + str(gpsd.fix.speed)) # Example (speed (m/s)   0.134)
#             print("mode           " + str(gpsd.fix.mode)) # mode 1 = No satellite fix, mode 2 = 2D fix, mode 3 = 3D fix
#             print
#             print("Satellites (total of " + str(len(gpsd.satellites)) + " in view)") #Prints out satalites in view/used
#             for i in gpsd.satellites:
#                 print("\t" + str(i))
#
#             time.sleep(2)  # set to whatever
#
#     except (KeyboardInterrupt, SystemExit):  # when you press ctrl+c
#         print
#         "\nKilling Thread..."
#         gpsp.running = False
#         gpsp.join()  # wait for the thread to finish what it's doing
#     print
#     "Done.\nExiting."
