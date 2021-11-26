from application.database import db
from application.models import Reserve_Record
from application.utils import strToTime, strToDate, now
import datetime

class ReserveService():
    def get_today_record():
        now_datetime = now()
        now_date = datetime.date(now_datetime.year, now_datetime.month, now_datetime.day)
        record_list = Reserve_Record.query.filter(Reserve_Record.reserveDate==now_date).all()
        return record_list

    def get_history_record(start_date_raw, end_date_raw):
        start_date = strToDate(start_date_raw)
        end_date = strToDate(end_date_raw)
        record_list = Reserve_Record.query.filter(Reserve_Record.reserveDate>=start_date,
                                                  Reserve_Record.reserveDate<=end_date).all()
        return record_list