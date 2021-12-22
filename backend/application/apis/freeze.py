from flask import  jsonify, Blueprint, g, request
from application.services import UserService
from .login_decorator import login_required

bp_freeze = Blueprint(
    'freeze',
    __name__
)


@bp_freeze.route('/user-api/v1/instruction/getFreezeStatus', methods=['GET'])
@login_required 
def get_freeze_status():
    msg_or_info, getStatus = UserService.get_freeze_info(g.userID)
    if not getStatus:
        return jsonify({"errCode": 1, "errMsg": msg_or_info}), 200
    return jsonify({
        "freezeStatus" : msg_or_info["status"],
        "freezeDate" : msg_or_info["date"],
        "errCode": 0
    }), 200
