from operator import or_
from application.database import db
from application.models import Instruction
import datetime
from sqlalchemy import or_
from application.utils import now

class InstructionService:
    def get_instruction(instructionID):
        ins = Instruction.query.filter(Instruction.instructionID == instructionID).first()
        return ins.instructionContent