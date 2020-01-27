import time, os
from multiprocessing import Process

#class Room:
#    isLightOn=False
#    isHeaterOn=False
#    temp=0.0
#    maintainingTemp=0.0
#    __lightPin=0
#    __heaterPin=0
#    __termoPin=0
#    __fallibility=0.0
#    __maintainingTemperature=False
#    def __init__(self,lightpin,heaterpin,fability):
#        self.__lightPin=lightpin
#        self.__heaterPin=heaterpin
#        self.__fallibility=fability
#        #os.system("echo "+ str(lightpin)+" > /sys/class/gpio/export")
#        #os.system("echo "+ str(heaterpin)+" > /sys/class/gpio/export")
#        pass
#    def __click(self, pin, state):
##        if state:
##            os.system("echo \"in\" > /sys/class/gpio/gpio"+ (str)(pin) +"/direction")
##        else:
##            os.system("echo \"out\" > /sys/class/gpio/gpio"+ (str)(pin) +"/direction")
#        print("click("+str(pin)+")!")
#    def switchLight(self):
#        self.__click(self.isLightOn,self.__lightPin)
#        self.isLightOn = not self.isLightOn
#    def __switchHeater(self):
#        self.__click(self.isHeaterOn,self.__heaterPin)
#        self.isHeaterOn = not self.isHeaterOn
#    def __updateTemperature(self):
#        #работа с датчтком
#        self.temp-=1
#        if self.isHeaterOn:
#            self.temp+=5
#        os.system("echo \"Current temp. is "+str(self.temp)+"\">> trmp.log")
#        pass
#    def __maintainTemperature(self,temperature):
#        while self.__maintainingTemperature:
#            os.system("echo \"FUCK+; Current temp. is "+str(self.temp)+"\">> trmp.log")
#            if(self.temp<=temperature-self.__fallibility):
#                if not self.isHeaterOn:
#                    self.__switchHeater()
#                time.sleep(1)
#                self.__updateTemperature()
#            elif(self.temp>=temperature+self.__fallibility):
#                if self.isHeaterOn:
#                    self.__switchHeater()
#                time.sleep(1)
#                self.__updateTemperature()
#            else:
#                self.__updateTemperature()
#    def switchMaintaingTemperature(self):
#        print("Doesn't work_)")
#        return False
#        if not self.__maintainingTemperature:
#            self.proc=Process(target=self.__maintainTemperature, args=(self.maintainingTemp,))
#            self.proc.start()
#        else:
#            self.proc.join()
#        self.__maintainingTemperature = not self.__maintainingTemperature

class Room:
    hasLight=False
    hasCamera=False
    lightPin=0
    cameraPin=0
    isLightOn=False
    def __init__(self,configJson):
        if configJson["hasLight"]:
            self.lightPin=configJson["lightPin"]
            os.system("echo "+ str(self.lightPin)+" > /sys/class/gpio/export")
            self.hasLight=True
        if configJson["hasCamera"]:
            self.__camera=cv2.VideoCapture(0)
            self.hasCamera=True
    def lightOn(self):
        if(not hasLight):return "The room has no lightning."
        if(isLightOn):return "The light is already on."
        try:
            os.system("echo \"in\" > /sys/class/gpio/gpio"+ str(lightPin) +"/direction")
        except: return "Can\'t turn the light on."
        islightOn=True
        return "Ok!"
    def lightOff(self):
        if(not hasLight):return "ERR: The room has no lightning."
        if(not isLightOn):return "The light is already off."
        try:
            os.system("echo \"out\" > /sys/class/gpio/gpio"+ str(lightPin) +"/direction")
        except: return "Can\'t turn the light off."
        islightOn=False
        return "Ok!"
    def makePhoto(self):
        if(not hasCamera):return "ERR: The room has no camera"
        try:
            useless,image=self.__camera.read()
            name=str(datetime.datetime.now())
            name=name[0:10]+'_'+name[11:19]+".png" #генерация имени фотографии
            cv2.imwrite(name,image)
        except:
            return "ERR: Can't make a photo."
        return name

class Home:
    isValid=True
    rooms=[]
    def __init__(self, path_to_config):
        self.__path_to_config=path_to_config
        try:
            with open(path_to_config,"r") as config:
                self.__data=json.load(config)
            self.roomsCount=len(self.__data["rooms"])
        except:
            isValid=False
        for room in self.__data["rooms"]:
            rooms.append(Room(room))



if __name__=="__main__":
    pass
