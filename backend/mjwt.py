import jwt
import datetime
import base64
import hashlib
import scrypt

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

    secret = "^753*&FdFS#4D"            #TODO:后续需要写在配置文件中

    token = jwt.encode(_payload, secret, algorithm='HS256')
    return token.decode()