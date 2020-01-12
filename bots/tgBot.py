import json, requests, os
from BotTemplate import BotTemplate

class Bot(BotTemplate):
    proxy={"http":"socks5://127.0.0.1:9150","https":"socks5://127.0.0.1:9150","ftp":"socks5://127.0.0.1:9150"}
    timeout=5
    def postInit(self):
        pass

    def getActions(self):
        actions=[]
        try:
            tg_response=requests.get(self.api_url+self.access_token+"/getUpdates?offset="+(str)(self.last_message_id)+"&timeout="+(str)(self.timeout),proxies=self.proxy)
        except:
            return []
        if not tg_response.status_code==200: return []
        if not tg_response.json()["ok"]: return []
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
            tg_response=requests.get(self.api_url+self.access_token+"/sendMessage?chat_id="+(str)(tg_chat_id)+"&text="+text,proxies=self.proxy)
        except:
            return 1
        if not tg_response.status_code==200: return 2
        if not tg_response.json()["ok"]: return 3
        return 0
    def sendImage(self, tg_chat_id, path_to_image):
        if os.path.exists(path_to_image):
            data={'chat_id':tg_chat_id}
            image={'photo':open(path_to_image, 'rb')}
            try:
                tg_response=requests.post(self.api_url+self.access_token+"/sendPhoto", data=data, files=image, proxies=self.proxy)
            except:
               return 2
            return 0
        return 1
