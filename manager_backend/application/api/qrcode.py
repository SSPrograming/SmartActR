from logging import exception
from flask import json, request, jsonify, Blueprint, g
from config import query_yaml
import os
from application.database import db
from application.service import ReserveService, UserService, EquipmentService
from application.utils import generate_jwt, hash_code
from .login_decorator import login_required
import qrcode
import datetime

bp_qrcode = Blueprint(
    'qrcode',
    __name__
)

@bp_qrcode.route('/api/v1/qrcode/refreshQRCode', methods=['POST'])
@login_required
def refreshQRCode():
    try:
        equipment_type = request.json['equipmentType']
        equipment_id = request.json['equipmentID']
    except:
        return jsonify({"errCode": 1, "errMsg": "bad arguments"}), 200
    raw_str = str(equipment_type) + '-' + str(equipment_id) + '-' + str(datetime.datetime.now())
    raw_code = hash_code(raw_str)
    print(raw_code)
    img_name = str(equipment_type)+"-"+str(equipment_id)+".png"
    img_url = query_yaml("app.MANAGERSERVERURL")+"image/qrcode/"+img_name
    msg, refreshStatus = EquipmentService.update_hashcode(equipment_type, equipment_id,raw_code, img_url)
    if refreshStatus==False:
        return jsonify({"errCode": 1, "errMsg": msg}), 200
    qr_img = qrcode.make(raw_code)
    print(os.getcwd())
    qr_img.save("./application/static/qrcode/"+img_name)
    return jsonify({"errCode": 0,"qrcodeURL": img_url}), 200

@bp_qrcode.route('/api/v1/qrcode/getQRCode', methods=['POST'])
@login_required
def getQRCode():
    try:
        equipment_type = request.json['equipmentType']
        equipment_id = request.json['equipmentID']
    except:
        return jsonify({"errCode": 1, "errMsg": "bad arguments"}), 200
    msg, status = EquipmentService.get_qrcodeURL(equipment_type, equipment_id)
    if status:
        return jsonify({"errCode": 0, "qrcodeURL": msg}), 200
    else:
        return jsonify({"errCode": 1, "errMsg": msg}), 200