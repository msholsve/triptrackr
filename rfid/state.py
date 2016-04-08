import threading
import os, time, sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) +'/pyusb_keyboard_alike')
from keyboard_alike import reader


class Identity(threading.Thread):
    __mutex = threading.Lock()

    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.current_value = None
        self.running = True  # setting the thread running to true
        self.connected = False
        self.reader = None

        self.id = None

        self.start()

    def run(self):
        while self.running:

            if not self.connected:
                try:
                    self.reader = reader.Reader(0xffff, 0x0035, 84, 16, should_reset=False)
                    self.reader.initialize()
                    self.connected = True
                except reader.DeviceException as e:
                    self.connected = False
            else:
                self.id = self.reader.read().strip()

        self.reader.disconnect()

    def get_id(self):
        ret = self.id
        self.id = None
        return ret


