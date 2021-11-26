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