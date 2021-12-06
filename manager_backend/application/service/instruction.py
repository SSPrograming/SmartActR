from yaml.tokens import TagToken
from application.database import db
from application.models import Equipment, equipmentType, QRCode, Reserve_Record, Instruction, InstructionImage, InstructionTag
from application.utils import strToTime, strToDate, now
import datetime

from config import query_yaml

class InstructionService():
    def addImage(imageName, instructionID):
        targetInstrucion = Instruction.query.filter(Instruction.instructionID==instructionID).first()
        if targetInstrucion is None:
            return "找不到这篇使用说明","", False
        
        now_timestamp = str(int(now().timestamp()))

        unique_imageName = str(instructionID) + "_" + now_timestamp + imageName
        image_url = query_yaml("app.MANAGERSERVERURL") + "image/instruction/"+unique_imageName
        new_instructionImage = InstructionImage()
        new_instructionImage.instructionID = instructionID
        new_instructionImage.imageURL = image_url
        try:
            db.session.add(new_instructionImage)
            return image_url, unique_imageName, True
        except:
            db.session.rollback()
            return "插入数据库时失败，可能是图片名过长","", False
        
    
    def addInstruction(instructionName, instructionTags, instructionCoverName):
        new_instruction = Instruction()
        new_instruction.instructionName = instructionName
        new_instruction.instructionContent = ""
        new_instruction.instructionCoverURL = ""
        try:
            db.session.add(new_instruction)
            db.session.commit()
        except:
            return "创建使用说明失败", False
        
        new_instruction = Instruction.query.order_by(Instruction.instructionID.desc()).first()

        instructionCoverURL = query_yaml("app.MANAGERSERVERURL") + "image/instructioncover/" + str(new_instruction.instructionID) + "_" + instructionCoverName
        
        new_instruction.instructionCoverURL = instructionCoverURL
        try:
            db.session.commit()
        except:
            db.session.rollback()
            return "为使用说明添加描述图片URL失败", False

        for tag in instructionTags:
            new_instruction_tag = InstructionTag()
            new_instruction_tag.instructionID = new_instruction.instructionID
            new_instruction_tag.tagName = tag
            try:
                db.session.add(new_instruction_tag)
                db.session.commit()
            except:
                return "为使用说明创建标签失败", False
        
        return instructionCoverURL, True