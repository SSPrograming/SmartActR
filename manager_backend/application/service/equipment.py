from application.database import db
from application.models import Equipment, equipmentType, QRCode
from application.utils import strToTime, strToDate, now
import datetime

class EquipmentService():
    def get_name_by_type(Type):
        target_type = equipmentType.query.filter(equipmentType.equipmentType==Type).first()
        if target_type is None:
            return "未定义设备类型", False
        return target_type.equipmentName, True
    
    def get_all_equipmentType():
        return equipmentType.query.all()

    def get_type_count(Type):
        return Equipment.query.filter(Equipment.equipmentType==Type).count()
    
    def update_hashcode(Type, id, hashcode):
        target_equipment = Equipment.query.filter(Equipment.equipmentType==Type,
                                                  Equipment.equipmentID==id).first()
        if target_equipment is None:
            return "equipment not found", False
        target_qrcode_entry = QRCode.query.filter(QRCode.equipmentType==Type,
                                                  QRCode.equipmentID==id)
        if target_qrcode_entry is None:
            new_qrcode_entry = QRCode()
            new_qrcode_entry.equipmentID = id
            new_qrcode_entry.equipmentType = Type
            new_qrcode_entry.hashCode = hashcode
            try:
                db.session.add(new_qrcode_entry)
                db.session.commit()
                return 'ok', True
            except:
                db.session.rollback()
                return '数据库更新失败', False
        else:
            target_qrcode_entry.hashCode = hashcode
            try:
                db.session.commit()
                return 'ok', True
            except:
                return '数据库更新失败', False