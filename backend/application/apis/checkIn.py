from flask import  jsonify, Blueprint, g, request
from application.services import CheckInService
from .login_decorator import login_required

bp_checkIn = Blueprint(
    'checkIn',
    __name__
)


@bp_checkIn.route('/api/v1/checkIn', methods=['POST'])
@login_required
def checkIn():
    try:
        hashCode = request.json["hashCode"]
    except:
        return jsonify({"errCode": 1, "errMsg": "bad arguments"}), 200
    t = CheckInService.test(hashCode, g.userID)
    return jsonify({
	    "errCode": 0, #0代表签到失败，1签到成功
        "checkInStatus": t
        })