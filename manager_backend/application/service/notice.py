from application.database import db
from application.models import TableNotcie
from application.utils import strToTime, strToDate

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
                return TableNotcie.query.filter(TableNotcie.noticeContent.like(query_str)).all()
            
            elif query_type==3:
                startDate = strToDate(query_startDate)
                endDate = strToDate(query_endDate)
                return TableNotcie.query.filter(TableNotcie.noticeDate>=startDate,
                                                TableNotcie.noticeDate<=endDate,
                                                TableNotcie.noticeContent.like(query_str)).all()
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
                return TableNotcie.query.filter(TableNotcie.noticeContent.like(query_str)).limit(num).all()
            elif query_type==3:
                startDate = strToDate(query_startDate)
                endDate = strToDate(query_endDate)
                return TableNotcie.query.filter(TableNotcie.noticeDate>=startDate,
                                                TableNotcie.noticeDate<=endDate,
                                                TableNotcie.noticeContent.like(query_str)).limit(num).all()
            else:
                return None
        else:
            return None