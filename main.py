# -*- codinfg: utf-8 -*- #
import time, subprocess, os, json, glob
from importlib.machinery import SourceFileLoader

def getBots():
    modules=glob.glob("bots/*.py")
    if modules == []:
        print("No bots available")
        exit()
    if not glob.glob("bots/BotTemplate*") == []:
        modules.remove(glob.glob("bots/BotTemplate*")[0])
    if modules == []:
        print("No bots available")
        exit()
    imports=[]
    for mod in modules:
        imports.append(SourceFileLoader(mod.split('/')[1],mod).load_module())
    for i in range(len(modules)):
        modules[i]=modules[i].split(".py")[0]
        modules[i]+=".json"
    bots=[]
    for i in range(len(imports)):
        tmpbot=imports[i].Bot(modules[i])
        if(tmpbot.isValid):
            bots.append(tmpbot)
        else:
            print("No", end=' ')
            print(modules[i],end=" config file found\n")
    return bots

def getRooms():
    modules=glob.glob("rooms/*.py")
    if modules == []:
        print("No rooms available")
        exit()
    if not glob.glob("rooms/RoomTemplate*") == []:
        modules.remove(glob.glob("rooms/RoomTemplate*")[0])
    if modules == []:
        print("No rooms available")
        exit()
    imports=[]
    for mod in modules:
        imports.append(SourceFileLoader(mod.split('/')[1],mod).load_module())
    for i in range(len(modules)):
        modules[i]=modules[i].split(".py")[0]
        modules[i]+=".json"
    rooms=[]
    for i in range(len(imports)):
        tmproom=imports[i].Room(modules[i])
        if(tmproom.isValid):
            rooms.append(tmproom)
        else:
            print("No", end=' ')
            print(modules[i],end=" config file found\n")
    return rooms

def action_parser(action):
    global rooms
    print(action)
    if action[0]==1:
        return [str(os.popen(action[1:]).read())]
    else:
        action=action.lower()
        if "комнате" in action:
            roomNumber=int(action.split("комнате ")[1])
            if roomNumber>len(rooms):
                return ["Неправильный номер комнаты. Всего доступно "+len(rooms)+", первая имеет индекс \'0\' "]
        else:
            return ["Не задан номер комнаты. Всего доступно "+str(len(rooms))+", первая имеет индекс \'0\' "]
        if "скажи" in action or "какая" in action:
             if "температуру" in action or "температура" in action:
                 return [rooms[roomNumber].temp]
             elif "свет" in action:
                 return [rooms[roomNumber].isLightOn]
             else:
                return ["Неподдерживаемая команда"]
        elif "ли" in action:
            if "свет" in action:
                if rooms[roomNumber].isLightOn:
                    return ["Да"]
                else:
                    return ["Нет"]
            else:
                return ["Неподдерживаемая команда"]
        elif "свет" in action:
            if "вкл" in action:
                rooms[roomNumber].lightOn()
                return ["Ok!"]
            elif "выкл" in action:
                rooms[roomNumber].lightOff()
                return ["Ok!"]
            else:
                return ["Неподдерживаемая команда"]
        elif  "сделай" in action and "фото" in action:
            try:
                path=rooms[roomNumber].MakePhoto()
            except:
                return ["Не могу сделать фото. Проверьте, имеет ли данная комната камеру"]
            return [1,path ]
        else:
            return ["Неподдерживаемая команда"]

if __name__=="__main__":
    bots=getBots()
    rooms=getRooms()
    print(bots)
    print(rooms)
    #exit()
    while True:
        for bot in bots:
            result=bot.getActions()
            if(not result == []):
                for action in result:
                    result=action_parser(action)
                    #print(result)
                    if len(result)>1:
                        if result[0]==1:
                            print(bot.sendImage(bot.user_id,result[1]))
                        elif result[0]==2:
                            result.remove[0]
                            bot.sendImage(bot.user_id,'\n'.join(result))
                    else:
                        bot.sendMessage(bot.user_id,result[0])
            else: print("Nothing happened")
            time.sleep(5)
