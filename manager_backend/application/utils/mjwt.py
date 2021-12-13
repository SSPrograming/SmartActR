import jwt
import datetime
from config import query_yaml
import scrypt
import base64

def generate_jwt(payload, expiry=None):
    """
    :param payload: dict 载荷
    :param expiry: datetime 有效期
    :return: 生成jwt
    """
    if expiry == None:
        now = datetime.datetime.now()
        expire_hours = 24
        expiry = now + datetime.timedelta(hours=expire_hours)

    _payload = {'exp': expiry}
    _payload.update(payload)

    secret = query_yaml('app.SECRET')

    token = jwt.encode(_payload, secret, algorithm='HS256')
    return token.decode()

def decode_jwt(authorization):
    secret = query_yaml('app.SECRET')
    try:
        payload = jwt.decode(authorization, secret, algorithms='HS256')
        return payload, True
    except Exception as e:
        return e, False

def encrypt_password(password):
    salt = query_yaml('app.SALT')
    key = scrypt.hash(password, salt, 32768, 8, 1, 32)
    return base64.b64encode(key).decode("ascii")

def hash_code(raw_str):
    qrsalt = query_yaml('app.QRSALT')
    key = scrypt.hash(raw_str, qrsalt, 32768, 8, 1, 32)
    return base64.b64encode(key).decode("ascii")
