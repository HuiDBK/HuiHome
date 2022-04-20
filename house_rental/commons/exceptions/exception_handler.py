#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 全局异常处理模块 }
# @Date: 2022/04/13 20:48
import logging
import traceback
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from house_rental.commons.responses import fail_response
from .global_exception import BusinessException, AuthorizationException

logger = logging.getLogger()


async def business_exception_handler(
        request: Request,
        exc: BusinessException
):
    """ 全局业务异常处理 """
    logger.info(
        f"Http请求异常\n"
        f"Method\n{request.method}"
        f"URL{request.url}\n"
        f"Headers:{request.headers}\n"
        f"Code:{exc.code}\n"
        f"Message:{exc.message}\n"
    )
    return JSONResponse(
        status_code=200,
        content=fail_response(code=exc.code, message=exc.message)
    )


async def authorization_exception_handler(
        request: Request,
        exc: AuthorizationException
):
    """ 认证异常处理 """
    print('认证失败')
    return JSONResponse(
        status_code=401,
        content=fail_response(code=exc.code, message=exc.message)
    )


async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError
):
    """ 全局捕捉参数验证异常 """
    message = '.'.join([f'{".".join(map(lambda x: str(x), error.get("loc")))}:{error.get("msg")};'
                        for error in exc.errors()])
    print(message)
    return JSONResponse(
        status_code=200,
        content=fail_response(message),
    )


async def global_exception_handler(
        request: Request,
        exc: Exception
):
    """ 全局系统异常处理器 """
    message = f'系统异常, {traceback.format_exc()}'
    logger.error(message)
    return JSONResponse(
        status_code=500,
        content='系统内部异常'
    )
