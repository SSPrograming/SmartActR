import requests
from config import query_yaml
class WechatService():
    def getAccessToken():
        wechatAppID = query_yaml('app.APPID')
        wechatAppSecret = query_yaml('app.APPSECRET')
        payload = {'appid': wechatAppID, 'secret': wechatAppSecret,'grant_type':'client_credential'}
        requestURL = query_yaml('app.ACCESSTOKENURL')
        wechatResponse = requests.get(requestURL, params=payload)
        wechatResponseContent = wechatResponse.json()
        if 'errcode' in wechatResponseContent.keys(): 
            return "获取失败", False
        else:
            return wechatResponseContent["access_token"], True

    def sendMessage(content, token):
        requestURL = query_yaml('app.SENDMESSAGEURL')
        payload = {'access_token': token}
        wechatResponse = requests.post(requestURL, params=payload, json=content)
        wechatResponseContent = wechatResponse.json()
        print(wechatResponseContent)
    

