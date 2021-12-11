from flask import  jsonify, Blueprint, g, request
from application.services import InstructionService
from .login_decorator import login_required

bp_instruction = Blueprint(
    'instruction',
    __name__
)


@bp_instruction.route('/api/v1/instruction/getSingleInstruction', methods=['POST'])
# @login_required 
def get_instruction_info():
   # id = request.json['instructionID']
    content = InstructionService.get_instruction(1)
    return jsonify({
        "instructionContent" : content
    }) 
