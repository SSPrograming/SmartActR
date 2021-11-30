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
    print(type(request.form))
    testFile = request.files.get('testFile')
    testFileName = request.files['testFile'].name
    print(type(testFile))
    print(testFile)
    testFile.save('./application/static/test/testFile.jpg')
    testFileURL = query_yaml("app.MANAGERSERVERURL")+"image/test/testFile.jpg"
    return jsonify({"errCode": 0,"testPicURL": testFileURL}), 200