from application.database import db
from application.models import TableNotcie
from application.utils import strToTime, strToDate, now
import datetime

class NoticeService():
    def query_notice(num, query_type, query_startDate=None, query_endDate=None, query_str=None):
        if num==-1:
            if query_type==0:
                return TableNotcie.query.all()
            elif query_type==1:
                startDate = strToDate(query_startDate)
                endDate = strToDate(query_endDate)
                return TableNotcie.query.filter(TableNotcie.noticeDate>=startDate,
                                                TableNotcie.noticeDate<=endDate).all()
            elif query_type==2:
                return TableNotcie.query.filter(TableNotcie.noticeContent.like('%'+query_str+'%')).all()
            
            elif query_type==3:
                startDate = strToDate(query_startDate)
                endDate = strToDate(query_endDate)
                return TableNotcie.query.filter(TableNotcie.noticeDate>=startDate,
                                                TableNotcie.noticeDate<=endDate,
                                                TableNotcie.noticeContent.like('%'+query_str+'%')).all()
            else:
                return None
        elif num >=0:
            if query_type==0:
                return TableNotcie.query.limit(num).all()
            elif query_type==1:
                startDate = strToDate(query_startDate)
                endDate = strToDate(query_endDate)
                return TableNotcie.query.filter(TableNotcie.noticeDate>=startDate,
                                                TableNotcie.noticeDate<=endDate).limit(num).all()
            elif query_type==2:
                return TableNotcie.query.filter(TableNotcie.noticeContent.like('%'+query_str+'%')).limit(num).all()
            elif query_type==3:
                startDate = strToDate(query_startDate)
                endDate = strToDate(query_endDate)
                return TableNotcie.query.filter(TableNotcie.noticeDate>=startDate,
                                                TableNotcie.noticeDate<=endDate,
                                                TableNotcie.noticeContent.like('%'+query_str+'%')).limit(num).all()
            else:
                return None
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