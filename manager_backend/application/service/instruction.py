from application.database import db
from application.models import Equipment, equipmentType, QRCode, Reserve_Record, Instruction, InstructionImage, InstructionTag
from application.utils import strToTime, strToDate, now
import datetime
import os
from config import query_yaml


class InstructionService():
    def addImage(imageName, instructionID):
        targetInstrucion = Instruction.query.filter(
            Instruction.instructionID == instructionID).first()
        if targetInstrucion is None:
            return "找不到这篇使用说明", False

        now_timestamp = str(int(now().timestamp()))

        unique_imageName = str(instructionID) + "_" + now_timestamp + imageName
        image_url = query_yaml("app.MANAGERSERVERURL") + \
            "image/instruction/"+unique_imageName
        new_instructionImage = InstructionImage()
        new_instructionImage.instructionID = instructionID
        new_instructionImage.imageURL = image_url
        try:
            db.session.add(new_instructionImage)
            db.session.commit()
            return [image_url, unique_imageName, new_instructionImage.instructionImageID], True
        except:
            db.session.rollback()
            return "插入数据库时失败，可能是图片名过长", False

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

        new_instruction = Instruction.query.order_by(
            Instruction.instructionID.desc()).first()

        instructionCoverURL = query_yaml("app.MANAGERSERVERURL") + "image/instructioncover/" + str(
            new_instruction.instructionID) + "_" + instructionCoverName

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

    def updateInstruction(instructionID, instructionName, instructionTags, instructionCoverName):
        targetInstruction = Instruction.query.filter(
            Instruction.instructionID == instructionID).first()
        if targetInstruction is None:
            return "此说明不存在", False
        if instructionCoverName is not None:
            old_cover_url = targetInstruction.instructionCoverURL
            old_img_name = old_cover_url.split('/')[-1]
            if os.path.exists("/code/application/static/instructioncover/"+old_img_name):
                os.remove(
                    "/code/application/static/instructioncover/"+old_img_name)
            new_img_url = query_yaml("app.MANAGERSERVERURL") + 'image/instructioncover/' + str(
                instructionID) + '_' + instructionCoverName
            targetInstruction.instructionCoverURL = new_img_url
        targetInstruction.instructionName = instructionName
        try:
            db.session.commit()
        except:
            db.session.rollback()
            return "更新说明失败", False
        exist_Tags = InstructionTag.query.filter(
            InstructionTag.instructionID == instructionID).all()
        exist_Tag_Names = [x.tagName for x in exist_Tags]
        """
        删除不再出现的tag
        """
        for tag in exist_Tags:
            if tag.tagName not in instructionTags:
                try:
                    db.session.delete(tag)
                    db.session.commit()
                except:
                    db.session.rollback()
                    return "更新tag时出错", False

        """
        增加新的tag
        """
        for tag in instructionTags:
            if tag not in exist_Tag_Names:
                try:
                    new_tag = InstructionTag()
                    new_tag.instructionID = instructionID
                    new_tag.tagName = tag
                    db.session.add(new_tag)
                    db.session.commit()
                except:
                    db.session.rollback()
                    return "更新tag时出错", False

        return "ok", True

    def updateInstructionContent(instructionID, instructionContent):
        targetInstruction = Instruction.query.filter(
            Instruction.instructionID == instructionID).first()
        if targetInstruction is None:
            return "此说明不存在", False
        targetInstruction.instructionContent = instructionContent
        try:
            db.session.commit()
            return "ok", True
        except:
            return "更新内容失败", False

    def getSingleInstruction(instructionID):
        targetInstruction = Instruction.query.filter(
            Instruction.instructionID == instructionID).first()
        if targetInstruction is None:
            return "此说明不存在", False
        return targetInstruction.instructionContent, True

    def getInstructionList():
        return Instruction.query.all()

    def getInstructionTags(instructionID):
        instructionTags = InstructionTag.query.filter(
            InstructionTag.instructionID == instructionID).all()
        return [item.tagName for item in instructionTags]

    def deleteInstruction(instructionID):
        targetInstruction = Instruction.query.filter(
            Instruction.instructionID == instructionID).first()
        if targetInstruction is None:
            return "此说明不存在", False
        try:
            InstructionTag.query.filter(
                InstructionTag.instructionID == instructionID).delete()
            db.session.commit()
        except:
            db.session.rollback()
            return "删除使用说明失败", False

        try:
            InstructionImage.query.filter(
                InstructionImage.instructionID == instructionID).delete()
            db.session.commit()
        except:
            db.session.rollback()
            return "删除使用说明失败", False
        try:
            db.session.delete(targetInstruction)
            db.session.commit()
            return "ok", True
        except:
            db.session.rollback()
            return "删除使用说明失败", False

    def getSingleInstructionImageList(instructionID):
        ImageList = InstructionImage.query.filter(
            InstructionImage.instructionID == instructionID).all()
        return ImageList

    def deleteImage(instructionID, instructionImageID):
        target_entry = InstructionImage.query.filter(InstructionImage.instructionID == instructionID,
                                                     InstructionImage.instructionImageID == instructionImageID).first()
        if target_entry is None:
            return "找不到这张图片的记录", False
        targetImageURL = target_entry.imageURL
        targetImageName = targetImageURL.split('/')[-1]
        if os.path.exists('./application/static/instruction/'+targetImageName):
            os.remove('./application/static/instruction/'+targetImageName)
        try:
            db.session.delete(target_entry)
            db.session.commit()
            return "ok", True
        except:
            db.session.rollback()
            return "删除图片失败", False
