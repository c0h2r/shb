# -*- coding: utf-8 -*-
import requests
import time
import subprocess
import os
import json

requests.packages.urllib3.disable_warnings()#хз
#константы и глобалки
#tg:
timeout=5
tg_user_id=0
tg_api_url="https://api.telegram.org/bot"
tg_bot_token=""
tg_update_id=0#id последнего сообщения
#vk:
vk_user_id=0
vk_api_url="https://api.vk.com/method/"
vk_token=""
vk_lpServer=""
vk_key=""
vk_ts=""
vk_sent_msg_id=0

proxy={"http":"socks5://127.0.0.1:9050","https":"socks5://127.0.0.1:9050","ftp":"socks5://127.0.0.1:9050"}

#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_tg_logic_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_

def tg_init():
    global tg_user_id, tg_bot_token, tg_update_id
    with open("/home/pi/source/python/bot_0/config.json","r") as config:
        data=json.load(config)
    tg_user_id=data["user_id"]
    tg_bot_token=data["bot_token"]
    tg_update_id=data["update_id"]

def tg_check_updates():
    global tg_update_id
    try:
        #print(tg_bot_token)
        #print(tg_update_id)
        #,data={"offset":offset_tg+1, "limit":5,"timeout":0}
        tg_response=requests.get(tg_api_url+tg_bot_token+"/getUpdates?offset="+(str)(tg_update_id)+"&timeout="+(str)(timeout),proxies=proxy)
    except:
        return "Update error"
    if not tg_response.status_code==200: return "Server error"
    if not tg_response.json()["ok"]: return "Server didn\"t return ok. Not valid response?"
    for element in tg_response.json()["result"]:
        if element["update_id"]>tg_update_id:
            tg_update_id=element["update_id"]
            with open("/home/pi/source/python/bot_0/config.json","w") as config:
                json.dump({"update_id":element["update_id"],"user_id":tg_user_id,"bot_token":tg_bot_token},config)
        else: continue
        if not "message" in element or not "text" in element["message"]:
            return "Unsupported message error"
            continue
        #from_id=element["message"]["chat"]["id"]
        if element["message"]["chat"]["id"]==tg_user_id:
            action_parser("tg",element["message"]["text"])
        else: print(tg_send_msg(element["message"]["chat"]["id"],element["message"]["from"]["username"]+" is not in the sudoers file. The incident will be reported."))
        return (str)(tg_update_id)
    return "No updates"

def tg_send_msg(tg_chat_id,text):
    tg_response=requests.get(tg_api_url+tg_bot_token+"/sendMessage?chat_id="+(str)(tg_chat_id)+"&text="+text,proxies=proxy)
    if not tg_response.status_code==200: return "Server error"
    if not tg_response.json()["ok"]: return "Server didn\"t return. ok Not valid response?"
    return "Msg sent successfully"

#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_vk_logic_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_

def vk_updateLpServerInfo():
   global vk_lpServer,vk_key,vk_ts
   vk_response=requests.get(vk_api_url+"messages.getLongPollServer?access_token="+vk_token+"&v=5.00")
   vk_lpServer=vk_response.json()["response"]["server"]
   vk_key=vk_response.json()["response"]["key"]
   vk_ts=vk_response.json()["response"]["ts"]

def vk_getLpEvents():
    #https://{$server}?act=a_check&key={$key}&ts={$ts}&wait=25&mode=2&version=2
    global vk_ts, vk_sent_msg_id
    vk_response=requests.get("https://"+vk_lpServer+"?act=a_check&key="+vk_key+"&ts="+(str)(vk_ts)+"&wait=25&mode=0&version=3")
    if not vk_response.status_code==200: return "Server error"
    if "failed" in vk_response.json():
        vk_updateLpServerInfo()
        vk_response=requests.get("https://"+vk_lpServer+"?act=a_check&key="+vk_key+"&ts="+(str)(vk_ts)+"&wait=25&mode=0&version=3")
    if not "ts" in vk_response.json():
        return "Unknown error"
    vk_ts=vk_response.json()["ts"]
    for event in vk_response.json()["updates"]:
        if event[0]==4 and event[3]==vk_user_id:
            if event[1]==vk_sent_msg_id:
                continue
            print(event[5])
            action_parser("vk",event[5])
    return "Ok"

def vk_send_msg(vk_user_id, text):
    #messages.send?chat_id=202060108&message=Test message&v=5.00
    #https://api.vk.com/method/messages.send?user_id=202060108&message=Test message&access_token=...&v=5.00
    global  vk_api_url, vk_token, vk_sent_msg_id
    vk_response=requests.get(vk_api_url+"messages.send?user_id="+(str)(vk_user_id)+"&message="+text+"&access_token="+vk_token+"&v=5.00")
    if not vk_response.status_code==200: return "Server error"
    if "error" in vk_response.json():
        return vk_response.json()["error"]
    vk_sent_msg_id=vk_response.json()["response"]

def vk_init():
    global vk_user_id, vk_token
    #нормально их инициальзировать
    vk_user_id=202060108
    vk_token=""
    vk_updateLpServerInfo()

#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_#_

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
    #tg_init()
    vk_init()
    while True:
        #print(tg_check_updates())
        print(vk_getLpEvents())
        time.sleep(5)
