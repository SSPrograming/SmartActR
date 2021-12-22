from flask import json, request, jsonify, Blueprint, g
from config import query_yaml
from application.database import db
from application.service import UserService, EquipmentService
from application.utils import generate_jwt, now
from .login_decorator import login_required

bp_user = Blueprint(
    'user',
    __name__
)

@bp_user.route('/manager-api/v1/user/queryUserInfo',methods=['POST'])
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

@bp_user.route('/manager-api/v1/user/updateUserStatus',methods=['POST'])
@login_required
def updateUserStatus():
    try:
        stuID = request.json["stuID"]
        status = request.json["status"]
    except:
        return jsonify({"errCode": 1, "errMsg": "bad arguments"}), 200
    msg, updateStatus = UserService.update_studentStatus(stuID, status)
    if not updateStatus:
        return jsonify({"errCode": 1, "errMsg": msg}), 200
    return jsonify({"errCode": 0}), 200


@bp_user.route('/manager-api/v1/user/getStudentRecordList', methods=['POST'])
@login_required
def getEquipmentRecordList():
    try:
        num = request.json["num"]
        stuID = request.json["stuID"]
    except:
        return jsonify({"errCode": 1, "errMsg": "bad arguments"}), 200
    startDate = request.json["startDate"] if "startDate" in request.json.keys() else None
    endDate = request.json["endDate"] if "endDate" in request.json.keys() else None
    recordList_raw, getStatus = UserService.get_user_recordList(stuID,startDate, endDate, num)

    if not getStatus:
        return jsonify({"errCode": 1, "errMsg": recordList_raw}), 200

    recordList = []
    for item in recordList_raw:
        recordList.append({"recordID": item.recordID,
                    "postTime": item.postTime.strftime("%Y-%m-%d %H:%M"),
                    "reserveDate": str(item.reserveDate),
                    "startTime": item.startTime.strftime("%H:%M"),
                    "endTime": item.endTime.strftime("%H:%M"),
                    "userName": UserService.get_name_by_id(item.userID),
                    "status": item.status,
                    "equipmentName": EquipmentService.get_name_by_type(item.equipmentType)[0]+str(item.equipmentID)+"号"
    })
    return jsonify({"errCode": 0, "recordList": recordList}), 200