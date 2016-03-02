from icar import ICar
from enum import Enum
import random, time

class CarSim(ICar):

    class SimVarDir(Enum):
        Up   = 0
        Down = 1
        Both = 2
            
    __enabled = []
    __errorMessage = ''
    __simParams = {
        # DataType                      (init value, variance, SimVarDir     , min, max )
        ICar.DataTypes.FuelLevel            :   (50        , 0.1     , SimVarDir.Down, 0  , 100 ),
        ICar.DataTypes.EngineLoad           :   (20        , 5       , SimVarDir.Both, 0  , 100 ),
        ICar.DataTypes.RPM                  :   (800       , 100     , SimVarDir.Both, 800, 6000),
        ICar.DataTypes.Speed                :   (0         , 10      , SimVarDir.Both, 0  , 120 ),
        ICar.DataTypes.IntakeAirTemp        :   (20        , 0.2     , SimVarDir.Both, 0  , 40  ),
        ICar.DataTypes.ThrottlePosition     :   (0         , 50      , SimVarDir.Both, 0  , 100 ),
        ICar.DataTypes.RunTime              :   (0         , 10      , SimVarDir.Both, 0  , 10000 ),
        ICar.DataTypes.OutsideAirTemp       :   (20        , 0.2     , SimVarDir.Both, 0  , 30  ),
        ICar.DataTypes.OilTemp              :   (20        , 0.2     , SimVarDir.Both, 0  , 120 ),
        ICar.DataTypes.FuelRate             :   (0         , 2       , SimVarDir.Both, 0  , 20  ),
    }

    __simValues = {}

    def __init__(self):
        print("Initialized Car!")
        random.seed()

    def Connect(self):
        print("Connected!")

    def EnableFetch(dataTypeList):
        self.__enabled = dataTypeList
        pass

    def GetSupportedDataTypes(self):
        return self.__simParams.keys()

    def FetchData(self, dataTypeList=None):
        dataToCheck=self.__enabled
        if dataTypeList is not None:
            dataToCheck = dataTypeList
        data = {}
        for dataType in dataToCheck:
            data[dataType] = self.__get(dataType)
        return data
        # Return: Map with data defined by 
        # enable fetch or given data type list

    def DumpAllData(self):
        # Return: Map of all available data from the car
        return self.FetchData()
        pass

    def DumpFreezeData(self):
        # Return: Map of all available freeze data (data logged on error)
        return self.FetchData()

    def CheckForCarErrors(self):
        return {}

    def GetErrorMessage(self):
        return __errorMessage

    def __get(self, dataType):
        if dataType not in self.__simParams:
            return None

        if dataType not in self.__simValues:
            self.__simValues[dataType] = self.__simParams[dataType][0]
            return self.__simValues[dataType]
        simValue = self.__simValues[dataType]
        simVarDir = self.__simParams[dataType][2]
        changeValue = random.uniform(0, self.__simParams[dataType][1])

        if simVarDir == self.SimVarDir.Down:
            simValue -= changeValue
        elif simVarDir == self.SimVarDir.Up:
            simValue += changeValue
        elif simVarDir == self.SimVarDir.Both:
            simValue += random.choice([changeValue, -changeValue])

        if simValue > self.__simParams[dataType][4]:
            simValue = self.__simParams[dataType][4]
        elif simValue < self.__simParams[dataType][3]:
            simValue = self.__simParams[dataType][3]

        self.__simValues[dataType] = simValue
        return simValue

    

if __name__ == '__main__':
    car = CarSim()
    car.Connect()
    supportedDataTypes = car.GetSupportedDataTypes()

    print('Supported data types is', supportedDataTypes)
    while True:
        time.sleep(1)
        data = car.FetchData(supportedDataTypes)
        for key, value in data.items():
            print(int(key), value)