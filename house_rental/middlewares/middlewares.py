#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 项目中间件 }
# @Date: 2022/02/28 15:07
import time

from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from house_rental.commons.utils.dependencies import jwt_authentication
from house_rental.commons import settings


class PreventCrawlerMiddleware(BaseHTTPMiddleware):
    """ 预防爬虫中间件 """
    NotAllowUAList = [
        "PostmanRuntime",
        "Python"
    ]

    async def dispatch(
            self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        headers = request.headers
        print(headers.get('user-agent'))
        print(headers.get('referer'))
        for not_allow_ua in self.NotAllowUAList:
            if not_allow_ua in headers.get("user-agent"):
                raise Exception("非法请求")

        resp = await call_next(request)
        return resp


class AuthorizationMiddleware(BaseHTTPMiddleware):
    """ 权限认证中间件 """

    async def dispatch(
            self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        for api_url in settings.API_URL_WHITE_LIST:
            # 在白名单的接口无需token验证
            if str(request.url.path).startswith(api_url):
                return await call_next(request)

        await jwt_authentication(request)

        return await call_next(request)


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    日志中间件
    记录请求参数信息、计算响应时间
    """

    async def set_body(self, request: Request):
        receive_ = await request._receive()

        async def receive():
            return receive_

        request._receive = receive

    async def dispatch(self, request: Request, call_next) -> Response:
        start_time = time.perf_counter()

        # 打印请求信息
        logger.info(f"--> {request.method} {request.url.path} {request.client.host}")
        if request.query_params:
            logger.info(f"--> Query Params: {request.query_params}")

        if "application/json" in request.headers.get("Content-Type", ""):
            await self.set_body(request)
            try:
                # starlette 中间件中不能读取请求数据，否则会进入循环等待 需要特殊处理或者换APIRoute实现
                body = await request.json()
                logger.info(f"--> Body: {body}")
            except Exception as e:
                logger.warning(f"Failed to parse JSON body: {e}")

        # 执行请求获取响应
        response = await call_next(request)

        # 计算响应时间
        process_time = time.perf_counter() - start_time
        response.headers["X-Response-Time"] = f"{process_time:.2f}s"
        logger.info(f"<-- {response.status_code} {request.url.path} (took: {process_time:.2f}s)\n")

        return response
