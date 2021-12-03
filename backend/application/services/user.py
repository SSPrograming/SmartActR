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
            print(e)
            db.session.rollback()
            return e, False
    
    def get_user(self, userID):
        try:
            u = User.query.filter(User.userID==userID).first()
            if u is None:
                return u, False
            else:
                return u, True
        except Exception as e:
            print(e)
            return e, False
    
    def get_user_status(self, userID):
        try:
            u = User.query.filter(User.userID==userID).first()
            if u is None:
                return "用户不存在", False
            else:
                return u.status, True
        except Exception as e:
            print(e)
            return e, False
    
    def get_stuInfo(self, userID):
        try:
            u = Student.query.filter(Student.userID==userID).first()
            if u is None:
                return "用户不存在", False
            else:
                return {"stuID": u.stuID, "department": u.department}, True
        except Exception as e:
            print(e)
            return e, False

    def get_student(self, userID):
        try:
            u = Student.query.filter(Student.userID==userID).first()
            if u is None:
                return u, False
            else:
                return u, True
        except Exception as e:
            print(e)
            return e, False
    
    def bind_user(self, userID, stuInfo):
        # TODO:失败时回滚
        try:
            msg, bindStatus = self.update_user_status(self, userID, '已绑定')
            self.update_user_identity(self, userID, 'student')
            stuID = stuInfo['stuID']
            stuName = stuInfo['stuName']
            stuDepartment = stuInfo['stuDepartment']
            stuCell = stuInfo['stuCell']
            stuMail = stuInfo['stuMail']
            stu = Student(stuID=stuID, userID=userID, name=stuName,
                          department=stuDepartment, cell=stuCell, email=stuMail)
            db.session.add(stu)
            db.session.commit()
            if not bindStatus:
                print(msg)
                return msg, False
            else:
                return 'ok', True
        except KeyError:
            return '参数错误', False
        except Exception as e:
            print(e)
            db.session.rollback()
            return e, False

    def update_user_status(self, userID, newStatus):
        statuses = ['已绑定', '未绑定', '冻结']
        if newStatus not in statuses:
            return "未定义的状态", False
        user, isExist = self.get_user(self, userID)
        if not isExist:
            return "该用户不存在", False
        try:
            user.status = newStatus
            db.session.commit()
            return 'ok', True
        except Exception as e:
            print(e)
            db.session.rollback()
            return e, False

    def update_user_identity(self, userID, newIdentity):
        identities = ['student', 'teacher', 'tourist']
        if newIdentity not in identities:
            return "未定义的身份", False
        user, isExist = self.get_user(self, userID)
        if not isExist:
            return "该用户不存在", False
        try:
            user.identity = newIdentity
            db.session.commit()
            return 'ok', True
        except Exception as e:
            print(e)
            db.session.rollback()
            return e, False

    def drop_single_student(self, userID):
        stu, exist = self.get_student(self, userID)
        if not exist:
            return "该学生不存在", False
        try:
            db.session.delete(stu)
            db.session.commit()
            return 'ok', True
        except Exception as e:
            db.session.rollback()
            return e, False