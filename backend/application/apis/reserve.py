from flask import request, jsonify, Blueprint, g
from application.services import EquipmentService, ReserveService, CheckInService
from .login_decorator import login_required
import operator
import datetime
import math
from application.utils import now, calculate_total_time, reduce_to_nowTime, calculate_spare_time

bp_reserve = Blueprint(
    'reserve',
    __name__
)


@bp_reserve.route('/user-api/v1/reserve/getEquipmentStatus', methods=['POST'])
@login_required
def getEquipmentStatus():
    try:
        targetType = request.json['equipmentType']
        targetID = request.json['equipmentID']
        year = request.json['year']
        month = request.json['month']
        day = request.json['date']
        date = datetime.date(year, month, day)
    except Exception as e:
        print(e)
        return jsonify({"errCode": 1, "errMsg": "bad agruments"}), 200
    targetEquipment = EquipmentService.get_single_equipment(
        targetType, targetID)
    targetEquipmentType = EquipmentService.get_single_equipmentType(targetType)
    if targetEquipment is None:
        return jsonify({"errCode": 1, "errMsg": "无此设备"}), 200
    if targetEquipment.equipmentStatus != '完好':
        return jsonify({"errCode": 1, "errMsg": "设备损坏，不可使用"}), 200
    occupation, hasOccupation = ReserveService.get_occupation_of_day(date)
    records = ReserveService.get_record_of_single_equipment(
        date, targetType, targetID)
    for record in records:
        occupation.append({"startTime": record.startTime,
                           "endTime": record.endTime})
    occupation = sorted(occupation, key=operator.itemgetter('startTime'))
    occupation_merged = []
    if len(occupation):
        cur_item = occupation[0]  # to be merged
        for item in occupation:
            if item["startTime"] <= cur_item["endTime"]:
                cur_item["endTime"] = max(cur_item["endTime"], item["endTime"])
            else:
                occupation_merged.append(cur_item)
                cur_item = item
        occupation_merged.append(cur_item)
    spareTime = [{"startTime": "08:00", "endTime": "22:00"}]

    for i in range(len(occupation_merged)):
        occupation_merged[i]["startTime"] = occupation_merged[i]["startTime"].strftime(
            "%H:%M")
        occupation_merged[i]["endTime"] = occupation_merged[i]["endTime"].strftime(
            "%H:%M")

    for item in occupation_merged:
        spareTime_last = spareTime[-1]
        spareTime.pop()
        splitTime_1 = {
            "startTime": spareTime_last["startTime"], "endTime": item["startTime"]}
        if splitTime_1["startTime"] != splitTime_1["endTime"]:
            spareTime.append(splitTime_1)
        splitTime_2 = {"startTime": item["endTime"],
                       "endTime": spareTime_last["endTime"]}
        if splitTime_2["startTime"] != splitTime_2["endTime"]:
            spareTime.append(splitTime_2)

    remove_end = 0
    now_datetime = now()
    for item in spareTime:
        item_endTime = datetime.datetime.strptime(item["endTime"], '%H:%M')
        item_endTime = item_endTime.replace(year=year, month=month, day=day)
        if item_endTime < now_datetime:
            remove_end += 1
        else:
            break
    del spareTime[:remove_end]
    if len(spareTime):
        item_startTime = datetime.datetime.strptime(
            spareTime[0]["startTime"], '%H:%M')
        item_startTime = item_startTime.replace(
            year=year, month=month, day=day)
        if item_startTime < now_datetime:
            minute_round = math.ceil(now_datetime.minute / 15) * 15
            hour = now_datetime.hour
            if minute_round == 60:
                hour += 1
                minute_round = 0
            item_startTime = item_startTime.replace(
                hour=hour, minute=minute_round)
            print(item_startTime)
            spareTime[0]["startTime"] = item_startTime.strftime("%H:%M")
            if spareTime[0]["startTime"] == spareTime[0]["endTime"]:
                del spareTime[0]

    return jsonify({
        "errCode": 0,
        "equipmentName": targetEquipmentType.equipmentName,
        "equipmentDescription": targetEquipmentType.equipmentDescription,
        "equipmentSpareTime": spareTime,
        "equipmentImageURL": targetEquipmentType.equipmentImageURL
    }), 200


@bp_reserve.route('/user-api/v1/reserve/getAllEquipmentStatus', methods=['POST'])
@login_required
def getAllEquipmentStatus():
    try:
        year = request.json['year']
        month = request.json['month']
        day = request.json['date']
        date = datetime.date(year, month, day)
    except Exception as e:
        print(e)
        return jsonify({"errCode": 1, "errMsg": "bad agruments"}), 200
    equipments = EquipmentService.get_all_equipment()
    equipmentStatuses = []
    for equipment in equipments:
        if equipment.equipmentStatus == "损坏":
            continue
        occupation, hasOccupation = ReserveService.get_occupation_of_day(date)
        targetEquipmentType = EquipmentService.get_single_equipmentType(
            equipment.equipmentType)
        records = ReserveService.get_record_of_single_equipment(
            date, equipment.equipmentType, equipment.equipmentID)
        for record in records:
            occupation.append({"startTime": record.startTime,
                               "endTime": record.endTime})
        occupation = sorted(occupation, key=operator.itemgetter('startTime'))
        occupation_merged = []
        if len(occupation):
            cur_item = occupation[0]  # to be merged
            for item in occupation:
                if item["startTime"] <= cur_item["endTime"]:
                    cur_item["endTime"] = max(
                        cur_item["endTime"], item["endTime"])
                else:
                    occupation_merged.append(cur_item)
                    cur_item = item
            occupation_merged.append(cur_item)
        occupation_merged = reduce_to_nowTime(occupation_merged, date)
        total_time_occupied = calculate_total_time(occupation_merged)
        spare_time = calculate_spare_time(date)
        if spare_time == datetime.timedelta(0) or total_time_occupied/spare_time >= 1:
            occupationStatus = 2
        elif total_time_occupied/spare_time >= 0.5:
            occupationStatus = 1
        else:
            occupationStatus = 0

        # TODO: 判断占用状态
        equipmentStatuses.append({"equipmentType": equipment.equipmentType,
                                  "equipmentName": targetEquipmentType.equipmentName,
                                  "equipmentID": equipment.equipmentID,
                                  "equipmentImageURL": targetEquipmentType.equipmentImageURL,
                                  "equipmentStatus": occupationStatus})

    return jsonify({
        "errCode": 0,
        "status": equipmentStatuses
    })


@bp_reserve.route('/user-api/v1/reserve/reserveEquipment', methods=['POST'])
@login_required
def reserveEquipment():
    try:
        year = request.json['year']
        month = request.json['month']
        day = request.json['date']
        strStartTime = request.json['startTime']
        strEndTime = request.json['endTime']
        targetType = request.json['equipmentType']
        targetID = request.json['equipmentID']
        date = datetime.date(year, month, day)
        StartTime = ReserveService.strToTime(strStartTime)
        EndTime = ReserveService.strToTime(strEndTime)
    except Exception as e:
        print(e)
        return jsonify({"errCode": 1, "errMsg": "bad agruments"}), 200

    occupations, hasoccupation = ReserveService.get_occupation_of_day(date)
    if hasoccupation:
        for item in occupations:
            if not (StartTime >= item['endTime'] or EndTime <= item['startTime']):
                return jsonify({"errCode": 1, "errMsg": "该时间段被占用"}), 200
    existedRecords = ReserveService.get_record_of_single_equipment(
        date, targetType, targetID)
    for record in existedRecords:
        if not (StartTime >= record.endTime or EndTime <= record.startTime):
            return jsonify({"errCode": 1, "errMsg": "该时间段被占用"}), 200

    if ReserveService.add_reserve_record(g.userID, date, StartTime, EndTime, targetType, targetID):
        return jsonify({"errCode": 0, "errMsg": ""}), 200
    else:
        return jsonify({"errCode": 1, "errMsg": "设备不存在或已被占用"})


@bp_reserve.route('/user-api/v1/reserve/cancelReserve', methods=['POST'])
@login_required
def cancelReserve():
    print(request.json)
    try:
        recordID = request.json['reserveID']
    except Exception as e:
        print(e)
        return jsonify({"errCode": 1, "errMsg": "bad agruments"}), 200
    msg, status = ReserveService.delete_reserve_record(g.userID, recordID)
    if status:
        return jsonify({"errCode": 0}), 200
    else:
        return jsonify({"errCode": 1, "errMsg": msg}), 200


@bp_reserve.route('/user-api/v1/reserve/getHistoryReserveInfo', methods=['GET'])
@login_required
def getHistoryReserveInfo():
    history_record = ReserveService.get_history_record(g.userID)
    resp_record = []
    for item in history_record:
        resp_record.append({
            "reserveID": item.recordID,
            "equipmentName": EquipmentService.get_name_by_Type(item.equipmentType),
            "equipmentID": item.equipmentID,
            "startTime": item.startTime.strftime("%H:%M"),
            "endTime": item.endTime.strftime("%H:%M"),
            "year": item.reserveDate.year,
            "month": item.reserveDate.month,
            "date": item.reserveDate.day,
            "status": item.status
        })
    return jsonify({
        "errCode": 0,
        "info": resp_record
    }), 200


@bp_reserve.route('/user-api/v1/reserve/getCurrentReserveInfo', methods=['GET'])
@login_required
def getCurrentReserveInfo():
    current_record = ReserveService.get_current_record(g.userID)
    resp_record = []
    for item in current_record:
        resp_record.append({
            "reserveID": item.recordID,
            "startTime": item.startTime.strftime("%H:%M"),
            "equipmentName": EquipmentService.get_name_by_Type(item.equipmentType),
            "equipmentID": item.equipmentID,
            "endTime": item.endTime.strftime("%H:%M"),
            "year": item.reserveDate.year,
            "month": item.reserveDate.month,
            "date": item.reserveDate.day,
            "status": item.status
        })
    return jsonify({
        "errCode": 0,
        "info": resp_record
    }), 200
