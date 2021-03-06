from abc import ABCMeta, abstractmethod
from enum import IntEnum

class ICar(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self):
        # Tries to connect to the OBD device. Check variable connected to check if there is a connection.
        pass

    @abstractmethod
    def Reconnect(self):
        # Closes OBD connection if there was one and reconnects
        pass

    @abstractmethod
    def close(self):
        # Closes the serial connection to the OBD device
        pass

    @abstractmethod
    def enableFetch(self,dataTypeList):
        # Return: void
        pass

    @abstractmethod
    def getSupportedDataTypes(self):
        # Return: List of supported data types
        # If error, returns None
        pass

    @abstractmethod
    def fetchData(self,dataTypeList=None):
        # Return: Map with data defined by 
        # enable fetch or given data type list
        # If error, returns None
        pass

    @abstractmethod
    def dumpAllData(self):
        # Return: Map of all available data from the car
        # If error, returns None
        pass

    @abstractmethod
    def dumpFreezeData(self):
        # Return: Map of all available freeze data (data logged on error)
        # If error, returns None
        pass

    @abstractmethod
    def checkForCarErrors(self):
        # Return: Map with error codes as keys and 
        # description as value
        # If error, returns None
        pass

    @abstractmethod
    def getErrorMessage(self):
        # Return: string with latest error message
        pass
