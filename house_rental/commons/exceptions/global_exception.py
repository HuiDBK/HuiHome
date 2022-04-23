#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 全局异常模块 }
# @Date: 2022/04/13 20:51
from house_rental.commons.responses.response_code import ErrorCodeEnum


class BusinessException(Exception):
    """ 业务异常类 """

    def __init__(self, code: int = None, message: str = None):
        """
        业务异常初始化
        :param code: 错误码
        :param message: 错误信息
        """
        self.code = code
        self.message = message

    def exc_data(self, error_enum: ErrorCodeEnum):
        """
        设置异常信息
        :param error_enum: 错误信息枚举
        :return:
        """
        self.code = error_enum.code
        self.message = error_enum.msg
        return self


class AuthorizationException(BusinessException):
    """ 认证异常类 """