from flask import  jsonify, Blueprint, g, request
from application.services import UserService
from .login_decorator import login_required

bp_freeze = Blueprint(
    'freeze',
    __name__
)


@bp_freeze.route('/api/v1/instruction/getFreezeStatus', methods=['GET'])
# @login_required 
def get_freeze_status():
    #freezeStatus,freezeDate = UserService.get_freeze_info(str(g.userID))
    freezeStatus,freezeDate = UserService.get_freeze_info('2')
    return jsonify({
        "freezeStatus" : freezeStatus,
        "freezeDate" : freezeDate
    }) #返回freezeStatus为0/1，未冻结/冻结
