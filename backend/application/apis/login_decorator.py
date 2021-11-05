from flask import g, jsonify

def login_required(func):
    def decorated(*args, **kwargs):
        if not g.userID:
            return jsonify({"errCode":2, "errMsg": "未登录或登录凭证失效"}), 200
        else:
            return func(*args, **kwargs)
    decorated.__name__ = 'decorated' + func.__name__
    return decorated