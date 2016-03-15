import obd, time, subprocess, re

try:
    from .icar import ICar
except SystemError:
    from icar import ICar

class Car(ICar):

    __obd = None
    __enabled = []
    __errorMessage = ''
    connected = False

    def __init__(self, debug = False):
        self.__debug = debug
        obd.debug.console = debug
        self.Reconnect()
        if self.connected:
            return
        scan = self.__scanBluetooth()
        if self.__debug:
            print(scan)
        if 'OBDII' in scan:
            res = subprocess.check_output(['sudo' ,'rfcomm', 'bind', 'hci0', scan['OBDII']])
            if self.__debug:
                print(res)
            self.Reconnect()
        else:
            self.__errorMessage = 'Unable to find OBDII bluetooth adapter.'


    def __scanBluetooth(self):
        scan = subprocess.check_output(['sudo' ,'hcitool', 'scan'])
        matches = re.findall(r'\\t((?:[A-Fa-f0-9]+:){5}[A-Fa-f0-9]+)\\t([A-å-+0-9]*)\\n', str(scan), re.MULTILINE)
        return dict([(match[1], match[0]) for match in matches])

    def Reconnect(self):
        try:
            if self.__obd is not None:
                self.__obd.close()
            self.__obd = obd.OBD()
            self.connected = self.__obd.is_connected()
        except e:
            self.__errorMessage = 'Exception when connecting to OBD: {0}'.format(e)
        return self.connected


    def enableFetch(self, dataTypeList):
        if not self.connected:
            raise Exception("OBD is not connected")
        self.__enabled = dataTypeList


    def getSupportedDataTypes(self):
        if not self.connected:
            raise Exception("OBD is not connected")
        
        supportedDataTypes = []
        for name, member in ICar.DataTypes.__members__.items():
            if obd.commands[1][int(member)].supported:
                supportedDataTypes.append(member)

        return supportedDataTypes

    def fetchData(self, dataTypeList=None):
        if not self.connected:
            raise Exception("OBD is not connected")

        dataToCheck=self.__enabled
        if dataTypeList is not None:
            dataToCheck = dataTypeList
        data = {}
        for dataType in dataToCheck:
            response = self.__obd.query(obd.commands[1][int(dataType)])
            if response.value is None:
                continue
            data[dataType] = (response.value, response.unit)
        return data

    def dumpAllData(self):
        if not self.connected:
            raise Exception("OBD is not connected")
        data = {}
        for command in self.__obd.supported_commands:
            response = self.__obd.query(command)
            data[command] = response.value
        return data

    def dumpFreezeData(self):
        if not self.connected:
            raise Exception("OBD is not connected")
        data = {}
        for command in self.__obd.supported_commands:
            pid = int(command.pid, 16)
            response = self.__obd.query(obd.commands[2][pid])
            data[obd.commands[2][pid]] = response.value
        return data

    def checkForCarErrors(self):
        if not self.connected:
            raise Exception("OBD is not connected")
        response = self.__obd.query(obd.commands.GET_DTC)
        return response.value

    def getErrorMessage(self):
        returnMessage = self.__errorMessage
        self.__errorMessage = ''
        return returnMessage

    def close(self):
        self.__obd.close()


if __name__ == '__main__':
    car = Car(True)
    supportedDataTypes = car.getSupportedDataTypes()

    print('Supported data types is', supportedDataTypes)
    print(car.checkForCarErrors())
    print(car.dumpAllData())
    print(car.dumpFreezeData())
    while True:
        time.sleep(1)
        data = car.fetchData(supportedDataTypes)

        for key, value in data.items():
            print(int(key), value)