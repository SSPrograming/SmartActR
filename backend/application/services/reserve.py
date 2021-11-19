from application.database import db
from application.models import User, Student, Reserve_Record, Equipment, equipmentType, OccupationInfo
import datetime
import time

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
        valid_occupations = OccupationInfo.query.filter(OccupationInfo.expireDate>=date).all()
        occupied_time = []
        occupy_flag = False
        weekday = datetime.datetime.now().isoweekday()
        for valid_occupation in valid_occupations:
            if valid_occupation.repeat==True:   #重复占用规则
                if valid_occupation.day==weekday:
                    occupied_time.append({"startTime": valid_occupation.startTime,
                                          "endTime": valid_occupation.endTime})
                    occupy_flag = True
            else:   #非重复占用规则
                if valid_occupation.date==datetime.datetime.now():
                    occupied_time.append({"startTime": valid_occupation.startTime,
                                          "endTime": valid_occupation.endTime})
                    occupy_flag = True
        return occupied_time, occupy_flag
    
    def add_reserve_record(userID, reserveDate, startTime, endTime, equipmentType, equipmentID):
        nrecord = Reserve_Record(userID=userID, postTime=datetime.datetime.now(),reserveDate=reserveDate, startTime=startTime,
                                endTime=endTime, equipmentType=equipmentType, equipmentID=equipmentID,
                                status="fine")
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
        if strict:
            now = datetime.datetime.now()
            reserveDate = query_reserve_record.reserveDate
            startTime = query_reserve_record.startTime
            target_startTime = datetime.datetime(reserveDate.year, reserveDate.month, reserveDate.day,
                                                startTime.hour, startTime.minute, startTime.second)
            if target_startTime<=now:
                return '超时，不可取消',False
        if query_reserve_record==None:
            return '无匹配记录',False
        try:
            db.session.delete(query_reserve_record)
            db.session.commit()
            return 'ok',True
        except Exception as e:
            print('删除预约记录时出错:',e)
            db.session.rollback()
            return '数据库错误',False

    def strToTime(strTime):
        """
        输入必须为 'hh:mm'的形式
        """
        timeStruct = datetime.datetime.strptime(strTime, '%H:%M').timetuple()
        return datetime.time(timeStruct[3], timeStruct[4])