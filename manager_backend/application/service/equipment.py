from application.database import db
from application.models import Equipment, equipmentType, QRCode
from application.utils import strToTime, strToDate, now
import datetime

from config import query_yaml

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
    
    def update_hashcode(Type, id, hashcode, qrcodeURL):
        target_equipment = Equipment.query.filter(Equipment.equipmentType==Type,
                                                  Equipment.equipmentID==id).first()
        if target_equipment is None:
            return "equipment not found", False
        target_qrcode_entry = QRCode.query.filter(QRCode.equipmentType==Type,
                                                  QRCode.equipmentID==id).first()
        if target_qrcode_entry is None:
            new_qrcode_entry = QRCode()
            new_qrcode_entry.equipmentID = id
            new_qrcode_entry.equipmentType = Type
            new_qrcode_entry.hashCode = hashcode
            new_qrcode_entry.QRCodeURL = qrcodeURL
            try:
                db.session.add(new_qrcode_entry)
                db.session.commit()
                return 'ok', True
            except:
                db.session.rollback()
                return '数据库更新失败', False
        else:
            target_qrcode_entry.hashCode = hashcode
            target_qrcode_entry.QRCodeURL = qrcodeURL
            try:
                db.session.commit()
                return 'ok', True
            except:
                return '数据库更新失败', False
    
    
    def get_qrcodeURL(Type, id):
        target_qrcode_entry = QRCode.query.filter(QRCode.equipmentType==Type,
                                                  QRCode.equipmentID==id).first()
        if target_qrcode_entry is None:
            return "二维码不存在", False
        if target_qrcode_entry.QRCodeURL is None:
            return "二维码不存在", False
        return target_qrcode_entry.QRCodeURL, True
        
    def add_equipmentType(self, equipmentName, Count, Description, img_name):
        new_equipmentType = equipmentType()
        new_equipmentType.equipmentDescription = Description
        new_equipmentType.equipmentName = equipmentName

        try:
            db.session.add(new_equipmentType)
            db.session.commit()
        except:
            db.session.rollback()
            return "新建设备种类失败", False
        """
        获取最新生成的设备种类序号
        """
        target_equipmentType = equipmentType.query.order_by(equipmentType.equipmentType.desc()).first().equipmentType
        new_equipmentType.equipmentImageURL = query_yaml("app.MANAGERSERVERURL") + "image/equipment/"+ str(target_equipmentType) + "_" +img_name
        try:
            db.session.commit()
        except:
            db.session.rollback()
            return "添加设备失败",False
        """
        添加对应数量的设备
        """
        for i in range(Count):
            addstatus = self.add_equipment(target_equipmentType)
            if not addstatus:
                return "添加设备失败", False
        return str(target_equipmentType), True


    def add_equipment(Type):
        new_equipment = Equipment()
        new_equipment.equipmentType = Type
        new_equipment.equipmentStatus = 'fine'
        try:
            db.session.add(new_equipment)
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False
    
    def update_equipmentType(Type, new_name, new_description, new_imgname):
        target_type = equipmentType.query.filter(equipmentType.equipmentType==Type).first()
        if target_type is None:
            return "设备种类不存在", False
        if new_name is not None:
            target_type.equipmentName = new_name
        if new_description is not None:
            target_type.equipmentDescription = new_description
        if new_imgname is not None:
            new_img_url = query_yaml("app.MANAGERSERVERURL") + "image/equipment/"+ str(Type) + "_" + new_imgname
            target_type.equipmentImageURL = new_img_url
        
        try:
            db.session.commit()
            return "ok", True
        except:
            db.session.rollback()
            return "更新设备种类失败", False
    
    def get_equipmentList(Type):
        target_type = equipmentType.query.filter(equipmentType.equipmentType==Type).first()
        if target_type is None:
            return "设备种类不存在", False
        return Equipment.query.filter(Equipment.equipmentType==Type).all(), True