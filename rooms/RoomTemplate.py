import time, os
from multiprocessing import Process
from abc import ABC, abstractmethod

class RoomTemplate(ABC):
    isLightOn=False
    __temp=0.0
    __lightPin=0
    #__heaterPin=0
    __termoPin=0
    isValid=True
    def __init__(self,path_to_config):
       # self.__lightPin=lightpin
       # self.__heaterPin=heaterpin
       # self.__fallibility=fability
       # #os.system("echo "+ str(lightpin)+" > /sys/class/gpio/export")
       # #os.system("echo "+ str(heaterpin)+" > /sys/class/gpio/export")
        self.postInit()
    @abstractmethod
    def postInit(self):
        pass
    def __click(self, pin, state):
#        if state:
#            os.system("echo \"in\" > /sys/class/gpio/gpio"+ (str)(pin) +"/direction")
#        else:
#            os.system("echo \"out\" > /sys/class/gpio/gpio"+ (str)(pin) +"/direction")
        print("click("+str(pin)+")!")
    def switchLight(self):
        self.__click(self.isLightOn,self.__lightPin)
        self.isLightOn = not self.isLightOn
    def updateTemperature(self):
        #работа с датчтком
        return self.__temp
        pass
