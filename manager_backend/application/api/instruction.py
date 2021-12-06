from flask import json, request, jsonify, Blueprint, g
from sqlalchemy.sql.operators import exists
from config import query_yaml
from application.database import db
from application.service import UserService, InstructionService
from application.utils import generate_jwt, now
from manager_backend.application.service import instruction
from .login_decorator import login_required
import os

bp_instruction = Blueprint(
    'instruction',
    __name__
)

@bp_instruction.route('/api/v1/instruction/addImage',methods=['POST'])
@login_required
def addImage():
    try:
        Image = request.files.get('file')
        instructionID = request.form["instructionID"]
    except:
        return jsonify({"errCode": 1, "errMsg": "bad arguments"}), 200
    if not os.path.exists("./application/static/instruction/"):
        os.makedirs("./application/static/instruction")
    ImageName = Image.filename
    msg_or_url, _or_name, addStatus = InstructionService.addImage(ImageName, instructionID)
    if not addStatus:
        return jsonify({"errCode": 1, "errMsg": msg_or_url}), 200
    Image.save("./application/static/instruction/" + _or_name)
    return jsonify({"errCode": 0, "ImageURL": msg_or_url}), 200


@bp_instruction.route('/api/v1/instruction/addInstruction',methods=['POST'])
@login_required
def addInstruction():
    try:
        instructionName = request.json["instructionName"]
        instructionTags = request.json["instructionTags"]
    except:
        return jsonify({"errCode":1, "errMsg": "bad arguments"}), 200
    