from logging import exception
from flask import request, jsonify, Blueprint, g
import mjwt
from config import query_yaml
from application.services import UserService, EquipmentService
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
        print(userjwt)
        response["errCode"] = 0
        return jsonify(response), 200


@bp_user.route('/api/v1/user/getIdentity', methods=['GET'])
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
        ticket = request.json['token']
    except KeyError:
        return jsonify({"errCode": 1,"errMsg": "bad agruments"}), 200
    except:
        return jsonify({"errCode": 1,"errMsg": "unknown error"}), 200
    tsinghuaURL = query_yaml('app.TSINGHUAURL')
    payload = {"token": ticket}
    tResponse = requests.post(url=tsinghuaURL, json=payload)
    tContent = tResponse.json()
    print(tContent)
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
            msg, bindstatus = UserService.bind_user(UserService, g.userID, stuInfo)
            if bindstatus:
                return jsonify({"errCode": 0, "isBind": True}), 200
            else:
                return jsonify({"errCode": 1, "errMsg": "绑定失败", "isBind": False}), 200
        except Exception as e:
            print(e)
            return jsonify({"errCode": 1,"errMsg": "bad response from tsinghua server"}), 200
    else:
        return jsonify({"errCode": 1,"errMsg": "Invalid token"}), 200


@bp_user.route('/api/v1/user/getBindStatus', methods=['GET'])
@login_required
def getBindStatus():
    msg, succ = UserService.get_user_status(UserService, g.userID)
    if succ:
        if msg == 'binded' or msg == 'freeze':
            return jsonify({"errCode": 0,"isBind": True}), 200
        else:
            return jsonify({"errCode": 0,"isBind": False}), 200
    else:
        return jsonify({"errCode": 1,"errMsg": msg}), 200


@bp_user.route('/api/v1/user/getStudentInfo', methods=['GET'])
@login_required
def getStudentInfo():
    msg, succ = UserService.get_stuInfo(UserService, g.userID)
    if succ:
        try:
            msg['errCode'] = 0
            stuID_tolist = list(msg['stuID'])
            stuID_tolist[2:8] = "*****"
            msg['stuID'] = ''.join(stuID_tolist)
            return jsonify(msg), 200
        except Exception as e:
            print(e)
            return jsonify({"errCode": 1,"errMsg": "server error"}), 200
    else:
        return jsonify({"errCode": 1,"errMsg": msg}), 200


@bp_user.route('/api/v1/user/unbind', methods=['POST'])
@login_required
def unBind():
    """
    解除绑定;删除stu表中相关行，更新user表中的status以及identity
    """
    # TODO:失败时回滚
    msg1, stauts1 = UserService.update_user_status(UserService, userID=g.userID, newStatus='not bind')
    msg2, status2 = UserService.update_user_identity(UserService, userID=g.userID, newIdentity='tourist')
    msg3, status3 = UserService.drop_single_student(UserService, g.userID)
    if stauts1 and status2 and status3:
        return jsonify({"errCode": 0,"unBinded": True}), 200
    else:
        print(msg1, msg2, msg3)
        return jsonify({"errCode": 1,"unBinded": False}), 200


@bp_user.route('/api/v1/user/test', methods=['GET'])
def test():
    """
    测试用接口
    """
    msg = True
    for i in range(2):
        msg = msg and EquipmentService.insert_single_equipment(1, i+1)
    for i in range(8):
        msg = msg and EquipmentService.insert_single_equipment(2, i+1)
    msg = msg and EquipmentService.insert_single_equipment(3,1)
    print(msg)
    return jsonify({"ok":msg}), 200