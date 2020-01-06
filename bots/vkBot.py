import json, requests
from BotTemplate import BotTemplate

class Bot(BotTemplate):
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

    def getActions(self):
        actions=[]
        try:
            vk_response=requests.get("https://"+self.lpServer+"?act=a_check&key="+self.key+"&ts="+(str)(self.ts)+"&wait=25&mode=0&version=3")
        except: return 3
        if not vk_response.status_code==200: return 4
        if "failed" in vk_response.json():
            self.updateLpServerInfo()
            vk_response=requests.get("https://"+self.lpServer+"?act=a_check&key="+self.key+"&ts="+(str)(self.ts)+"&wait=25&mode=0&version=3")
        if not "ts" in vk_response.json():
            return 5
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

