import jwt
from functools import wraps
from db_client import Mongodb
def jwt_jm(token):
    """
    功能对token解密
    :param token:
    :return:
    """

    try:
        payload=jwt.decode(token,'secret',algorithms='HS256')
    except BaseException as e:
        payload={}
    return payload

def checke_putong(fn):
    @wraps(fn)
    def inner():
        user=Mongodb.users.find_one()
        if user['role']!='putong':

        fn()
    return inner