from application.database import db
from application.models import Reserve_Record
from application.utils import strToTime, strToDate, now, WechatService
import datetime
from sqlalchemy import and_
from flask import current_app
from application.service import UserService, EquipmentService
from config import query_yaml


class ReserveService():
    def get_today_record():
        now_datetime = now()
        now_date = datetime.date(
            now_datetime.year, now_datetime.month, now_datetime.day)
        record_list = Reserve_Record.query.filter(
            Reserve_Record.reserveDate == now_date).all()
        return record_list

    def get_history_record(start_date_raw, end_date_raw, num):
        query_condition = and_()
        if start_date_raw:
            start_date = strToDate(start_date_raw)
            query_condition = and_(
                query_condition, Reserve_Record.reserveDate >= start_date)
        if end_date_raw:
            end_date = strToDate(end_date_raw)
            query_condition = and_(
                query_condition, Reserve_Record.reserveDate <= end_date)
        record_list = Reserve_Record.query.filter(query_condition).order_by(
            Reserve_Record.recordID.desc()).limit(num).all()
        return record_list

    def update_all_record_status():
        current_app.lock.acquire()
        now_datetime = now()
        now_date = datetime.date(
            now_datetime.year, now_datetime.month, now_datetime.day)
        now_time = datetime.time(now_datetime.hour, now_datetime.minute)
        records_to_update = Reserve_Record.query.filter(
            Reserve_Record.reserveDate <= now_date).all()
        valid_time = query_yaml("app.VALIDTIME")
        notice_time = query_yaml('app.NOTICETIME')
        for record in records_to_update:
            record_startTime = datetime.datetime.combine(
                record.reserveDate, record.startTime)
            if record_startTime + datetime.timedelta(minutes=valid_time) < now_datetime and record.status == "成功":
                try:
                    record.status = "违约"
                    db.session.commit()
                except:
                    db.session.rollback()
            elif (now_datetime + datetime.timedelta(minutes=notice_time) >= record_startTime and record.status == "成功" and
                  (not record.noticed)):
                token, getStatus = WechatService.getAccessToken()
                if getStatus:
                    messageContent = ReserveService.compute_notice_message(
                        record)
                    WechatService.sendMessage(
                        content=messageContent, token=token)
                record.noticed = True
                db.session.commit()
        current_app.lock.release()

    def compute_notice_message(record):
        messageContent = {}
        messageContent_data = {}
        messageContent["touser"] = record.userID
        messageContent["template_id"] = query_yaml('app.TEMPLATEID')
        messageContent_data["name1"] = {
            "value": UserService.get_name_by_id(record.userID)}
        messageContent_data["time22"] = {"value": str(
            record.reserveDate) + ' ' + record.startTime.strftime("%H:%M")}
        messageContent_data["time23"] = {"value": str(
            record.reserveDate) + ' ' + record.endTime.strftime("%H:%M")}
        messageContent_data["thing8"] = {"value": "签到提醒: " + EquipmentService.get_name_by_type(
            record.equipmentType)[0] + str(record.equipmentID) + '号'}
        messageContent_data["thing7"] = {"value": "请前往活动室签到"}
        messageContent["data"] = messageContent_data
        return messageContent
