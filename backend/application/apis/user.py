from flask import request, jsonify, Blueprint
import mjwt
from config import query_yaml
from application.services import UserService
import requests

bp_user = Blueprint(
    'user',
    __name__
)

@bp_user.route('/api/v1/user/login', methods=['POST'])
def login():
    response = {}
    try:
        code = request.json['code']
    except KeyError:
        return jsonify({"errmsg": "bad agruments"}), 200
    except:
        return jsonify({"errmsg": "unknown error"}), 200
    
    #获取用户信息
    wechatAppID = query_yaml('app.APPID')
    wechatAppSecret = query_yaml('app.APPSECRET')
    payload = {'appid': wechatAppID, 'secret': wechatAppSecret, 'js_code': code, 'grant_type':'authorization_code'}
    requestURL = query_yaml('app.WECHATURL')
    wechatResponse = requests.get(requestURL, params=payload)
    wechatResponseContent = wechatResponse.json()

    if 'errcode' in wechatResponseContent.keys(): 
        if wechatResponseContent['errcode'] == -1:
            return jsonify({"errmsg": "系统繁忙，请稍候再试"}), 200
        elif wechatResponseContent['errcode'] == 40029:
            return jsonify({"errmsg": "无效的登录码"}), 200
        elif wechatResponseContent['errcode'] == 45011:
            return jsonify({"errmsg": "操作频繁，请稍候再试"}), 200
        elif wechatResponseContent['errcode'] == 40226:
            return jsonify({"errmsg": "账户风险等级高，暂不能登录"}), 200
        else:
            return jsonify({"errmsg": "未知错误"}), 200
    else:
        openid = wechatResponseContent['openid']
        user, isExist = UserService.get_user(UserService,userID=openid)
        if not isExist:
            UserService.create_user(UserService, userID=openid, identity="tourist")
        else:
            print(user.identity)
        userjwt = mjwt.generate_jwt({"openID": openid})
        response["jwt"] = userjwt
        return jsonify(response), 200

