from application.database import db
from flask_sqlalchemy import SQLAlchemy

class User(db.Model):
    """
    用户表
    """
    __tablename__ = 'user'
    userID = db.Column(db.String(128), primary_key=True,
                        doc="openid")
    status = db.Column(db.String(32), doc="用户状态")
    violationTimes = db.Column(db.Integer, doc="违约次数")
    freezeDate = db.Column(db.Date, doc= "开始冻结日期")
    identity = db.Column(db.String(32), doc="身份")


class Equipment(db.Model):
    __tablename__ = 'equipment'
    equipmentType = db.Column(db.Integer, primary_key=True,
                              doc="设备种类")
    equipmentID = db.Column(db.Integer, primary_key=True,
                            doc="设备号")
    equipmentStatus = db.Column(db.String(32),
                                doc="设备状态,是否损坏等,默认为fine")

class Reserve_Record(db.Model):
    """
    预约记录
    """
    __tablename__ = 'reserve_record'
    recordID = db.Column(db.BigInteger, primary_key=True,
                         autoincrement=True, doc="记录ID")
    postTime = db.Column(db.DateTime, doc="下单时间")
    reserveDate = db.Column(db.Date, doc="预约日期")
    startTime = db.Column(db.Time, doc="开始时间")
    endTime = db.Column(db.Time, doc="结束时间")
    status = db.Column(db.String(32), doc="该次预约状态")
    userID = db.Column(db.String(128), db.ForeignKey('user.userID'),
                       doc="openid", nullable=False)
    equipmentType = db.Column(db.Integer,
                                doc="设备种类", nullable=False)                      
    equipmentID = db.Column(db.Integer,
                            doc="设备号",nullable=False)
    __table_args__ = (
        db.ForeignKeyConstraint(
            [equipmentType, equipmentID],
            [Equipment.equipmentType, Equipment.equipmentID]
        ),
    )
