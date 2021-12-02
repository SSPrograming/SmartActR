from application.database import db
from application.models import Equipment, equipmentType, TableNotcie, QRCode, Reserve_Record
import datetime

class CheckInService:
    # def get_record(hash,currentTime):
        #return TableNotcie.query.filter(TableNotcie.noticeID==TableNotcie.query.count()).all()
        # equipment_list = QRCode.query.filter(QRCode.hashCode == hash)
        # if len(equipment_list) == 0:
        #     return 
        # else:
        # return 0
        #return TableNotcie.query.filter(TableNotcie.noticeID==100).all()
        #return TableNotcie.query.all()
    def test(hash,user_id):
        current = datetime.datetime.now()
        current_date = datetime.date(int(current.year),int(current.month),int(current.day))
        current_time = datetime.time(int(current.hour),int(current.minute),int(current.second))
        current_time_A = datetime.datetime.combine(datetime.date.today(), current_time)
        print("current_date:",current_date)
        print("current_time:",current_time)
        record =  QRCode.query.filter(QRCode.hashCode == hash).first()
        if len(record) == 0:
            return 1  #签到码过期
        else:  #qrcode有效的情况
            flag = 0 #用来判定在码有效情况下是否签到成功
            equipment_type = record[0].equipmentType
            id = record[0].equipmentID
            #今天这台设备的预约记录
            update_reserve_record_list = Reserve_Record.query.filter(Reserve_Record.userID == user_id,Reserve_Record.equipmentID==id,Reserve_Record.equipmentType==equipment_type,Reserve_Record.reserveDate==current_date).all()
            for equipment in update_reserve_record_list:
                starttime_A = datetime.datetime.combine(datetime.date.today(), equipment.startTime)
                print("startTime:",equipment.startTime)
                diff_A = current_time_A - starttime_A
                diff = diff_A.total_seconds() / 60   #以分钟位时间间隔单位
                print("diff:",diff)
                if diff <= 20 and diff >= -20:
                    flag+=1
                    equipment.status = 1
                    db.session.commit()
            if flag==0 is True:
                return 2 #码有效，但是签到失败（未预约或者已经逾期违约）
            else:
                return 0 #签到成功
            