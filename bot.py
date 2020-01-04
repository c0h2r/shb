# -*- coding: utf-8 -*-
import requests, time, subprocess, os, json
from abc import ABC, abstractmethod

requests.packages.urllib3.disable_warnings()#хз
proxy={"http":"socks5://127.0.0.1:9050","https":"socks5://127.0.0.1:9150","ftp":"socks5://127.0.0.1:9050"}

#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_tg_logic_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_
class BotTemplate(ABC):
    user_id=0
    last_message_id=0
    api_url=""
    access_token=""
    path_to_config=""
    #user_id, last_message_id, api_url, access_token, path_to_config
    #@abstractmethod
   # def init():
   #     pass
    def __init__(self, path_to_config):
        self.path_to_config=path_to_config
        with open(path_to_config,"r") as config:
            data=json.load(config)
        self.api_url=data["api_url"]
        self.user_id=data["user_id"]
        self.access_token=data["access_token"]
        self.last_message_id=data["last_message_id"]
        self.postInit()
    @abstractmethod
    def getEvents():
        pass
    @abstractmethod
    def sendMessage():
        pass
    @abstractmethod
    def postInit():
        pass
    @abstractmethod
    def checkData():
        pass
#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_tg_logic_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_

class tgBot(BotTemplate):
    timeout=5
    def postInit(self):
        pass

    def getEvents(self):
        global proxy
        actions=[]
        try:
            tg_response=requests.get(self.api_url+self.access_token+"/getUpdates?offset="+(str)(self.last_message_id)+"&timeout="+(str)(self.timeout),proxies=proxy)
        except:
            return None
        if not tg_response.status_code==200: return None
        if not tg_response.json()["ok"]: return None
        #print(tg_response.json())
        for element in tg_response.json()["result"]:
            if element["update_id"]>self.last_message_id:
                self.last_message_id=element["update_id"]
                with open(self.path_to_config,"w") as config:
                    json.dump({"api_url":self.api_url,"last_message_id":element["update_id"],"user_id":self.user_id,"access_token":self.access_token},config)
            else: continue
            if not "message" in element or not "text" in element["message"]:
                continue
            if element["message"]["chat"]["id"]==self.user_id:
                actions.append(element["message"]["text"])
        return actions
    def sendMessage(self, tg_chat_id, text):
        try:
            tg_response=requests.get(self.api_url+self.access_token+"/sendMessage?chat_id="+(str)(tg_chat_id)+"&text="+text,proxies=proxy)
        except:
            return "Error"
        if not tg_response.status_code==200: return "Server error"
        if not tg_response.json()["ok"]: return "Server didn\'t return ok. Not valid response?"
        return "Msg sent successfully"
    def checkData(self):
        print(self.api_url)
        print(self.user_id)
        print(self.access_token)
        print(self.last_message_id)
        print()

#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_tg_logic_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_
#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_vk_logic_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_
class vkBot(BotTemplate):
    lpServer=""
    key=""
    ts=0
    def postInit(self):
        self.updateLpServerInfo()

    def updateLpServerInfo(self):
        global vk_lpServer,vk_key,vk_ts
        try:
            vk_response=requests.get(self.api_url+"messages.getLongPollServer?access_token="+self.access_token+"&v=5.00")
        except:
            return False
        self.lpServer=vk_response.json()["response"]["server"]
        self.key=vk_response.json()["response"]["key"]
        self.ts=vk_response.json()["response"]["ts"]
        return True

    def getEvents(self):
        actions=[]
        try:
            vk_response=requests.get("https://"+self.lpServer+"?act=a_check&key="+self.key+"&ts="+(str)(self.ts)+"&wait=25&mode=0&version=3")
        except: return None
        if not vk_response.status_code==200: return None
        if "failed" in vk_response.json():
            self.updateLpServerInfo()
            vk_response=requests.get("https://"+self.lpServer+"?act=a_check&key="+self.key+"&ts="+(str)(self.ts)+"&wait=25&mode=0&version=3")
        if not "ts" in vk_response.json():
            return None
        self.ts=vk_response.json()["ts"]
        for event in vk_response.json()["updates"]:
            if event[0]==4 and event[3]==self.user_id:
                if event[1]==self.last_message_id:
                    continue
                actions.append(event[5])
                #action_parser("vk",event[5])
        return actions

    def sendMessage(self,vk_user_id,text):
        #messages.send?chat_id=202060108&message=Test message&v=5.00
        try:
            vk_response=requests.get(self.api_url+"messages.send?user_id="+(str)(vk_user_id)+"&message="+text+"&access_token="+self.access_token+"&v=5.00")
        except:
            return False
        if not vk_response.status_code==200: return False
        if "error" in vk_response.json():
            return vk_response.json()["error"]
        self.last_message_id=vk_response.json()["response"]
        return True

    def checkData(self):
        print(self.api_url)
        print(self.user_id)
        print(self.access_token)
        print(self.last_message_id)
        print()

#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_vk_logic_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_

def action_parser(source,action):
    global tg_user_id, vk_user_id
    if action=="alive?":
        if source == "tg": print(tg_send_msg(tg_user_id,"Yep"))
        elif source == "vk": print(vk_send_msg(vk_user_id,"Yep"))
    #elif action == "1": os.system("echo \"out\" > /sys/class/gpio/gpio4/direction")
    #elif action == "0": os.system("echo \"in\" > /sys/class/gpio/gpio4/direction")
    elif action[0]=="!":
        if source == "tg": tg_send_msg(tg_user_id,(str)(os.popen(action[1:]).read()))
        elif source == "vk": vk_send_msg(vk_user_id,(str)(os.popen(action[1:]).read()))
    else:
         if source == "tg": print(tg_send_msg(tg_user_id,"unknown cmd"))
         elif source == "vk": print(vk_send_msg(vk_user_id,"unknown cmd"))

#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_

if __name__=="__main__":
    #os.system("echo 4 > /sys/class/gpio/export")
    bots=[]
    bots.append(tgBot("config_tg.json"))
    bots.append(vkBot("config_vk.json"))
    for bot in bots:
        bot.checkData()
        print(bot.sendMessage(bot.user_id,"hello_from_bot"))
    while True:
        for bot in bots:
            result=bot.getEvents()
            if(not result == []): print(result)
            time.sleep(5)
