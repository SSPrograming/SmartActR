from flask import json, request, jsonify, Blueprint, g
from config import query_yaml
from application.database import db
from application.service import ruleService
from application.utils import generate_jwt, now
from .login_decorator import login_required
import datetime

bp_rule = Blueprint(
    'rule',
    __name__
)

@bp_rule.route('/manager-api/v1/rules/addRule', methods=['POST'])
@login_required
def addRule():
    argumentErr = {"errCode": 1, "errMsg": "bad arguments"}
    ruleContent = {}
    try:
        repeat = request.json["repeat"]
        startTime = request.json["startTime"]
        endTime = request.json["endTime"]
        ruleContent["startTime"] = startTime
        ruleContent["endTime"] = endTime
        ruleDescription = request.json["ruleDescription"]
        ruleContent["ruleDescription"] = ruleDescription
    except:
        return jsonify(argumentErr), 200
    if repeat == 1:
        try:
            expireDate = request.json["expireDate"]
            ruleContent["expireDate"] = expireDate
            day = request.json["day"]
            if day==0:
                day=7
            ruleContent["day"] = day
        except:
            return jsonify(argumentErr), 200
    elif repeat==0:
        try:
            date = request.json["date"]
            ruleContent["expireDate"] = date
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


@bp_rule.route('/manager-api/v1/rules/updateRule', methods=['POST'])
@login_required
def updateRule():
    argumentErr = {"errCode": 1, "errMsg": "bad arguments"}
    ruleContent = {}
    try:
        ruleID = request.json["ruleID"]
        repeat = request.json["repeat"]
        startTime = request.json["startTime"]
        endTime = request.json["endTime"]
        ruleContent["startTime"] = startTime
        ruleContent["endTime"] = endTime
        ruleDescription = request.json["ruleDescription"]
        ruleContent["ruleDescription"] = ruleDescription
    except:
        return jsonify(argumentErr), 200
    if repeat == 1:
        try:
            expireDate = request.json["expireDate"]
            ruleContent["expireDate"] = expireDate
            day = request.json["day"]
            if day==0:
                day=7
            ruleContent["day"] = day
        except:
            return jsonify(argumentErr), 200
    elif repeat==0:
        try:
            date = request.json["date"]
            ruleContent["expireDate"] = date
            ruleContent["date"] = date
        except:
            return jsonify(argumentErr), 200
    else:
        return jsonify(argumentErr)
    
    msg, addStatus = ruleService.updateRule(ruleID, repeat, ruleContent)
    if not addStatus:
        return jsonify({"errCode": 1, "errMsg": msg}), 200
    else:
        return jsonify({"errCode": 0}), 200
    

@bp_rule.route('/manager-api/v1/rules/getRules', methods=['GET'])
@login_required
def getRules():
    rule_list_raw = ruleService.get_rule_list()
    now_datetime = now()
    now_date = datetime.date(now_datetime.year, now_datetime.month, now_datetime.day)
    rule_list_ret = []
    for item in rule_list_raw:
        rule = {}
        rule["repeat"] = item.repeat
        if item.repeat==1:
            rule["day"] = item.day % 7
        else:
            rule["date"] = str(item.date)
        rule["startTime"] = item.startTime.strftime("%H:%M")
        rule["endTime"] = item.endTime.strftime("%H:%M")
        rule["expireDate"] = str(item.expireDate)
        rule["takeEffectDate"] = str(now_date)
        rule["ruleID"] = item.ruleID
        rule["ruleDescription"] = '' if item.ruleDescription is None else item.ruleDescription
        rule_list_ret.append(rule)
    return jsonify({"rules": rule_list_ret, "errCode": 0}), 200

@bp_rule.route('/manager-api/v1/rules/deleteRule', methods=['POST'])
@login_required
def deleteRule():
    argumentErr = {"errCode": 1, "errMsg": "bad arguments"}
    try:
        ruleID = request.json["ruleID"]
    except:
        return jsonify(argumentErr), 200
    msg, deleteStatus = ruleService.deleteRule(ruleID=ruleID)
    if deleteStatus:
        return jsonify({"errCode": 0}), 200
    else:
        return jsonify({"errCode": 1, "errMsg": msg}), 200