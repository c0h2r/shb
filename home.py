import time, os, json, cv2, datetime
from multiprocessing import Process

class Room:
    hasLight=False
    hasCamera=False
    lightPin=0
    cameraId=0
    isLightOn=False
    def __init__(self,configJson):
        if configJson["hasLight"]:
            self.lightPin=configJson["lightPin"]
            os.system("echo "+ str(self.lightPin)+" > /sys/class/gpio/export")
            self.hasLight=True
        if configJson["hasCamera"]:
            if "cameraId" in configJson:
                self.cameraId=configJson["cameraId"]
            self.__camera=cv2.VideoCapture(self.cameraId)
            self.hasCamera=True
    def lightOn(self):
        if(not self.hasLight):return "The room has no lightning."
        if(self.isLightOn):return "The light is already on."
        try:
            os.system("echo \"out\" > /sys/class/gpio/gpio"+ str(self.lightPin) +"/direction")
        except: return "Can\'t turn the light on."
        self.isLightOn=True
        return "Ok!"
    def lightOff(self):
        if(not self.hasLight):return "ERR: The room has no lightning."
        if(not self.isLightOn):return "The light is already off."
        try:
            os.system("echo \"in\" > /sys/class/gpio/gpio"+ str(self.lightPin) +"/direction")
        except: return "Can\'t turn the light off."
        self.isLightOn=False
        return "Ok!"
    def makePhoto(self):
        if(not self.hasCamera):return "ERR: The room has no camera"
        try:
            _ ,image=self.__camera.read()
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
                data=json.load(config)
            for room in data["rooms"]:
                self.rooms.append(Room(room))
        except:
            isValid=False



if __name__=="__main__":
    home=Home("config.json")
    print(len(home.rooms))
    for room in home.rooms:
        print(room.hasCamera)
        print(room.lightOn())
