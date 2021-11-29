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
    def test(hash):
        current = datetime.datetime.now()
        current_date = datetime.date(int(current.year),int(current.month),int(current.day))
        current_time = datetime.time(int(current.hour),int(current.minute),int(current.second))
        current_time_A = datetime.datetime.combine(datetime.date.today(), current_time)
        print("current_date:",current_date)
        print("current_time:",current_time)
        record =  QRCode.query.filter(QRCode.hashCode == hash).all()
        if len(record) == 0:
            return 0
        else:
            equipment_type = record[0].equipmentType
            id = record[0].equipmentID
            #今天这台设备的预约记录
            update_reserve_record_list = Reserve_Record.query.filter(Reserve_Record.equipmentID==id,Reserve_Record.equipmentType==equipment_type,Reserve_Record.reserveDate==current_date).all()
            for equipment in update_reserve_record_list:
                starttime_A = datetime.datetime.combine(datetime.date.today(), equipment.startTime)
                print("startTime:",equipment.startTime)
                diff_A = current_time_A - starttime_A
                diff = diff_A.total_seconds() / 60   #以分钟位时间间隔单位
                print("diff:",diff)
                if diff <= 20 and diff >= -20:
                    equipment.status = 1
                    db.session.commit()
                    break
            return 1