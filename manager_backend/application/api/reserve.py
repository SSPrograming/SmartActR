from logging import exception
from flask import request, jsonify, Blueprint, g
from config import query_yaml
from application.models import Admin
from application.database import db
from application.service import ReserveService, UserService, EquipmentService
from application.utils import generate_jwt
from .login_decorator import login_required

bp_reserve = Blueprint(
    'reserve',
    __name__
)

@bp_reserve.route('/api/v1/reserve/getTodayRecord', methods=['GET'])
@login_required
def getTodayRecord():
    record_list_raw = ReserveService.get_today_record()
    record_list = []
    for item in record_list_raw:
        record_list.append({
            "recordID": item.recordID,
			"postTime": item.postTime.strftime("%Y-%m-%d %H:%M"),
			"reserveDate": item.reserveDate.strftime("%Y-%m-%d"),
			"startTime": item.startTime.strftime("%H:%M"),
			"endTime": item.endTime.strftime("%H:%M"),
			"userName": UserService.get_name_by_id(item.userID),
			"status": item.status,
			"equipmentName": EquipmentService.get_name_by_type(item.equipmentType)[0]
        })
    return jsonify({"errCode": 0, "recordList": record_list}), 200


@bp_reserve.route('/api/v1/reserve/getHistoryRecord', methods=['POST'])
@login_required
def getHistoryRecord():
    try:
        start_date = request.json["startDate"]
        end_date = request.json["endDate"]
    except:
        return jsonify({"errCode": 1, "errMsg": "bad arguments"}), 200
    try:
        record_list_raw = ReserveService.get_history_record(start_date, end_date)
    except:
        return jsonify({"errCode": 1, "errMsg": "bad arguments"}), 200
    record_list = []
    for item in record_list_raw:
        record_list.append({
            "recordID": item.recordID,
			"postTime": item.postTime.strftime("%Y-%m-%d %H:%M") if item.postTime else "undefined",
			"reserveDate": item.reserveDate.strftime("%Y-%m-%d") if item.reserveDate else "undefined",
			"startTime": item.startTime.strftime("%H:%M") if item.startTime else "undefined",
			"endTime": item.endTime.strftime("%H:%M") if item.endTime else "undefined",
			"userName": UserService.get_name_by_id(item.userID),
			"status": item.status,
			"equipmentName": EquipmentService.get_name_by_type(item.equipmentType)[0]
        })
    return jsonify({"errCode": 0, "recordList": record_list}), 200