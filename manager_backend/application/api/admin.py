from logging import exception
from flask import request, jsonify, Blueprint, g
from config import query_yaml
from application.models import Admin
from application.database import db
import requests

bp_admin = Blueprint(
    'admin',
    __name__
)

@bp_admin.route('/api/v1/admin/getAdminName', methods=['GET'])
def getAdminName():
    admin_name = Admin.query.first()
    print(admin_name.userName)
    try:
        admin_name.userName = 'Admin'
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
    return jsonify({"name": admin_name.userName}), 200
