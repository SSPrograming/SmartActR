from flask import Flask
from flask import request
from flask import jsonify
import mjwt
import requests
app = Flask(__name__)

@app.route('/api/v2/login', methods=['POST'])
def login():
    response = {}
    code = request.json['code']
    #TODO:ID 以及 secret 需要在配置文件中配置
    wechatAppID = 'wx399e9ceebc89171e'
    wechatAppSecret = '84d80f309434708c2b936cd32d3a3065'
    payload = {'appid': wechatAppID, 'secret': wechatAppSecret, 'js_code': code, 'grant_type':'authorization_code'}
    requestURL = 'https://api.weixin.qq.com/sns/jscode2session'
    wechatResponse = requests.get(requestURL, params=payload)
    wechatResponseContent = wechatResponse.json()
    if 'errcode' in wechatResponseContent.keys(): 
        if wechatResponseContent['errcode'] == -1:
            return jsonify({"errmsg": "系统繁忙，请稍候再试"})
        elif wechatResponseContent['errcode'] == 40029:
            return jsonify({"errmsg": "无效的登录码"})
        elif wechatResponseContent['errcode'] == 45011:
            return jsonify({"errmsg": "操作频繁，请稍候再试"})
        elif wechatResponseContent['errcode'] == 40226:
            return jsonify({"errmsg": "账户风险等级高，暂不能登录"})
        else:
            return jsonify({"errmsg": "未知错误"})
    else:
        userjwt = mjwt.generate_jwt({"openID": wechatResponseContent['openid']})
        response["jwt"] = userjwt
        return jsonify(response), 200

