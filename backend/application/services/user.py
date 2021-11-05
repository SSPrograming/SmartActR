from application.database import db
from application.models import User, Student
import datetime

class UserService():
    def create_user(self, userID, identity):
        try:
            frzTime = datetime.date(year=1970,month=1,day=1)
            nuser = User(userID=userID, status='not bind', violationTimes=0,
                        freezeDate=frzTime, identity=identity)
            db.session.add(nuser)
            db.session.commit()
            return 'ok', True
        except Exception as e:
            return e, False
    
    def get_user(self, userID):
        try:
            u = User.query.filter(User.userID==userID).first()
            if u is None:
                return u, False
            else:
                return u, True
        except Exception as e:
            return e, False
    
    def bind_user(self, userID, stuInfo):
        try:
            stuID = stuInfo['stuID']
            stuName = stuInfo['stuName']
            stuDepartment = stuInfo['stuDepartment']
            stuCell = stuInfo['stuCell']
            stuMail = stuInfo['stuMail']
            stu = Student(stuID=stuID, userID=userID, name=stuName,
                          department=stuDepartment, cell=stuCell, email=stuMail)
            db.session.add(stu)
            db.session.commit()
            return 'ok', True
        except KeyError:
            return '参数错误', False
        except Exception as e:
            return e, False
