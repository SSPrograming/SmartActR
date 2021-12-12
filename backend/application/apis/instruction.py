from flask import  jsonify, Blueprint, g, request
from application.services import InstructionService
from .login_decorator import login_required

bp_instruction = Blueprint(
    'instruction',
    __name__
)


@bp_instruction.route('/api/v1/instruction/getSingleInstruction', methods=['POST'])
# @login_required 
def get_single_instruction_info():
   # id = request.json['instructionID']
   #content = InstructionService.get_instruction(id)
    content = InstructionService.get_instruction(1)  # for test
    return jsonify({
        "instructionContent" : content
    }) 

@bp_instruction.route('/api/v1/instruction/getInstructionList', methods=['GET'])
#@login_required
def get_all_instruction_info():
    instructionList = InstructionService.get_all_instrucion()
    return jsonify({
        "instructionList":instructionList
    })