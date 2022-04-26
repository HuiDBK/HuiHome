#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 项目接口依赖(depends)模块 }
# @Date: 2022/04/26 22:59
from starlette.requests import Request

from house_rental.commons.exceptions.global_exception import AuthorizationException
from house_rental.commons.responses import ErrorCodeEnum
from house_rental.commons.utils import jwt_util
from house_rental.constants.enums import UserRole
from house_rental.managers.user_manager import UserBasicManager


async def jwt_authentication(request: Request):
    """ jwt 鉴权"""
    token = request.headers.get('Authorization') or None
    if not token:
        raise AuthorizationException().exc_data(ErrorCodeEnum.AUTHORIZATION_ERR)

    token = str(token)[7:]
    user_info = jwt_util.verify_jwt(token)
    if not user_info:
        # 无效token
        raise AuthorizationException().exc_data(ErrorCodeEnum.AUTHORIZATION_ERR)

    # 校验通过保存到request.user中
    user_id = user_info.get('user_id')
    user = await UserBasicManager.get_by_id(user_id)

    if user.role != UserRole.admin.value and str(request.url.path).startswith('/api/v1/admin'):
        # 不是管理员无法访问了后台模块接口
        raise AuthorizationException().exc_data(ErrorCodeEnum.AUTHORIZATION_ERR)

    request.scope['user'] = user


async def login_required(request: Request):
    """ 登录权限校验 """
    try:
        user = request.user
    except:
        raise AuthorizationException().exc_data(ErrorCodeEnum.AUTHORIZATION_ERR)

    if not user:
        raise AuthorizationException().exc_data(ErrorCodeEnum.AUTHORIZATION_ERR)
