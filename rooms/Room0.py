from RoomTemplate import RoomTemplate
import cv2, datetime

class Room(RoomTemplate):
    def postInit(self):
        self.__camera=cv2.VideoCapture(0)
    def MakePhoto(self):
        useless,image=self.__camera.read()
        name=str(datetime.datetime.now())
        name=name[0:10]+'_'+name[11:19]+".png"
        cv2.imwrite(name,image)
        return name

