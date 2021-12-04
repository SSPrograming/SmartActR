from application.database import db
from application.models import Equipment, equipmentType
import datetime

class EquipmentService:
    def get_all_equipmentType():
        """
        ret a list of equipmenType class
        """
        return equipmentType.query.all()

    def get_all_equipment():
        return Equipment.query.all()

    def get_single_equipmentType(equipmentTypeID):
        """
        ret None if the ID does not exist
        """
        return equipmentType.query.filter(equipmentType.equipmentType==equipmentTypeID).first()

    def get_single_equipment(equipmentTypeID, equipmentID):
        """
        ret None if the equipment does not exist
        """
        return Equipment.query.filter(Equipment.equipmentType==equipmentTypeID,
                                      Equipment.equipmentID==equipmentID).first()
    
    def insert_single_equipmentType(equipmentName, equipmentDescription):
        """
        插入单种设备
        """
        existedName = equipmentType.query.filter(equipmentType.equipmentName==equipmentName).first()
        if existedName is None: # 确保不会重名造成歧义
            newType = equipmentType(equipmentName=equipmentName,
                                    equipmentDescription=equipmentDescription)
            try:
                db.session.add(newType)
                db.session.commit()
                return True
            except Exception as e:
                print(e)
                db.session.rollback()
                return False
        else:
            return False

    def insert_single_equipment(equipmentTypeID, equipmentID):
        """
        插入单台设备
        """
        newEquipment = Equipment(equipmentType=equipmentTypeID,equipmentID=equipmentID,
                                equipmentStatus='fine')
        try:
            db.session.add(newEquipment)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            db.session.rollback()
            return False