from icar import ICar
import obd, time

class Car(ICar):

    __obd = None
    __enabled = []
    __errorMessage = ''

    def __init__(self, ):
        self.__obd = obd.OBD()
        print("Initialized Car!")

    def enableFetch(self, dataTypeList):
        if self.__obd is None:
            raise Exception("OBD is not connected")
        self.__enabled = dataTypeList


    def getSupportedDataTypes(self):
        supportedDataTypes = []
        if self.__obd is None:
            raise Exception("OBD is not connected")
        
        for name, member in ICar.DataTypes.__members__.items():
            if obd.commands[1][int(member)].supported:
                supportedDataTypes.append(member)

        return supportedDataTypes

    def fetchData(self, dataTypeList=None):
        if self.__obd is None:
            raise Exception("OBD is not connected")

        dataToCheck=self.__enabled
        if dataTypeList is not None:
            dataToCheck = dataTypeList
        data = {}
        for dataType in dataToCheck:
            response = self.__obd.query(obd.commands[1][int(dataType)])
            data[dataType] = response.value
        return data

    def dumpAllData(self):
        if self.__obd is None:
            raise Exception("OBD is not connected")
        data = {}
        for command in self.__obd.supported_commands:
            response = self.__obd.query(command)
            data[command] = response.value
        return data

    def dumpFreezeData(self):
        if self.__obd is None:
            raise Exception("OBD is not connected")
        data = {}
        for command in self.__obd.supported_commands:
            response = self.__obd.query(obd.commands[2][command.pid])
            data[obd.commands[2][command.pid]] = response.value
        return data

    def checkForCarErrors(self):
        if self.__obd is None:
            raise Exception("OBD is not connected")
        response = self.__obd.query(self.__obd.command.GET_DTC)
        return response.value

    def getErrorMessage(self):
        return self.__errorMessage

    def close(self):
        self.__obd.close()

if __name__ == '__main__':
    obd.debug.console = True
    car = Car()
    supportedDataTypes = car.getSupportedDataTypes()

    print('Supported data types is', supportedDataTypes)
    while True:
        time.sleep(1)
        data = car.fetchData(supportedDataTypes)
        for key, value in data.items():
            print(int(key), value)