import time
import random
from multiprocessing import Process

class Room:
    isLightOn=False
    isHeaterOn=False
    temp=0.0
    __lightPin=0
    __heaterPin=0
    __termoPin=0
    __fallibility=0.0
    __maintainingTemperature=False
    def __init__(self,lightpin,heaterpin,fability):
        self.__lightPin=lightpin
        self.__heaterPin=heaterpin
        self.__fallibility=fability
        #os.system("echo "+ str(lightpin)+" > /sys/class/gpio/export")
        #os.system("echo "+ str(heaterpin)+" > /sys/class/gpio/export")
        pass
    def __click(self, pin, state):
#        if state:
#            os.system("echo \"in\" > /sys/class/gpio/gpio"+ (str)(pin) +"/direction")
#        else:
#            os.system("echo \"out\" > /sys/class/gpio/gpio"+ (str)(pin) +"/direction")
        print("click!")
    def switchLight(self):
        self.__click(self.isLightOn,self.__lightPin)
        self.isLightOn = not self.isLightOn
    def __switchHeater(self):
        self.__click(self.isHeaterOn,self.__heaterPin)
        self.isHeaterOn = not self.isHeaterOn
    def __updateTemperature(self):
        #работа с датчтком
        self.temp-=1
        if self.isHeaterOn:
            self.temp+=5
        print("Current temp. is", end=' ')
        print(self.temp)
        pass
    def __maintainTemperature(self,temperature):
        while self.__maintainingTemperature:
            if(self.temp<=temperature-self.__fallibility):
                if not self.isHeaterOn:
                    self.__switchHeater()
                time.sleep(1)
                self.__updateTemperature()
            elif(self.temp>=temperature+self.__fallibility):
                if self.isHeaterOn:
                    self.__switchHeater()
                time.sleep(1)
                self.__updateTemperature()
            else:
                self.__updateTemperature()
    def switchMaintaingTemperature(self, temperature):

class Home:
    def __init__(self):
      livingroom=Room()
      bedroom0=Room()
      bedroom1=Room()
      bathroom=bathRoom()


if __name__=="__main__":
    random.seed()
    rum=Room(0,1,2)
    rum.switchLight()
    rum.switchMaintaingTemperature(25.123)
    time.sleep(5.5)
    print("LOL")
    rum.switchMaintaingTemperature(0.0)
    print("101")
