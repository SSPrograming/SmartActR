from application.database import db
from application.models import Reserve_Record, ruleTable
import datetime
from application.utils import now

class ReserveService:
    def get_record_of_single_equipment(date, equipmentType, equipmentID):
        """
        返回特定日期，特定设备的所有预约记录
        """
        records = Reserve_Record.query.filter(Reserve_Record.reserveDate==date,
                                              Reserve_Record.equipmentType==equipmentType,
                                              Reserve_Record.equipmentID==equipmentID).all()
        return records
        
    def get_occupation_of_day(date):
        """
        返回一个占用时间段和标志位，标志这一天是否有占用
        占用时间段可能有多个，以[{"startTime":Time, "endTime": Time}]形式返回
        """
        valid_occupations = ruleTable.query.filter(ruleTable.expireDate>=date).all()
        occupied_time = []
        occupy_flag = False
        weekday = date.isoweekday()
        for valid_occupation in valid_occupations:
            if valid_occupation.repeat==True:   #重复占用规则
                if valid_occupation.day==weekday:
                    occupied_time.append({"startTime": valid_occupation.startTime,
                                          "endTime": valid_occupation.endTime})
                    occupy_flag = True
            else:   #非重复占用规则
                if valid_occupation.date==date:
                    occupied_time.append({"startTime": valid_occupation.startTime,
                                          "endTime": valid_occupation.endTime})
                    occupy_flag = True
        return occupied_time, occupy_flag
    
    def add_reserve_record(userID, reserveDate, startTime, endTime, equipmentType, equipmentID):
        nrecord = Reserve_Record(userID=userID, postTime=now(),reserveDate=reserveDate, startTime=startTime,
                                endTime=endTime, equipmentType=equipmentType, equipmentID=equipmentID,
                                status="成功")
        try:
            db.session.add(nrecord)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            db.session.rollback()
            return False


    def delete_reserve_record(userID, recordID, strict=True):
        """
        当strict==True时
        无法删除当前时间之前的预约
        """
        query_reserve_record = Reserve_Record.query.filter(Reserve_Record.userID==userID,
                                                            Reserve_Record.recordID==recordID).first()
        if query_reserve_record==None:
            return '无匹配记录',False
        if strict:
            now = datetime.datetime.now()
            reserveDate = query_reserve_record.reserveDate
            startTime = query_reserve_record.startTime
            target_startTime = datetime.datetime(reserveDate.year, reserveDate.month, reserveDate.day,
                                                startTime.hour, startTime.minute, startTime.second)
            if target_startTime<=now:
                return '超时，不可取消',False
        try:
            query_reserve_record.status = 'cancel'
            db.session.commit()
            return 'ok',True
        except Exception as e:
            print('删除预约记录时出错:',e)
            db.session.rollback()
            return '数据库错误',False

    def get_history_record(userID):
        query_record = Reserve_Record.query.filter(Reserve_Record.userID==userID).order_by(Reserve_Record.reserveDate.asc()).all()
        rem_start = len(query_record)
        now = datetime.datetime.now()
        today = datetime.date(now.year, now.month, now.day)
        for i in range(len(query_record)-1, -1, -1):
            if query_record[i].reserveDate >= today:
                rem_start = i
            else:
                break
        if rem_start < len(query_record):
            del query_record[rem_start:]
        
        return query_record     

    def get_current_record(userID):
        query_record = Reserve_Record.query.filter(Reserve_Record.userID==userID).order_by(Reserve_Record.reserveDate.asc()).all()
        rem_start = len(query_record)
        now = datetime.datetime.now()
        today = datetime.date(now.year, now.month, now.day)
        for i in range(len(query_record)-1, -1, -1):
            if query_record[i].reserveDate >= today:
                rem_start = i
            else:
                break
        if rem_start < len(query_record):
            del query_record[:rem_start]
        return query_record     

    def strToTime(strTime):
        """
        输入必须为 'hh:mm'的形式
        """
        timeStruct = datetime.datetime.strptime(strTime, '%H:%M').timetuple()
        return datetime.time(timeStruct[3], timeStruct[4])