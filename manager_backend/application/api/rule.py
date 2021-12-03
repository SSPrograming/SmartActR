from flask import request, jsonify, Blueprint, g
from config import query_yaml
from application.database import db
from application.service import ruleService
from application.utils import generate_jwt
from .login_decorator import login_required

bp_rule = Blueprint(
    'rule',
    __name__
)

@bp_rule.route('/api/v1/rules/addRule', methods=['POST'])
@login_required
def addRule():
    argumentErr = {"errCode": 1, "errMsg": "bad arguments"}
    ruleContent = {}
    try:
        repeat = request.json["repeat"]
        startTime = request.json["startTime"]
        endTime = request.json["endTime"]
        expireDate = request.json["expireDate"]
        ruleContent["startTime"] = startTime
        ruleContent["endTime"] = endTime
        ruleContent["expireDate"] = expireDate
    except:
        return jsonify(argumentErr), 200
    if repeat == 1:
        try:
            day = request.json["day"]
            ruleContent["day"] = day
        except:
            return jsonify(argumentErr), 200
    elif repeat==0:
        try:
            date = request.json["date"]
            ruleContent["date"] = date
        except:
            return jsonify(argumentErr), 200
    else:
        return jsonify(argumentErr)
    
    msg, addStatus = ruleService.addRule(repeat, ruleContent)
    if not addStatus:
        return jsonify({"errCode": 1, "errMsg": msg}), 200
    else:
        return jsonify({"errCode": 0}), 200
    
