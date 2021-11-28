from application.database import db
from application.models import Equipment, equipmentType
from application.utils import strToTime, strToDate, now
import datetime

class EquipmentService():
    def get_name_by_type(Type):
        target_type = equipmentType.query.filter(equipmentType.equipmentType==Type).first()
        if target_type is None:
            return "未定义设备类型", False
        return target_type.equipmentName, True