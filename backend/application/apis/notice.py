from logging import exception
from flask import request, jsonify, Blueprint, g
from werkzeug.wrappers.request import PlainRequest
import mjwt
import datetime
from config import query_yaml
from application.services import UserService, EquipmentService, NoticeService
from .login_decorator import login_required
import requests

bp_notice = Blueprint(
    'notice',
    __name__
)

@bp_notice.route('/api/v1/reserve/getNotice', methods=['GET'])
#@login_required
def notice():
    notice = NoticeService.get_notice()
    print(type(notice))
    if notice is None:
        return jsonify({
	    "errCode": 1,
	    "errMsg": "无可获取公告",
	    "noticeContent":"",
        "noticeDate":"", #格式的样例："2021-11-09"
        "expireDate": "", #格式的样例："2021-11-12"
        }) 
    else:
        print("Date:")
        print(notice.noticeDate)
        noticeDate_str = str(notice.noticeDate)
        expireDate_str = str(notice.expireDate)
        return jsonify({
	    "errCode": 1,
	    "errMsg": "",
	    "noticeContent": notice.noticeContent,
        "noticeDate": noticeDate_str, #格式的样例："2021-11-09"
        "expireDate": expireDate_str, #格式的样例："2021-11-12"
        })
    