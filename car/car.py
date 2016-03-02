from icar import ICar
import obd, time

class Car(ICar):

    __obd = None
    __enabled = []
    __errorMessage = ''

    def __init__(self, ):
        print("Initialized Car!")

    def Connect(self):
        self.__obd = obd.OBD()

    def EnableFetch(dataTypeList):
        if self.__obd == None:
            raise StandardError("OBD is not connected")
        __enabled = dataTypeList


    def GetSupportedDataTypes(self):
        supportedDataTypes = []
        if self.__obd == None:
            raise StandardError("OBD is not connected")
        
        for name, member in ICar.DataTypes.__members__.items():
            if obd.commands[1][int(member)].supported:
                supportedDataTypes.append(member)

        return supportedDataTypes

    def FetchData(self, dataTypeList=None):
        if self.__obd == None:
            raise StandardError("OBD is not connected")

        dataToCheck=self.__enabled
        if dataTypeList is not None:
            dataToCheck = dataTypeList
        data = {}
        for dataType in dataToCheck:
            response = self.__obd.query(obd.commands[1][int(dataType)])
            data[dataType] = response.value
        return data

    def DumpAllData(self):
        if self.__obd == None:
            raise StandardError("OBD is not connected")
        data = {}
        for command in self.__obd.supported_commands:
            response = self.__obd.query(command)
            data[command] = response.value
        return data

    def DumpFreezeData(self):
        if self.__obd == None:
            raise StandardError("OBD is not connected")
        data = {}
        for command in self.__obd.supported_commands:
            response = self.__obd.query(obd.commands[2][command.pid])
            data[obd.commands[2][command.pid]] = response.value
        return data

    def CheckForCarErrors(self):
        if self.__obd == None:
            raise StandardError("OBD is not connected")
        response = self.__obd.query(self.__obd.command.GET_DTC)
        return response.value

    def GetErrorMessage(self):
        return __errorMessage

if __name__ == '__main__':
    obd.debug.console = True
    car = Car()
    car.Connect()
    supportedDataTypes = car.GetSupportedDataTypes()

    print('Supported data types is', supportedDataTypes)
    while True:
        time.sleep(1)
        data = car.FetchData(supportedDataTypes)
        for key, value in data.items():
            print(int(key), value)