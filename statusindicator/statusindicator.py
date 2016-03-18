# import RPi.GPIO as GPIO
import time
from enum import Enum
import threading


class Status(Enum):
    Powered = 0
    GPSFix = 1
    DBConn = 2
    OBDConn = 3


class Statusindicator(threading.Thread):
    def __init__(self, debug=False):
        threading.Thread.__init__(self)
        self.LED = True
        self.debug = debug
        self.statuses = {s: False for s in Status}
        self.outputPin = 21

    def run(self):
        while True:
            self.handleStatus()

    def handleStatus(self):
        if self.LED:
            GPIO.setmode(GPIO.BOARD)  # Set to use Raspberry Pi board pin numbers
            GPIO.setup(self.outputPin, GPIO.OUT)  # Set up GPIO output channel
            def blink(duration):
                self.__DBG("Blinked for", duration, "s")
                GPIO.output(self.outputPin, True)
                time.sleep(duration)
                GPIO.output(self.outputPin, False)

            # Binks in the pattern: 1 long, 1 short for each status that's true, 1 long

            blink(1)  # Control blink #1
            self.__DBG("Sleeping for", .5, "s")
            time.sleep(.5)
            for s in (Status.GPSFix, Status.DBConn, Status.OBDConn):
                if self.statuses[s]:
                    blink(.5)
                    self.__DBG("Sleeping for", .5, "s")
                    time.sleep(.5)
                else:
                    self.__DBG("Sleeping for", 1, "s")
                    time.sleep(1)
            blink(1)  # Control blink #2

            self.__DBG("Sleeping for", 1, "s")
            time.sleep(1)

    def setStatus(self, *statuses):
        for s in statuses:
            if isinstance(s[0], Status):
                self.statuses[s[0]] = s[1]

    def __DBG(self, *args):
        if self.debug:
            msg = " ".join([str(a) for a in args])
            print(msg)
