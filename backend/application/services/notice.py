from application.database import db
from application.models import Equipment, equipmentType, TableNotcie
import datetime

class NoticeService:
    def get_notice():
        return TableNotcie.query.filter(TableNotcie.noticeID==TableNotcie.query.count()).all()
        #return TableNotcie.query.filter(TableNotcie.noticeID==100).all()
        #return TableNotcie.query.all()