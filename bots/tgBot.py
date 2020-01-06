import json, requests
from BotTemplate import BotTemplate

class Bot(BotTemplate):
    proxy={"http":"socks5://127.0.0.1:9050","https":"socks5://127.0.0.1:9150","ftp":"socks5://127.0.0.1:9050"}
    timeout=5
    def postInit(self):
        pass

    def getActions(self):
        actions=[]
        try:
            tg_response=requests.get(self.api_url+self.access_token+"/getUpdates?offset="+(str)(self.last_message_id)+"&timeout="+(str)(self.timeout),proxies=self.proxy)
        except:
            return None
        if not tg_response.status_code==200: return 1
        if not tg_response.json()["ok"]: return 2
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

