from application.database import db
from application.models import User, Student
from application.utils import strToTime, strToDate, now
import datetime

class UserService():
    def get_name_by_id(userid):
        target_user = Student.query.filter(Student.userID==userid).first()
        if target_user is None:
            return "未绑定用户"
        else:
            return target_user.name