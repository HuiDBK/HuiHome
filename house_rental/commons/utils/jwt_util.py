#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { jwt 工具模块 }
# @Date: 2022/04/19 18:06
import jwt
from house_rental.commons import settings


def generate_jwt(payload, expiry_time, secret=None, algorithm='HS256'):
    """
    生成jwt
    :param payload: dict 载荷
    :param expiry_time: datetime 有效期
    :param secret: 密钥
    :param algorithm: 加密算法 默认HS256
    :return: jwt
    """
    _payload = {'exp': expiry_time}
    _payload.update(payload)

    if not secret:
        secret = settings.JWT_SECRET

    token = jwt.encode(_payload, secret, algorithm=algorithm)
    return token


def verify_jwt(token, secret=None, algorithms: list = None):
    """
    检验jwt
    :param token: jwt
    :param secret: 密钥
    :param algorithms: 加密算法
    :return: payload
    """
    if not algorithms:
        algorithms = ['HS256']
    if not secret:
        secret = settings.JWT_SECRET

    try:
        payload = jwt.decode(token, secret, algorithms=algorithms)
    except jwt.PyJWTError:
        payload = None
    return payload


def main():
    from datetime import datetime
    from datetime import timedelta
    payload = {'user_id': 123, 'username': 'hui'}
    now = datetime.now()
    print(now)
    expiry = now + timedelta(hours=settings.JWT_EXPIRY_HOURS)
    token = generate_jwt(payload, expiry)
    print(token)

    payload = verify_jwt(token)
    print(payload)


if __name__ == '__main__':
    main()
