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

    def strToTime(strTime):
        timeStruct = datetime.datetime.strptime(strTime, '%H:%M').timetuple()
        return datetime.time(timeStruct[3], timeStruct[4])