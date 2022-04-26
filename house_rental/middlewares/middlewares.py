#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 项目中间件 }
# @Date: 2022/02/28 15:07
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from starlette.types import ASGIApp, Scope, Receive, Send, Message

from house_rental import jwt_authentication
from house_rental.commons import settings
from house_rental.commons.utils import jwt_util
from house_rental.constants.enums import UserRole
from house_rental.managers.user_manager import UserBasicManager


class BaseMiddleware(object):
    """中间件基类"""

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive=receive)
        response = await self.before_request(request) or self.app
        await response(request.scope, request.receive, send)
        await self.after_request(request)

    async def get_body(self, request: Request):
        """获取请求BODY"""
        body = await request.body()
        return body

    async def before_request(self, request: Request) -> [Response, None]:
        """如果需要修改请求信息，可直接重写此方法"""
        return self.app

    async def after_request(self, request: Request):
        """请求后的处理【记录请求耗时等，注意这里没办法对响应结果进行处理】"""
        return None


class AuthorizationMiddleware(BaseMiddleware):
    """ 权限认证中间件 """

    async def before_request(self, request: Request):
        """ 在请求前校验jwt """
        for api_url in settings.API_URL_WHITE_LIST:
            # 在白名单的接口无需token验证
            if str(request.url.path).startswith(api_url):
                return
        # await jwt_authentication(request)
