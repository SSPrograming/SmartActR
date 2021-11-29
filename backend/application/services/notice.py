from application.database import db
from application.models import Equipment, equipmentType, TableNotcie
import datetime

class NoticeService:
    def get_notice():
        return TableNotcie.query.order_by(TableNotcie.noticeID.desc()).first()