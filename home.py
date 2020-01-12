import time, os
from multiprocessing import Process

class Room:
    isLightOn=False
    isHeaterOn=False
    temp=0.0
    maintainingTemp=0.0
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
        print("click("+str(pin)+")!")
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
        os.system("echo \"Current temp. is "+str(self.temp)+"\">> trmp.log")
        pass
    def __maintainTemperature(self,temperature):
        while self.__maintainingTemperature:
            os.system("echo \"FUCK+; Current temp. is "+str(self.temp)+"\">> trmp.log")
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
    def switchMaintaingTemperature(self):
        print("Doesn't work_)")
        return False
        if not self.__maintainingTemperature:
            self.proc=Process(target=self.__maintainTemperature, args=(self.maintainingTemp,))
            self.proc.start()
        else:
            self.proc.join()
        self.__maintainingTemperature = not self.__maintainingTemperature
class Homt:
    def __init__(self):
      livingroom=Room()
      bedroom0=Room()
      bedroom1=Room()
      bathroom=bathRoom()


if __name__=="__main__":
    rum=Room(0,1,2)

