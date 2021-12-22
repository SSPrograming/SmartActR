from flask import jsonify, Blueprint, g
from application.services import  NoticeService
from .login_decorator import login_required

bp_notice = Blueprint(
    'notice',
    __name__
)

@bp_notice.route('/user-api/v1/reserve/getNotice', methods=['GET'])
@login_required
def notice():
    notice = NoticeService.get_notice()
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
	    "errCode": 0,
	    "errMsg": "",
	    "noticeContent": notice.noticeContent,
        "noticeDate": noticeDate_str, #格式的样例："2021-11-09"
        "expireDate": expireDate_str, #格式的样例："2021-11-12"
        })
    