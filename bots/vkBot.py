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
        print(vk_response.json());
        self.lpServer=vk_response.json()["response"]["server"]
        self.key=vk_response.json()["response"]["key"]
        self.ts=vk_response.json()["response"]["ts"]
        return True

    def getActions(self):
        actions=[]
        try:
            vk_response=requests.get("https://"+self.lpServer+"?act=a_check&key="+self.key+"&ts="+(str)(self.ts)+"&wait=25&mode=0&version=3")
        except: return []
        if not vk_response.status_code==200: return []
        if "failed" in vk_response.json():
            self.updateLpServerInfo()
            try:
                vk_response=requests.get("https://"+self.lpServer+"?act=a_check&key="+self.key+"&ts="+(str)(self.ts)+"&wait=25&mode=0&version=3")
            except:
                return []
        if not "ts" in vk_response.json():
            return []
        self.ts=vk_response.json()["ts"]
        for event in vk_response.json()["updates"]:
            if event[0]==4 and event[3]==self.user_id:
                if event[1]==self.last_message_id or event[5]=="":
                    continue
                actions.append(event[5])
        return actions

    def sendMessage(self,vk_user_id,text):
        #messages.send?chat_id=202060108&message=Test message&v=5.00
        try:
            vk_response=requests.get(self.api_url+"messages.send?user_id="+(str)(vk_user_id)+"&message="+text+"&access_token="+self.access_token+"&v=5.00")
        except:
            return 1
        if not vk_response.status_code==200: return 2
        if "error" in vk_response.json():
            return 3#vk_response.json()["error"]
        self.last_message_id=vk_response.json()["response"]
        return 0

    def sendImage(self,vk_user_id,path_to_image):
        #https://vk.com/dev/upload_files?f=4.%20%D0%97%D0%B0%D0%B3%D1%80%D1%83%D0%B7%D0%BA%D0%B0%20%D1%84%D0%BE%D1%82%D0%BE%D0%B3%D1%80%D0%B0%D1%84%D0%B8%D0%B8%20%D0%B2%20%D0%BB%D0%B8%D1%87%D0%BD%D0%BE%D0%B5%20%D1%81%D0%BE%D0%BE%D0%B1%D1%89%D0%B5%D0%BD%D0%B8%D0%B5
        try:
            vk_response=requests.get(self.api_url+"photos.getMessagesUploadServer?peer_id"+(str)(vk_user_id)+"&access_token="+self.access_token+"&v=5.103")
        except:
            return 1
        if not vk_response.status_code==200: return 2
        try:
            image={'file': open(path_to_image, 'rb')}
        except:
            return 3
        try:
            upload_server_response=requests.post(vk_response.json()['response']['upload_url'],files=image)
        except:
            return 4
        try:
            vk_response=requests.get(self.api_url+"photos.saveMessagesPhoto?photo="+upload_server_response.json()['photo']+"&server="+str(upload_server_response.json()['server'])+"&hash="+str(upload_server_response.json()['hash'])+"&access_token="+self.access_token+"&v=5.103")
        except:
            return 5
        try:
            sending_response=requests.get(self.api_url+"messages.send?user_id="+str(vk_user_id)+"&attachment=photo"+str(vk_response.json()['response'][0]['owner_id'])+'_'+str(vk_response.json()['response'][0]['id'])+"&access_token="+self.access_token+"&v=5.00")
            self.last_message_id=vk_response.json()["response"]
        except:
            return 6
        return 0
