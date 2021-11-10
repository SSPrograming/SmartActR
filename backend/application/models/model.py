from application.database import db

class User(db.Model):
    """
    用户表
    """
    __tablename__ = 'user'
    userID = db.Column(db.String(128), primary_key=True,
                        doc="openid")
    status = db.Column(db.String(32), doc="用户状态")
    # not bind, binded, freeze
    violationTimes = db.Column(db.Integer, doc="违约次数")
    freezeDate = db.Column(db.Date, doc= "开始冻结日期")
    identity = db.Column(db.String(32), doc="身份")


class equipmentType(db.Model):
    """
    设备种类
    """
    __tablename__ = 'equipmentType'
    equipmentType = db.Column(db.Integer,primary_key=True,autoincrement=True)
    equipmentName = db.Column(db.String(256))
    equipmentDescription = db.Column(db.String(1024))

class Equipment(db.Model):
    __tablename__ = 'equipment'
    equipmentType = db.Column(db.Integer, db.ForeignKey('equipmentType.equipmentType'), primary_key=True,
                              doc="设备种类")
    equipmentID = db.Column(db.Integer, primary_key=True)
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
    # 复合外键约束
    __table_args__ = (
        db.ForeignKeyConstraint(
            [equipmentType, equipmentID],
            [Equipment.equipmentType, Equipment.equipmentID]
        ),
    )

class Student(db.Model):
    """
    学生表
    """
    __tablename__ = 'student'
    stuID = db.Column(db.String(16), primary_key=True)
    userID = db.Column(db.String(128), db.ForeignKey('user.userID'), nullable=False)
    name = db.Column(db.String(32), doc="学生姓名")
    department = db.Column(db.String(64), doc="院系名称")
    cell = db.Column(db.String(16))
    email = db.Column(db.String(32))

class OccupationInfo(db.Model):
    """
    占用规则表
    """
    __tablename__ = 'occupationinfo'
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    repeat = db.Column(db.Boolean, doc="是否为重复规则")
    day = db.Column(db.Integer, doc="如重复，是星期几")
    date = db.Column(db.Date, doc="如不重复，是哪一天")
    startTime = db.Column(db.Time, doc="开始时间")
    endTime = db.Column(db.Time, doc="结束时间")
    expireDate = db.Column(db.Date, doc="规则失效日期")

class TableNotcie(db.Model):
    """
    公告表
    """
    __tablename__ = 'tablenotice'
    noticeID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    noticeContent = db.Column(db.String(10000), doc="公告内容")
    noticeDate = db.Column(db.Date, doc="公告发布日期")
    expireDate = db.Column(db.Date, doc="公告失效日期")

class Instruction(db.Model):
    """
    使用说明
    """
    __tablename__ = 'instruction'
    instructionContent = db.Column(db.Text, doc="html格式说明内容")
    instructionTag = db.Column(db.String(256), doc="标签")
    instructionID = db.Column(db.Integer, autoincrement=True, primary_key=True, doc="ID")
    instructionName = db.Column(db.String(64), doc="说明标题")

