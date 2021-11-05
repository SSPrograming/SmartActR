from logging import exception
from flask import request, jsonify, Blueprint, g
import mjwt
from config import query_yaml
from application.services import UserService
from .login_decorator import login_required
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
        return jsonify({"errCode": 1,
        "errMsg": "bad agruments"}), 200
    except:
        return jsonify({"errCode": 1,"errMsg": "unknown error"}), 200
    
    #获取用户信息
    wechatAppID = query_yaml('app.APPID')
    wechatAppSecret = query_yaml('app.APPSECRET')
    payload = {'appid': wechatAppID, 'secret': wechatAppSecret, 'js_code': code, 'grant_type':'authorization_code'}
    requestURL = query_yaml('app.WECHATURL')
    wechatResponse = requests.get(requestURL, params=payload)
    wechatResponseContent = wechatResponse.json()

    if 'errcode' in wechatResponseContent.keys(): 
        if wechatResponseContent['errcode'] == -1:
            return jsonify({"errCode": 1,"errMsg": "系统繁忙，请稍候再试"}), 200
        elif wechatResponseContent['errcode'] == 40029:
            return jsonify({"errCode": 1,"errMsg": "无效的登录码"}), 200
        elif wechatResponseContent['errcode'] == 45011:
            return jsonify({"errCode": 1,"errMsg": "操作频繁，请稍候再试"}), 200
        elif wechatResponseContent['errcode'] == 40226:
            return jsonify({"errCode": 1,"errMsg": "账户风险等级高，暂不能登录"}), 200
        else:
            return jsonify({"errCode": 1,"errMsg": "未知错误"}), 200
    else:
        openid = wechatResponseContent['openid']
        user, isExist = UserService.get_user(UserService,userID=openid)
        if not isExist:
            UserService.create_user(UserService, userID=openid, identity="tourist")
        else:
            print(user.identity)
        userjwt = mjwt.generate_jwt({"openID": openid})
        response["jwt"] = userjwt
        response["errCode"] = 0
        return jsonify(response), 200


@bp_user.route('/api/v1/user/getIdentity', methods=['POST'])
@login_required
def getIdentity():
    openid = g.userID
    user, isExist = UserService.get_user(UserService,userID=openid)
    if not isExist:
        return jsonify({"errCode": 1,"errMsg": "用户身份无效"}), 200
    else:
        return jsonify({"errCode": 0,"identity": user.identity}), 200


@bp_user.route('/api/v1/user/bind', methods=['POST'])
@login_required
def bind():
    try:
        ticket = request.json['ticket']
    except KeyError:
        return jsonify({"errCode": 1,"errMsg": "bad agruments"}), 200
    except:
        return jsonify({"errCode": 1,"errMsg": "unknown error"}), 200
    tsinghuaURL = query_yaml('app.TSINGHUAURL')
    payload = {"token": ticket}
    tResponse = requests.post(url=tsinghuaURL, data=payload)
    tContent = tResponse.json()
    if 'user' in tContent.keys():
        try:
            stuID = tContent['user']['card']
            stuName = tContent['user']['name']
            stuDepartment = tContent['user']['department']
            stuCell = tContent['user']['cell']
            stuMail = tContent['user']['mail']
            stuInfo = {
                'stuID': stuID,
                'stuName': stuName,
                'stuDepartment': stuDepartment,
                'stuCell': stuCell,
                'stuMail': stuMail
            }
            UserService.bind_user(g.userID, stuInfo)
        except Exception:
            return jsonify({"errCode": 1,"errMsg": "bad response from tsinghua server"}), 200
    else:
        return jsonify({"errCode": 1,"errMsg": "Invalid token"}), 200