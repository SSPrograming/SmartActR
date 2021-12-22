from flask import  jsonify, Blueprint, g, request
from application.services import InstructionService
from .login_decorator import login_required
import markdown
bp_instruction = Blueprint(
    'instruction',
    __name__
)


@bp_instruction.route('/api/v1/instruction/getSingleInstruction', methods=['POST'])
@login_required 
def get_single_instruction_info():
    try: 
        instructionID = request.json["instructionID"]
    except:
        return jsonify({"errCode": 1, "errMsg": "bad arguments"}), 200
    content = InstructionService.get_instruction_content(instructionID)
    return jsonify({
        "errCode": 0,
        "instructionContent" : markdown.markdown(content)
    }), 200 

@bp_instruction.route('/api/v1/instruction/getInstructionList', methods=['GET'])
@login_required
def get_all_instruction_info():
    instructionList = InstructionService.get_all_instrucion()
    return jsonify({
        "errCode": 0,
        "instructionList":instructionList
    }), 200

@bp_instruction.route('/api/v1/instruction/getTagList', methods=['GET'])
@login_required
def get_TagList():
    tagList = InstructionService.getTagList()
    return jsonify({
        "errCode":0,
        "errMsg":"",
        "tagList":tagList
    }), 200
