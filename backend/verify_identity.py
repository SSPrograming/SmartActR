from flask import request, g
from mjwt import decode_jwt

def verify_identity():
    g.userID = None
    try:
        authorization = request.headers.get('Authorization')
    except Exception:
        return
    payload, verified = decode_jwt(authorization)
    if verified:
        g.userID = payload['openID']