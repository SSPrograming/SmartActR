from logging import exception
from flask import request, jsonify, Blueprint, g
from config import query_yaml
from application.models import Admin
from application.database import db
from application.service import NoticeService
from application.utils import generate_jwt
from .login_decorator import login_required

bp_notice = Blueprint(
    'notice',
    __name__
)

@bp_notice.route('/api/v1/notice/getNoticeList', methods=['POST'])
#@login_required
def getNoticeList():
    try:
        num = request.json['num']
        query_type = request.json['queryType']
        query_startDate = None
        query_endDate = None
        query_str = None
        if query_type==1 or query_type==3:
            query_startDate = request.json['queryStartDate']
            query_endDate = request.json['queryEndDate']
        if query_type==2 or query_type==3:
            query_str = request.json['queryStr']
    except Exception as e:
        print(e)
        return jsonify({"errCode": 1, "errMsg": "bad arguments"}), 200
    
    try:
        query_result = NoticeService.query_notice(num, query_type, query_startDate, query_endDate, query_str)
    except Exception as e:
        print(e)
        return jsonify({"errCode": 1, "errMsg": "bad arguments"}), 200
    
    noticeList = []
    for item in query_result:
        noticeList.append({
            "noticeID": item.noticeID,
			"postDate": item.noticeDate.strftime("%Y-%m-%d"),
			"expireDate": item.expireDate.strftime("%Y-%m-%d"),
			"content": item.noticeContent
        })
    
    return jsonify({
        "noticeList":noticeList, "errCode": 0
    }), 200
        

@bp_notice.route('/api/v1/notice/createNotice', methods=['POST'])
#@login_required
def createNotice():
    try:
        notice_content = request.json['noticeContent']
        expire_date = request.json['expireDate']
    except:
        return jsonify({"errCode": 1, "errMsg": "bad arguments"}), 200

    create_status = NoticeService.create_notice(notice_content, expire_date)
    if create_status:
        return jsonify({"errCode": 0}), 200
    else:
        return jsonify({"errCode": 1, "errMsg": "bad arguments"}), 200