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


@bp_notice.route('/manager-api/v1/notice/getNoticeList', methods=['POST'])
@login_required
def getNoticeList():
    try:
        num = request.json['num']
        query_startDate = None
        query_endDate = None
        query_str = None
        if 'queryStartDate' in request.json.keys():
            query_startDate = request.json['queryStartDate']
        if 'queryEndDate' in request.json.keys():
            query_endDate = request.json['queryEndDate']
        if 'queryStr' in request.json.keys():
            query_str = request.json['queryStr']
    except Exception as e:
        print(e)
        return jsonify({"errCode": 1, "errMsg": "bad arguments"}), 200

    try:
        query_result = NoticeService.query_notice(
            num, query_startDate, query_endDate, query_str)
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
        "noticeList": noticeList, "errCode": 0
    }), 200


@bp_notice.route('/manager-api/v1/notice/createNotice', methods=['POST'])
@login_required
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


@bp_notice.route('/manager-api/v1/notice/updateNotice', methods=['POST'])
@login_required
def updateNotice():
    try:
        notice_content = request.json['noticeContent']
        expire_date = request.json['expireDate']
        notice_id = request.json['noticeID']
    except:
        return jsonify({"errCode": 1, "errMsg": "bad arguments"}), 200

    update_status = NoticeService.update_notice(
        notice_content, expire_date, notice_id)

    if update_status:
        return jsonify({"errCode": 0}), 200
    else:
        return jsonify({"errCode": 1, "errMsg": "bad arguments"}), 200


@bp_notice.route('/manager-api/v1/notice/deleteNotice', methods=['POST'])
@login_required
def deleteNotice():
    try:
        notice_id = request.json['noticeID']
    except:
        return jsonify({"errCode": 1, "errMsg": "bad arguments"}), 200

    msg, delete_status = NoticeService.delete_notice(notice_id)
    if delete_status:
        return jsonify({"errCode": 0}), 200
    else:
        return jsonify({"errCode": 1, "errMsg": msg}), 200
