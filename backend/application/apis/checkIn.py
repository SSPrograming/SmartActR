from logging import exception
from flask import request, jsonify, Blueprint, g
from werkzeug.wrappers.request import PlainRequest
import mjwt
import datetime,time
from config import query_yaml
from application.services import UserService, EquipmentService, NoticeService,CheckInService
from .login_decorator import login_required
import requests

bp_checkIn = Blueprint(
    'checkIn',
    __name__
)


@bp_checkIn.route('/api/v1/checkIn', methods=['POST'])
# @login_required
def checkIn():
    # code = request.json['equipmentType']
    # currentTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
    # j = {'hash':'1111'}
    # print("t: ",t)
    # print("currentTime:",currentTime)
    # print(type(currentTime))
    #     test     hash = request.json['equipmentType']
    t = CheckInService.test('testhash')
    return jsonify({
	    "errCode": t, #0代表签到失败，1签到成功
        })