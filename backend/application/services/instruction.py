from application.database import db
from application.models import InstructionImage,InstructionTag,Instruction
import datetime
from application.utils import now

class InstructionService:
    def get_instruction_content(instructionID):
        ins = Instruction.query.filter(Instruction.instructionID == instructionID).first()
        return ins.instructionContent
    
    def get_all_instrucion():
        instructionList = []
        instructionObject_list = Instruction.query.all()
        for i in instructionObject_list:
            instruction_to_add = {}
            instruction_to_add['instructionID'] = i.instructionID
            instruction_to_add["instructionName"] = i.instructionName
            instruction_to_add["instructionTags"] = []
            TagList = InstructionTag.query.filter(InstructionTag.instructionID == i.instructionID).all()
            for tag in TagList:
                instruction_to_add["instructionTags"].append(tag.tagName)
            instruction_to_add["instructionCoverURL"] = i.instructionCoverURL
            instructionList.append(instruction_to_add)
        return instructionList

    def getTagList():
        taglist_raw = InstructionTag.query.with_entities(InstructionTag.tagName).filter().all()
        tagset = set([item.tagName for item in taglist_raw])
        taglist = [tag for tag in tagset]
        return taglist
