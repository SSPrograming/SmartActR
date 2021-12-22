from application.database import db
from application.models import Equipment, equipmentType, QRCode, Reserve_Record
from application.utils import strToTime, strToDate, now
import datetime
from sqlalchemy import and_
from config import query_yaml
import os

class EquipmentService():
    def get_name_by_type(Type):
        target_type = equipmentType.query.filter(equipmentType.equipmentType==Type).first()
        if target_type is None:
            return "未定义设备类型", False
        return target_type.equipmentName, True
    
    def get_all_equipmentType():
        return equipmentType.query.order_by(equipmentType.equipmentOrder.asc()).all()

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
        
    def add_equipmentType(equipmentName, Count, Description, img_name):
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
        new_equipmentType.equipmentOrder = target_equipmentType
        try:
            db.session.commit()
        except:
            db.session.rollback()
            return "添加设备失败",False
        """
        添加对应数量的设备
        """
        for i in range(Count):
            addstatus = EquipmentService.add_equipment(target_equipmentType, i+1)
            if not addstatus:
                return "添加设备失败", False
        return str(target_equipmentType), True


    def add_equipment(Type,id):
        new_equipment = Equipment()
        new_equipment.equipmentType = Type
        new_equipment.equipmentStatus = '完好'
        new_equipment.equipmentID = id
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
    
    def drop_related_record(Type):
        related_records = Reserve_Record.query.filter(Reserve_Record.equipmentType==Type).all()
        for record in related_records:
            try:
                db.session.delete(record)
                db.session.commit()
            except:
                db.session.rollback()
                return "删除相关预约记录失败", False
        return "ok", True
    
    def drop_related_qrCode(Type):
        related_records = QRCode.query.filter(QRCode.equipmentType==Type).all()
        for record in related_records:
            try:
                db.session.delete(record)
                db.session.commit()
            except:
                db.session.rollback()
                return "删除相关二维码记录失败", False
        return "ok", True

    def drop_single_qrCode(Type, id):
        related_record = QRCode.query.filter(QRCode.equipmentType==Type,
                                              QRCode.equipmentID==id).first()
        if related_record is not None:
            qrcode_name = related_record.QRCodeURL.split('/')[-1]
            if os.path.exists(query_yaml('app.QRCODEPATH')+ qrcode_name):
                os.remove(query_yaml('app.QRCODEPATH')+ qrcode_name)
            try:
                db.session.delete(related_record)
                db.session.commit()
            except:
                db.session.rollback()
                return "删除相关二维码记录失败", False
        return "ok", True

    def drop_related_equipment(Type):
        related_equipments = Equipment.query.filter(Equipment.equipmentType==Type).all()
        for equipment in related_equipments:
            try:
                db.session.delete(equipment)
                db.session.commit()
            except:
                db.session.rollback()
                return "删除相关设备记录失败", False
        return "ok", True
    
    def drop_type(Type):
        target_type = equipmentType.query.filter(equipmentType.equipmentType==Type).first()
        if target_type is None:
            return "设备种类不存在", False
        try:
            db.session.delete(target_type)
            db.session.commit()
        except:
            db.session.rollback()
            return "删除设备种类失败", False
        return "ok", True
    
    def update_equipment_status(Type, id, status):
        now_datetime = now()
        now_date = datetime.date(now_datetime.year, now_datetime.month, now_datetime.day)
        target_equipment = Equipment.query.filter(Equipment.equipmentType==Type,
                                                  Equipment.equipmentID==id).first()
        if target_equipment is None:
            return "设备不存在", False
        
        if status=='损坏':
            related_records = Reserve_Record.query.filter(Reserve_Record.equipmentType==Type,
                                                          Reserve_Record.equipmentID==id,
                                                          Reserve_Record.reserveDate>=now_date,
                                                          Reserve_Record.status=='成功').all()
            for record in related_records:
                record.status='取消'
                try:
                    db.session.commit()
                except:
                    db.session.rollback()
                    return "数据库更新失败", False

        try:
            target_equipment.equipmentStatus = status
            db.session.commit()
            return "ok", True
        except:
            db.session.rollback()
            return "更新设备状态失败",False
    
    def get_largest_id(Type):
        target_type = equipmentType.query.filter(equipmentType.equipmentType==Type).first()
        if target_type is None:
            return "设备种类不存在", False
        target_equipment = Equipment.query.filter(Equipment.equipmentType==Type).order_by(Equipment.equipmentID.desc()).first()
        if target_equipment is None:
            return 0, True
        else:
            return target_equipment.equipmentID, True
    
    def get_TypeImg_url(Type):
        target_type = equipmentType.query.filter(equipmentType.equipmentType==Type).first()
        if target_type is None:
            return "设备种类不存在", False
        return target_type.equipmentImageURL, True
    
    def get_equipment_recordList(equipmentType, equipmentID,startDate, endDate, num):
        query_condition = and_(Reserve_Record.equipmentType==equipmentType,Reserve_Record.equipmentID==equipmentID)
        if startDate is not None:
            try:
                startDate = strToDate(startDate)
            except:
                return "bad arguments", False
            query_condition = and_(query_condition, Reserve_Record.reserveDate>=startDate)
        
        if endDate is not None:
            try:
                endDate = strToDate(endDate)
            except:
                return "bad arguments", False
            query_condition = and_(query_condition, Reserve_Record.reserveDate<=endDate)

        recordList = Reserve_Record.query.filter(query_condition).order_by(Reserve_Record.recordID.desc()).limit(num).all()
        return recordList, True
    
    def swap_equipmentOrder(Type1, Type2):
        target_type1 = equipmentType.query.filter(equipmentType.equipmentType==Type1).first()
        target_type2 = equipmentType.query.filter(equipmentType.equipmentType==Type2).first()
        if target_type1 is None or target_type2 is None:
            return "设备种类不存在", False
        Type1_order = target_type1.equipmentOrder
        Type2_order = target_type2.equipmentOrder
        target_type1.equipmentOrder = 2147483647
        try:
            db.session.commit()
        except:
            db.session.rollback()
            return "交换次序失败", False
        target_type2.equipmentOrder = Type1_order
        try:
            db.session.commit()
        except:
            db.session.rollback()
            return "交换次序失败", False
        
        target_type1.equipmentOrder = Type2_order
        try:
            db.session.commit()
        except:
            db.session.rollback()
            return "交换次序失败", False
        
        return "ok", True

    def deleteEquipment(Type, id):
        targetEquipment = Equipment.query.filter(Equipment.equipmentType==Type,
                                                     Equipment.equipmentID==id).first()
        if targetEquipment is None:
            return "该设备不存在", False
        
        msg, drop_qrcode_status = EquipmentService.drop_single_qrCode(Type, id)
        if not drop_qrcode_status:
            return msg, False
        relatedRecords = Reserve_Record.query.filter(Reserve_Record.equipmentType==Type,
                                                     Reserve_Record.equipmentID==id).all()
        for record in relatedRecords:
            try:
                db.session.delete(record)
                db.session.commit()
            except:
                db.session.rollback()
                return "删除相关预约记录时出错", False
        
        try:
            db.session.delete(targetEquipment)
        except:
            db.session.rollback()
            return "删除设备失败", False
        db.session.commit()
        return "ok", True