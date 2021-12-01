from logging import exception
from flask import request, jsonify, Blueprint, g
from config import query_yaml
from application.models import Admin
from application.database import db
from application.service import ReserveService, UserService, EquipmentService
from application.utils import generate_jwt
from .login_decorator import login_required

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
        "equipmentImage": item.equipmentImageURL
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

@bp_equipment.route('/api/v1/equipment/AddEquipmentType', methods=['POST'])
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
    new_img_file_name = new_img_file.filename if new_img_file is not None else None
    msg, updateStatus = EquipmentService.update_equipmentType(target_type, new_name, new_description, new_img_file_name)
    if not updateStatus:
        return jsonify({"errCode": 1, "errMsg": msg})
    if new_img_file:
        new_img_file.save("./application/static/equipment/"+str(target_type)+"_"+new_img_file_name)
    return jsonify({"errCode": 0}), 200
    