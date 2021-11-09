from logging import exception
from flask import request, jsonify, Blueprint, g
import mjwt
from config import query_yaml
from application.services import UserService, EquipmentService, ReserveService
from .login_decorator import login_required
import operator, datetime


bp_reserve = Blueprint(
    'reserve',
    __name__
)

@bp_reserve.route('/api/v1/reserve/getEquipmentStatus', methods=['POST'])
#@login_required
def getEquipmentStatus():
    try:
        targetType = request.json['equipmentType']
        targetID = request.json['equipmentID']
        year = request.json['year']
        month = request.json['month']
        day = request.json['day']
        date = datetime.date(year, month, day)
    except Exception as e:
        print(e)
        return jsonify({"errCode": 1,"errMsg": "bad agruments"}), 200

    targetEquipment = EquipmentService.get_single_equipment(targetType, targetID)
    targetEquipmentType = EquipmentService.get_single_equipmentType(targetType)
    if targetEquipment is None:
        return jsonify({"errCode": 1,"errMsg": "无此设备"}), 200
    
    if targetEquipment.equipmentStatus != 'fine':
        return jsonify({"errCode": 1,"errMsg": "设备损坏，不可使用"}), 200

    occupation, hasOccupation = ReserveService.get_occupation_of_day(date)

    records = ReserveService.get_record_of_single_equipment(date, targetType, targetID)
    
    for record in records:
        occupation.append({"startTime": record.startTime,
                                          "endTime": record.endTime})
    occupation = sorted(occupation, key=operator.itemgetter('startTime'))
    if len(occupation)<1:
        return jsonify({
            "errCode": 0,
            "equipmentName": targetEquipmentType.equipmentName,
            "equipmentDescription": targetEquipmentType.equipmentDescription,
            "equipmentSpareTime": [
                {
                    "startTime": "08:00",
                    "endTime": "22:00"
                }
            ]
        })
    print(occupation)
    occupation_merged = []
    cur_item = occupation[0] # to be merged
    for item in occupation:
        if item["startTime"]<=cur_item["endTime"]:
            cur_item["endTime"] = max(cur_item["endTime"], item["endTime"])
        else:
            occupation_merged.append(cur_item)
            cur_item = item
    return jsonify({
            "errCode": 0,
            "equipmentName": targetEquipmentType.equipmentName,
            "equipmentDescription": targetEquipmentType.equipmentDescription,
            "equipmentSpareTime": 
            occupation_merged
        }), 200