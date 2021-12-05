from flask import json, request, jsonify, Blueprint, g
from config import query_yaml
from application.database import db
from application.service import UserService
from application.utils import generate_jwt, now
from .login_decorator import login_required

bp_user = Blueprint(
    'user',
    __name__
)

@bp_user.route('/api/v1/user/queryUserInfo',methods=['POST'])
@login_required
def queryUserInfo():
    stuID = request.json["stuID"] if "stuID" in request.json.keys() else None
    limitNum = request.json["limitNum"] if "limitNum" in request.json.keys() else None
    stuName = request.json["stuName"] if "stuName" in request.json.keys() else None
    department = request.json["department"] if "department" in request.json.keys() else None
    if stuID is None and limitNum is None and stuName is None and department is None:
        return jsonify({"errCode": 1, "errMsg": "bad arguments"}), 200
    
    msg_or_stuList, queryStatus = UserService.query_user_info({
        "stuID": stuID,
        "limitNum": limitNum,
        "stuName": stuName,
        "department": department
    })
    if not queryStatus:
        return jsonify({"errCode": 1, "errMsg": msg_or_stuList}), 200
    else:
        return jsonify({"errCode": 0, "stuList": msg_or_stuList}), 200