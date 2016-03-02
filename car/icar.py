from abc import ABCMeta, abstractmethod
from enum import IntEnum

class ICar(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self):
        pass


    @abstractmethod
    def Connect(self):
        # Return: bool indicating if the connection was succesfull
        pass

    @abstractmethod
    def EnableFetch(self,dataTypeList):
        # Return: void
        pass

    @abstractmethod
    def GetSupportedDataTypes(self):
        # Return: List of supported data types
        # If error, returns None
        pass

    @abstractmethod
    def FetchData(self,dataTypeList=None):
        # Return: Map with data defined by 
        # enable fetch or given data type list
        # If error, returns None
        pass

    @abstractmethod
    def DumpAllData(self):
        # Return: Map of all available data from the car
        # If error, returns None
        pass

    @abstractmethod
    def DumpFreezeData(self):
        # Return: Map of all available freeze data (data logged on error)
        # If error, returns None
        pass

    @abstractmethod
    def CheckForCarErrors(self):
        # Return: Map with error codes as keys and 
        # description as value
        # If error, returns None
        pass

    @abstractmethod
    def GetErrorMessage(self):
        # Return: string with latest error message
        pass

    class DataTypes(IntEnum):
        FuelStatus          = 0x03
        FuelLevel           = 0x2F
        EngineLoad          = 0x04
        RPM                 = 0x0C
        Speed               = 0x0D
        IntakeAirTemp       = 0x0F
        ThrottlePosition    = 0x11
        RunTime             = 0x1F
        OutsideAirTemp      = 0x46
        OilTemp             = 0x5C
        FuelRate            = 0x5E
