#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 项目接口依赖(depends)模块 }
# @Date: 2022/04/26 22:59
from starlette.requests import Request

from house_rental.commons import settings
from house_rental.commons.exceptions.global_exception import AuthorizationException
from house_rental.commons.responses import ErrorCodeEnum
from house_rental.commons.utils import jwt_util, context_util
from house_rental.constants.enums import UserRole
from house_rental.managers.user_manager import UserBasicManager


async def jwt_authentication(request: Request):
    """ jwt 鉴权"""
    for api_url in settings.API_URL_WHITE_LIST:
        # 在白名单的接口无需token验证
        if str(request.url.path).startswith(api_url):
            return
    token = request.headers.get('Authorization') or None
    if not token:
        raise AuthorizationException()

    # Bearer 占了7位
    if not str(token).startswith('Bearer '):
        raise AuthorizationException()

    token = str(token)[7:]
    user_info = jwt_util.verify_jwt(token)
    if not user_info:
        # 无效token
        raise AuthorizationException()

    # 校验通过保存到request.user中
    user_id = user_info.get('user_id')
    user = await UserBasicManager.get_by_id(user_id)

    if user.role != UserRole.admin.value and str(request.url.path).startswith('/api/v1/admin'):
        # 不是管理员无法访问了后台模块接口
        raise AuthorizationException()

    request.scope['user'] = user


async def request_context(request: Request):
    """ 保存当前request对象到上下文中 """
    context_util.REQUEST_CONTEXT.set(request)


async def login_required(request: Request):
    """ 登录权限校验 """
    try:
        user = request.user
    except:
        raise AuthorizationException().exc_data(ErrorCodeEnum.AUTHORIZATION_ERR)

    if not user:
        raise AuthorizationException().exc_data(ErrorCodeEnum.AUTHORIZATION_ERR)
