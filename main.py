# -*- codinfg: utf-8 -*- #
import time, subprocess, os, json, glob
from importlib.machinery import SourceFileLoader
import home

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

#def getRooms():
#    modules=glob.glob("rooms/*.py")
#    if modules == []:
#        print("No rooms available")
#        exit()
#    if not glob.glob("rooms/RoomTemplate*") == []:
#        modules.remove(glob.glob("rooms/RoomTemplate*")[0])
#    if modules == []:
#        print("No rooms available")
#        exit()
#    imports=[]
#    for mod in modules:
#        imports.append(SourceFileLoader(mod.split('/')[1],mod).load_module())
#    for i in range(len(modules)):
#        modules[i]=modules[i].split(".py")[0]
#        modules[i]+=".json"
#    rooms=[]
#    for i in range(len(imports)):
#        tmproom=imports[i].Room(modules[i])
#        if(tmproom.isValid):
#            rooms.append(tmproom)
#        else:
#            print("No", end=' ')
#            print(modules[i],end=" config file found\n")
#    return rooms

def action_parser(action):
    global home
    try:
        action[0]
    except:
        return [2]
    if action[0]=='!':
        return [0, str(os.popen(action[1:]).read())]
    else:
        action=action.lower()
        if "комнате" in action:
            roomNumber=int(action.split("комнате ")[1])
            if roomNumber>len(home.rooms):
                return [0, "Неправильный номер комнаты. Всего доступно "+len(home.rooms)+", первая имеет индекс \'0\' "]
        else:
            return [0, "Не задан номер комнаты. Всего доступно "+str(len(home.rooms))+", первая имеет индекс \'0\' "]
        if "скажи" in action or "какая" in action:
#             if "температуру" in action or "температура" in action:
#                 return [home.rooms[roomNumber].temp]
             if "свет" in action:
                 return [0, home.rooms[roomNumber].isLightOn]
             else:
                return [0, "Неподдерживаемая команда"]
        elif "ли" in action:
            if "свет" in action:
                if home.rooms[roomNumber].isLightOn:
                    return [0, "Да"]
                else:
                    return [0, "Нет"]
            else:
                return [0, "Неподдерживаемая команда"]
        elif "свет" in action:
            if "вкл" in action:
                return [0, home.rooms[roomNumber].lightOn()]
            elif "выкл" in action:
                return [0, home.rooms[roomNumber].lightOff()]
            else:
                return [0, "Неподдерживаемая команда"]
        elif  "сделай" in action and "фото" in action:
            try:
                camResponse=home.rooms[roomNumber].makePhoto()
            except:
                return [0, "Не могу сделать фото. Проверьте, имеет ли данная комната камеру"]
            if not "ERR:" in camResponse:
                return [1 ,camResponse]
            else:
                return [0, camResponse]
        else:
            return [0, "Неподдерживаемая команда"]

if __name__=="__main__":
    bots=getBots()
#    rooms=getRooms()
    home=home.Home("homeConfig.json")
    print(bots)
    print(home.rooms)
    #exit()
    while True:
        for bot in bots:
            result=bot.getActions()
            if(not result == []):
                for action in result:
                    result=action_parser(action)
                    #print(result)
                    if len(result)>=2:
                        if result[0]==0:
                            #print(bot.sendImage(bot.user_id,result[1]))
                            bot.sendMessage(bot.user_id, result[1])
                        elif result[0]==1:
                            bot.sendImage(bot.user_id, result[1])
                            #result.remove[0]
                            #bot.sendImage(bot.user_id,'\n'.join(result))
                        elif result[0]==2:
                            print("!ERR!")
                    else:
                        bot.sendMessage(bot.user_id,"<ERROR>")
            else: print("Nothing happened")
            time.sleep(5)
