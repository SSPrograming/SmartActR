from application.database import db
from application.models import TableNotcie
from application.utils import strToTime, strToDate, now
import datetime
from sqlalchemy import and_
class NoticeService():
    def query_notice(num, query_startDate=None, query_endDate=None, query_str=None):
        query_condition = and_()
        if query_startDate is not None:
            query_condition = and_(query_condition, TableNotcie.noticeDate>=query_startDate)
        if query_endDate is not None:
            query_condition = and_(query_condition, TableNotcie.noticeDate<=query_endDate)
        if query_str is not None:
            query_condition = and_(query_condition, TableNotcie.noticeContent.like('%'+query_str+'%'))
        if num==-1:
            return TableNotcie.query.filter(query_condition).all()
        elif num >=0:
            return TableNotcie.query.filter(query_condition).limit(num).all()
        else:
            return None

    def create_notice(notice_content, expire_date):
        new_notice = TableNotcie()
        new_notice.noticeContent = notice_content
        now_datetime = now()
        now_date = datetime.date(now_datetime.year, now_datetime.month, now_datetime.day)
        new_notice.noticeDate = now_date
        new_notice.expireDate = strToDate(expire_date)
        try:
            db.session.add(new_notice)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            db.session.rollback()
            return False
    
    def update_notice(notice_content, expire_date, notice_id):
        target_notice = TableNotcie.query.filter(TableNotcie.noticeID==notice_id).first()
        if target_notice is None:
            return False
        try:
            target_notice.expireDate = strToDate(expire_date)
            target_notice.noticeContent = notice_content
            now_datetime = now()
            now_date = datetime.date(now_datetime.year, now_datetime.month, now_datetime.day)
            target_notice.noticeDate = now_date
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            db.session.rollback()
            return False
    
    def delete_notice(notice_id):
        target_notice = TableNotcie.query.filter(TableNotcie.noticeID==notice_id).first()
        if target_notice is None:
            return "无此公告", False
        try:
            db.session.delete(target_notice)
            db.session.commit()
            return "ok", True
        except:
            db.session.rollback()
            return "bad arguments", False