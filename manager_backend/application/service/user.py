from sqlalchemy.sql.functions import user
from application.database import db
from application.models import User, Student
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