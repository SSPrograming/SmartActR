from flask import  jsonify, Blueprint, g, request
from application.services import UserService
from .login_decorator import login_required

bp_freeze = Blueprint(
    'freeze',
    __name__
)


@bp_freeze.route('/api/v1/instruction/getFreezeStatus', method=['GET'])
@login_required 
def get_freeze_status():
    UserService.get_freeze_info(g.userID)
    return jsonify({"errCode":0}),200
