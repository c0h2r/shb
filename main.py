# -*- coding: utf-8 -*- #
import time, subprocess, os, json, glob
from importlib.machinery import SourceFileLoader

def action_parser(action):
#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#
#                                                                                                 #
#    global tg_user_id, vk_user_id                                                                #
#    if action=="alive?":                                                                         #
#        if source == "tg": print(tg_send_msg(tg_user_id,"Yep"))                                  #
#        elif source == "vk": print(vk_send_msg(vk_user_id,"Yep"))                                #
#    #elif action == "1": os.system("echo \"out\" > /sys/class/gpio/gpio4/direction")             #
#    #elif action == "0": os.system("echo \"in\" > /sys/class/gpio/gpio4/direction")              #
#    elif action[0]=="!":                                                                         #
#        if source == "tg": tg_send_msg(tg_user_id,(str)(os.popen(action[1:]).read()))            #
#        elif source == "vk": vk_send_msg(vk_user_id,(str)(os.popen(action[1:]).read()))          #
#    else:                                                                                        #
#         if source == "tg": print(tg_send_msg(tg_user_id,"unknown cmd"))                         #
#         elif source == "vk": print(vk_send_msg(vk_user_id,"unknown cmd"))                       #
#                                                                                                 #
#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#

if __name__=="__main__":
    #os.system("echo 4 > /sys/class/gpio/export")
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
        imports.append(SourceFileLoader(mod.split('\\')[1],mod).load_module())
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
    print(bots)
    while True:
        for bot in bots:
            result=bot.getActions()
            if(not result == []): print(result)
            time.sleep(5)
