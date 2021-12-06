from flask import json, request, jsonify, Blueprint, g
from sqlalchemy.sql.operators import exists
from config import query_yaml
from application.database import db
from application.service import UserService, InstructionService
from application.utils import generate_jwt, now
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
        instructionName = request.form["instructionName"]
        instructionCover = request.files.get('instructionCover')
        instructionTags = request.form.get("instructionTags").split(',')
        print(request.form.to_dict())
    except:
        return jsonify({"errCode":1, "errMsg": "bad arguments"}), 200
    
    instructionCoverName = instructionCover.filename
    msg_or_url, addStatus = InstructionService.addInstruction(instructionName, instructionTags, instructionCoverName)
    if not addStatus:
        return jsonify({"errCode": 1, "errMsg": msg_or_url}), 200
    
    if not os.path.exists("./application/static/instructioncover/"):
        os.makedirs("./application/static/instructioncover")

    new_cover_name = msg_or_url.split('/')[-1]
    instructionCover.save('./application/static/instructioncover/'+new_cover_name)
    return jsonify({"errCode": 0}), 200
    
@bp_instruction.route('/api/v1/instruction/updateInstruction',methods=['POST'])
@login_required
def updateInstruction():
    try:
        instructionName = request.form["instructionName"]
        instructionContent = request.form["instructionContent"]
        instructionID = int(request.form["instructionID"])
        instructionTags = request.form["instructionTags"].split(',')
    except:
        return jsonify({"errCode": 1, "errMsg": "bad arguments"}), 200
    msg, updateStatus = InstructionService.updateInstruction(instructionID, instructionName,instructionTags,instructionContent)
    if not updateStatus:
        return jsonify({"errCode": 1,"errMsg": msg}), 200
    else:
        return jsonify({"errCode": 0}), 200

@bp_instruction.route('/api/v1/instruction/getSingleInstruction',methods=['POST'])
@login_required
def getSingleInstruction():
    try:
        instructionID = int(request.json["instructionID"])
    except:
        return jsonify({"errCode": 1, "errMsg": "bad arguments"}), 200
    
    msg, getStatus = InstructionService.getSingleInstruction(instructionID)
    if not getStatus:
        return jsonify({"errCode": 1, "errMsg": msg})
    else:
        return jsonify({"errCode": 0, "instructionContent": msg}), 200

@bp_instruction.route('/api/v1/instruction/getInstructionList',methods=['GET'])
@login_required
def getInstructionList():
    instructionList_raw = InstructionService.getInstructionList()
    instructionList = [
        {
            "instructionID": item.instructionID,
            "instructionName": item.instructionName,
            "instructionCoverURL": item.instructionCoverURL,
            "instructionTags": InstructionService.getInstructionTags(item.instructionID)
        }for item in instructionList_raw
    ]
    return jsonify({"errCode": 0, "instructionList": instructionList}), 200