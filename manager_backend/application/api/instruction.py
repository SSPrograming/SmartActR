from flask import json, request, jsonify, Blueprint, g
from config import query_yaml
from application.database import db
from application.service import UserService
from application.utils import generate_jwt, now
from .login_decorator import login_required

bp_instruction = Blueprint(
    'instruction',
    __name__
)

@bp_instruction.route('/api/v1/instruction/addImage',methods=['POST'])
@login_required
def addImage():
    return jsonify({"errCode": 0}), 200