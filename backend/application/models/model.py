from application.database import db

class User(db.Model):
    """
    用户表
    """
    __tablename__ = 'user'
    userID = db.Column(db.String(128), primary_key=True,
                        doc="openid")
    status = db.Column(db.String(32), doc="用户状态")
    stuID = db.Column(db.String(16), doc="学号")
