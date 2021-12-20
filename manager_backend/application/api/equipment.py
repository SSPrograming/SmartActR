from logging import exception
from flask import request, jsonify, Blueprint, g
from config import query_yaml
from application.models import Admin
from application.database import db
from application.service import ReserveService, UserService, EquipmentService
from application.utils import generate_jwt
from .login_decorator import login_required
import os

bp_equipment = Blueprint(
    'equipment',
    __name__
)

@bp_equipment.route('/api/v1/equipment/getAllEquipmentType', methods=['GET'])
@login_required
def getAllEquipmentType():
    type_all_raw = EquipmentService.get_all_equipmentType()
    type_list = [{
        "equipmentType": item.equipmentType,
        "equipmentName": item.equipmentName,
        "equipmentDescription": item.equipmentDescription,
        "equipmentCount": EquipmentService.get_type_count(item.equipmentType),
        "equipmentImage": item.equipmentImageURL,
        "equipmentOrder": item.equipmentOrder
    }   for item in type_all_raw
    ]
    return jsonify({"errCode": 0, "TypeList": type_list}), 200

@bp_equipment.route('/api/v1/equipment/testPicUpload', methods=['POST'])
@login_required
def testPicUpload():
    testFile = request.files.get('testFile')
    print(testFile.filename)
    testFile.save('./application/static/test/'+'test_'+testFile.filename)
    testFileURL = query_yaml("app.MANAGERSERVERURL")+"image/test/test_"+testFile.filename
    return jsonify({"errCode": 0,"testPicURL": testFileURL}), 200

@bp_equipment.route('/api/v1/equipment/addEquipmentType', methods=['POST'])
@login_required
def AddEquipmentType():
    try:
        equipmentImage = request.files.get('equipmentImage')
        equipmentName = request.form['equipmentName']
        equipmentCount = int(request.form['equipmentCount'])
        equipmentDescription = request.form['equipmentDescription']
    except:
        return jsonify({"errCode": 1, "errMsg": "bad arguments"}), 200
    imgName = equipmentImage.filename
    msg, addStatus = EquipmentService.add_equipmentType(EquipmentService, equipmentName,
                                                        equipmentCount, equipmentDescription,imgName)
    if not addStatus:
        return jsonify({"errCode": 1, "errMsg": msg})
    equipmentImage.save('./application/static/equipment/'+msg+'_'+imgName)
    return jsonify({"errCode":0}), 200

@bp_equipment.route('/api/v1/equipment/getAllEquipment', methods=['POST'])
@login_required
def getAllEquipment():
    try:
        target_type = request.json["equipmentType"]
    except:
        return jsonify({"errCode": 1, "errMsg": "bad arguments"})
    msg, getStatus = EquipmentService.get_equipmentList(target_type)
    if not getStatus:
        return jsonify({"errCode": 1, "errMsg": msg})
    equipmentName, getStatus = EquipmentService.get_name_by_type(target_type)
    equipmentList = []
    for item in msg:
        equipmentList.append({
            "equipmentID": item.equipmentID,
            "equipmentName": equipmentName,
            "equipmentStatus": item.equipmentStatus
        })
    return jsonify({"errCode": 0, "equipmentList":equipmentList}), 200



@bp_equipment.route('/api/v1/equipment/editEquipmentType', methods=['POST'])
@login_required
def editEquipmentType():
    try:
        target_type = int(request.form['equipmentType'])
    except:
        return jsonify({"errCode": 1, "errMsg": "bad arguments"})

    new_name = request.form["equipmentName"] if "equipmentName" in request.form.keys() else None

    new_description = request.form["equipmentDescription"] if "equipmentDescription" in request.form.keys() else None

    new_img_file = request.files["equipmentImage"] if "equipmentImage" in request.files.keys() else None

    old_img_url = EquipmentService.get_TypeImg_url(target_type)[0]

    new_img_file_name = new_img_file.filename if new_img_file is not None else None

    msg, updateStatus = EquipmentService.update_equipmentType(target_type, new_name, new_description, new_img_file_name)

    if not updateStatus:
        return jsonify({"errCode": 1, "errMsg": msg})
    if new_img_file:
        img_url_prefix = query_yaml("app.MANAGERSERVERURL") + "image/equipment/"
        old_img_name = old_img_url[len(img_url_prefix):]
        if os.path.exists("/code/application/static/equipment/"+old_img_name):
            os.remove("/code/application/static/equipment/"+old_img_name)
        new_img_file.save("./application/static/equipment/"+str(target_type)+"_"+new_img_file_name)
    return jsonify({"errCode": 0}), 200
    
@bp_equipment.route('/api/v1/equipment/deleteEquipmentType', methods=['POST'])
@login_required
def deleteEquipmentType():
    try:
        target_type = request.json["equipmentType"]
    except:
        return jsonify({"errCode":1,"errMsg":"bad arguments"})
    msg, dropStatus = EquipmentService.drop_related_record(target_type)
    if not dropStatus:
        return jsonify({"errCode":1, "errMsg": msg}), 200
    
    msg, dropStatus = EquipmentService.drop_related_qrCode(target_type)
    if not dropStatus:
        return jsonify({"errCode":1, "errMsg": msg}), 200

    msg, dropStatus = EquipmentService.drop_related_equipment(target_type)
    if not dropStatus:
        return jsonify({"errCode": 1, "errMsg": msg}), 200
    
    msg, dropStatus = EquipmentService.drop_type(target_type)
    if not dropStatus:
        return jsonify({"errCode": 1, "errMsg": msg}), 200
    return jsonify({"errCode": 0}), 200

@bp_equipment.route('/api/v1/equipment/editEquipment', methods=['POST'])
@login_required
def editEquipment():
    try:
        Type = request.json["equipmentType"]
        id = request.json["equipmentID"]
        target_status = request.json["equipmentStatus"]
    except:
        return jsonify({"errCode": 1, "errMsg": "bad arguments"}), 200
    msg, updateStatus = EquipmentService.update_equipment_status(Type, id, target_status)
    if not updateStatus:
        return jsonify({"errCode": 1, "errMsg": msg}), 200
    return jsonify({"errCode": 0}), 200

@bp_equipment.route('/api/v1/equipment/addEquipment', methods=['POST'])
@login_required
def addEquipment():
    try:
        Type = request.json["equipmentType"]
    except:
        return jsonify({"errCode": 1, "errMsg": "bad arguments"}), 200
    
    msg_or_id, getStatus = EquipmentService.get_largest_id(Type)
    if not getStatus:
        return jsonify({"errCode": 1, "errMsg": msg_or_id}), 200
    addStatus = EquipmentService.add_equipment(Type,msg_or_id+1)
    if not addStatus:
        return jsonify({"errCode": 1, "errMsg": "新增设备失败"}), 200
    else:
        return jsonify({"errCode": 0}), 200

@bp_equipment.route('/api/v1/equipment/getEquipmentRecordList', methods=['POST'])
@login_required
def getEquipmentRecordList():
    try:
        num = request.json["num"]
        equipmentType = request.json["equipmentType"]
        equipmentID = request.json["equipmentID"]
    except:
        return jsonify({"errCode": 1, "errMsg": "bad arguments"}), 200
    startDate = request.json["startDate"] if "startDate" in request.json.keys() else None
    endDate = request.json["endDate"] if "endDate" in request.json.keys() else None
    recordList_raw, getStatus = EquipmentService.get_equipment_recordList(equipmentType, equipmentID,startDate, endDate, num)

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
                    "status": item.status
    })
    return jsonify({"errCode": 0, "recordList": recordList}), 200

@bp_equipment.route('/api/v1/equipment/swapEquipmentOrder', methods=['POST'])
@login_required
def swapEquipmentOrder():
    try:
        equipmentType1 = request.json["equipmentType1"]
        equipmentType2 = request.json["equipmentType2"]
    except:
        return jsonify({"errCode": 1, "errMsg": "bad arguments"}), 200
    msg, swapStatus = EquipmentService.swap_equipmentOrder(equipmentType1, equipmentType2)
    if not swapStatus:
        return jsonify({"errCode": 1, "errMsg": msg}), 200
    else:
        return jsonify({"errCode": 0}), 200

@bp_equipment.route('/api/v1/equipment/deleteEquipment', methods=['POST'])
@login_required
def deleteEquipment():
    try:
        Type = request.json["equipmentType"]
        id = request.json["equipmentID"]
    except:
        return jsonify({"errCode": 1, "errMsg": "bad arguments"}), 200
    
    msg, DeleteStatus = EquipmentService.deleteEquipment(Type, id)
    if not DeleteStatus:
        return jsonify({"errCode": 1, "errMsg": msg}), 200
    return jsonify({"errCode": 0}), 200