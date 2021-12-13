from logging import exception
from flask import request, jsonify, Blueprint, g
from config import query_yaml
from application.models import Admin
from application.database import db
from application.service import AdminService
from application.utils import generate_jwt
import requests

from .login_decorator import login_required

bp_admin = Blueprint(
    'admin',
    __name__
)

@bp_admin.route('/api/v1/admin/getAdminName', methods=['GET'])
@login_required
def getAdminName():
    admin_name = Admin.query.first()
    try:
        admin_name.userName = 'Admin'
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
    return jsonify({"name": admin_name.userName}), 200


@bp_admin.route('/api/v1/admin/login', methods=['POST'])
def login():
    try:
        username = request.json['username']
        pswd = request.json['password']
    except:
        return jsonify({"errCode": 1,"errMsg": "bad agruments"}), 200
    admin_user = AdminService.get_admin(username, pswd)
    if admin_user is None:
        return jsonify({"errCode": 1,"errMsg": "用户名或密码无效"}), 200
    adminjwt = generate_jwt({"username": admin_user.userName})

    return jsonify({"errCode": 0, "jwt": adminjwt})

    
        
