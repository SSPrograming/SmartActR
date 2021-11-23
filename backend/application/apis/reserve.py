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
@login_required
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
        print(record.startTime)
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
            ],
            "equipmentOccupiedTime": []
        })
    print(occupation)
    occupation_merged = []
    cur_item = occupation[0] #to be merged
    for item in occupation:
        if item["startTime"]<=cur_item["endTime"]:
            cur_item["endTime"] = max(cur_item["endTime"], item["endTime"])
        else:
            occupation_merged.append(cur_item)
            cur_item = item
    occupation_merged.append(cur_item)
    spareTime=[{"startTime": "08:00", "endTime":"22:00"}]

    for i in range(len(occupation_merged)):
        occupation_merged[i]["startTime"] = occupation_merged[i]["startTime"].strftime("%H:%M")
        occupation_merged[i]["endTime"] = occupation_merged[i]["endTime"].strftime("%H:%M")
    
    for item in occupation_merged:
        spareTime_last = spareTime[-1]
        spareTime.pop()
        splitTime_1 = {"startTime": spareTime_last["startTime"], "endTime": item["startTime"]}
        if splitTime_1["startTime"] != splitTime_1["endTime"]:
            spareTime.append(splitTime_1)
        splitTime_2 = {"startTime": item["endTime"], "endTime": spareTime_last["endTime"]}
        if splitTime_2["startTime"] != splitTime_2["endTime"]:
            spareTime.append(splitTime_2)

    return jsonify({
            "errCode": 0,
            "equipmentName": targetEquipmentType.equipmentName,
            "equipmentDescription": targetEquipmentType.equipmentDescription,
            "equipmentSpareTime": 
            spareTime,
            "equipmentOccupiedTime":
            occupation_merged
        }), 200


@bp_reserve.route('/api/v1/reserve/getAllEquipmentStatus', methods=['POST'])
@login_required
def getAllEquipmentStatus():
    try:
        year = request.json['year']
        month = request.json['month']
        day = request.json['day']
        date = datetime.date(year, month, day)
    except Exception as e:
        print(e)
        return jsonify({"errCode": 1,"errMsg": "bad agruments"}), 200
    equipments = EquipmentService.get_all_equipment()
    equipmentStatuses= []
    for equipment in equipments:
        occupation, hasOccupation = ReserveService.get_occupation_of_day(date)
        targetEquipmentType = EquipmentService.get_single_equipmentType(equipment.equipmentType)
        records = ReserveService.get_record_of_single_equipment(date, equipment.equipmentType, equipment.equipmentID)
        for record in records:
            occupation.append({"startTime": record.startTime,
                               "endTime": record.endTime})
            occupation = sorted(occupation, key=operator.itemgetter('startTime'))
        occupation_merged = []
        if len(occupation)>0:
            cur_item = occupation[0] #to be merged
            for item in occupation:
                if item["startTime"]<=cur_item["endTime"]:
                    cur_item["endTime"] = max(cur_item["endTime"], item["endTime"])
                else:
                    occupation_merged.append(cur_item)
                    cur_item = item
        # TODO: 判断占用状态
        equipmentStatuses.append({"equipmentType": equipment.equipmentType,
                                  "equipmentName": targetEquipmentType.equipmentName,
                                  "equipmentID": equipment.equipmentID,
                                  "equipmentStatus": 0})
    
    return jsonify({
        "errCode": 0,
        "status": equipmentStatuses
    })


@bp_reserve.route('/api/v1/reserve/reserveEquipment', methods=['POST'])
@login_required
def reserveEquipment():
    try:
        year = request.json['year']
        month = request.json['month']
        day = request.json['day']
        strStartTime = request.json['startTime']
        strEndTime = request.json['endTime']
        targetType = request.json['equipmentType']
        targetID = request.json['equipmentID']
        date = datetime.date(year, month, day)
        StartTime = ReserveService.strToTime(strStartTime)
        EndTime = ReserveService.strToTime(strEndTime)
    except Exception as e:
        print(e)
        return jsonify({"errCode": 1,"errMsg": "bad agruments"}), 200
    
    occupations, hasoccupation = ReserveService.get_occupation_of_day(date)
    if hasoccupation:
        for item in occupations:
            print(item)
            if not (StartTime>=item['endTime'] or EndTime<=item['startTime']):
                return jsonify({"errCode": 1,"errMsg": "该时间段被占用"}), 200
    existedRecords = ReserveService.get_record_of_single_equipment(date, targetType, targetID)
    for record in existedRecords:
        print(record.startTime)
        if not (StartTime>=record.endTime or EndTime<=record.startTime):
            return jsonify({"errCode": 1,"errMsg": "该时间段被占用"}), 200
    
    if ReserveService.add_reserve_record(g.userID, date, StartTime, EndTime, targetType, targetID):
        return jsonify({"errCode": 0,"errMsg": ""}), 200
    else:
        return jsonify({"errCode": 1, "errMsg": "设备不存在或已被占用"})