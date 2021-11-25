from application.database import db
from application.models import Admin
from application.utils import encrypt_password
import datetime

class UserService():
    def get_admin(username, pswd):
        pswd = encrypt_password(pswd)
        admin_user = Admin.query.filter(Admin.userName==username, Admin.password==pswd).first()
        return admin_user