#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 项目响应封装模块 }
# @Date: 2022/04/13 23:02
from house_rental.commons.responses.response_code import ErrorCodeEnum


def _format_success_response(data=None):
    """ 成功的响应 """
    data = data or {}
    response_content = {
        'code': ErrorCodeEnum.OK.code,
        'message': ErrorCodeEnum.OK.msg,
        'data': data or {}
    }
    return response_content


def _format_fail_response(message, data=None, code=-1):
    """ 失败的响应 """
    response_content = {
        'code': code,
        'message': str(message),
        'data': data or {}
    }
    return response_content


def success_response(data=None):
    """ 成功的响应 """
    return _format_success_response(data)


def fail_response(message, data=None, code=-1):
    """ 失败的响应 """
    return _format_fail_response(message, data, code)
