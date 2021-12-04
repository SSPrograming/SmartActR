from application.database import db
from application.models import  QRCode, Reserve_Record
from application.utils import now
import datetime

class CheckInService:
    def test(hash,user_id):
        current = now()
        current_date = datetime.date(current.year,current.month,current.day)
        current_time = datetime.time(current.hour,current.minute,current.second)
        current_time_A = datetime.datetime.combine(datetime.date.today(), current_time)
        record =  QRCode.query.filter(QRCode.hashCode == hash).first()
        if record is None:
            return 1  #签到码过期
        else:  #qrcode有效的情况
            flag = False #用来判定在码有效情况下是否签到成功
            equipment_type = record.equipmentType
            id = record.equipmentID
            #今天这台设备的预约记录
            update_reserve_record_list = Reserve_Record.query.filter(Reserve_Record.userID==user_id,
                                                                    Reserve_Record.equipmentID==id,
                                                                    Reserve_Record.equipmentType==equipment_type,
                                                                    Reserve_Record.reserveDate==current_date).all()
            for equipment in update_reserve_record_list:
                starttime_A = datetime.datetime.combine(datetime.date.today(), equipment.startTime)
                diff_A = current_time_A - starttime_A
                diff = diff_A.total_seconds() / 60   #以分钟位时间间隔单位
                print("diff:",diff)
                if diff <= 20 and diff >= -20:
                    flag = True
                    equipment.status = "完成"
                    db.session.commit()
            if not flag:
                return 2 #码有效，但是签到失败（未预约或者已经逾期违约）
            else:
                return 0 #签到成功
            