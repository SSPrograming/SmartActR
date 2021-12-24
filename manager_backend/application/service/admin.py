from application.database import db
from application.models import Admin
from application.utils import encrypt_password
from config import query_yaml
import datetime
import hashlib


class AdminService():
    def get_admin(username, pswd):
        pswd = encrypt_password(pswd)
        admin_user = Admin.query.filter(
            Admin.userName == username, Admin.password == pswd).first()
        return admin_user

    def create_admin():
        adminName = query_yaml('app.ADMINNAME')
        adminPass = query_yaml('app.ADMINPASS')
        frontend_salt = query_yaml('app.FRONTENDSALT')
        hashFunc = hashlib.md5()
        raw_code = adminName + adminPass + frontend_salt
        print(raw_code)
        hashFunc.update(raw_code.encode('utf-8'))
        frontend_code = hashFunc.hexdigest()

        print(frontend_code)
        administrator = Admin.query.filter(Admin.userName == adminName).first()
        if administrator is None:
            new_admin = Admin()
            new_admin.userName = adminName
            new_admin.password = encrypt_password(frontend_code)
            try:
                db.session.add(new_admin)
                db.session.commit()
            except:
                db.session.rollback()
                raise Exception("管理员账户初始化失败")
        else:
            administrator.password = encrypt_password(frontend_code)
            try:
                db.session.commit()
            except:
                db.session.rollback()
                raise Exception("管理员账户初始化失败")
