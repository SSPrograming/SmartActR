from sqlalchemy.sql.functions import user
from application.database import db
from application.models import User, Student, Reserve_Record
from application.utils import strToTime, strToDate, now
from sqlalchemy import and_
import datetime
from config import query_yaml

class UserService():
    def get_name_by_id(userid):
        target_user = Student.query.filter(Student.userID==userid).first()
        if target_user is None:
            return "未绑定用户"
        else:
            return target_user.name
    
    def query_user_info(query_content):
        query_condition = and_()
        if query_content["stuID"] is not None:
            query_condition = and_(query_condition, Student.stuID==query_content["stuID"])
        if query_content["department"] is not None:
            query_condition = and_(query_condition, Student.department.like('%'+query_content["department"]+'%'))
        if query_content["stuName"] is not None:
            query_condition = and_(query_condition, Student.name.like('%'+query_content["stuName"]+'%'))
        
        if query_content["limitNum"] is None:
            stuList = Student.query.filter(query_condition).all()
        else:
            try:
                limitNum = int(query_content["limitNum"])
            except:
                return "bad arguments", False
            if limitNum<=0:
                return "bad arguments", False
            stuList = Student.query.filter(query_condition).limit(limitNum).all()
        stuInfoList = []
        for stu in stuList:
            userID = stu.userID
            userInfo = User.query.filter(User.userID==userID).first()
            stuInfoList.append({
                "userID": userID,
                "stuID": stu.stuID,
                "stuName": stu.name,
                "department": stu.department,
                "email": stu.email,
                "cellphone": stu.cell,
                "freezeStatus": userInfo.freezeStatus,
                "freezeDate": str(userInfo.freezeDate)
            })
        return stuInfoList, True
    

    def daily_update_userStatus():
        freezelen = query_yaml("app.FREEZELEN")
        now_datetime = now()
        now_date = datetime.date(now_datetime.year, now_datetime.month, now_datetime.day)
        userList = User.query.all()
        for user in userList:
            user.violateToday = 0
            if user.freezeStatus and now_date>=user.freezeDate+datetime.timedelta(days=freezelen):
                user.freezeStatus = 0
            db.session.commit()

    def update_studentStatus(stuID, status):
        target_student = Student.query.filter(Student.stuID==stuID).first()
        if target_student is None:
            return "找不到这名学生", False
        target_user = User.query.filter(User.userID==target_student.userID).first()
        now_datetime = now()
        now_date = datetime.date(now_datetime.year, now_datetime.month, now_datetime.day)
        if status==1:
            target_user.freezeStatus = 1
            target_user.freezeDate = now_date
        elif status==0:
            target_user.freezeStatus = 0
        else:
            return "bad arguments", False
        try:
            db.session.commit()
            return "ok", True
        except:
            db.session.rollback()
            return "数据库更新失败", False
    
    def get_user_recordList(stuID,startDate, endDate, num):
        target_student = Student.query.filter(Student.stuID==stuID).first()
        if target_student is None:
            return "找不到这名学生", False
        query_condition = and_(Reserve_Record.userID==target_student.userID)
        if startDate is not None:
            try:
                startDate = strToDate(startDate)
            except:
                return "bad arguments", False
            query_condition = and_(query_condition, Reserve_Record.reserveDate>=startDate)
        
        if endDate is not None:
            try:
                endDate = strToDate(endDate)
            except:
                return "bad arguments", False
            query_condition = and_(query_condition, Reserve_Record.reserveDate<=endDate)

        recordList = Reserve_Record.query.filter(query_condition).order_by(Reserve_Record.recordID.desc()).limit(num).all()
        return recordList, True
