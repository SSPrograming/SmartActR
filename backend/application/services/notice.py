from application.database import db
from application.models import TableNotcie


class NoticeService:
    def get_notice():
        return TableNotcie.query.order_by(TableNotcie.noticeID.desc()).first()
