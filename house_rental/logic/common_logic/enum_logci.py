#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 系统枚举接口逻辑模块 }
# @Date: 2022/05/07 22:06
from house_rental.commons.responses.response_code import ErrorCodeEnum


async def get_error_enum_logic():
    """ 获取错误码枚举信息 """
    error_names = ErrorCodeEnum.get_member_names()
    error_values = ErrorCodeEnum.get_member_values()

    error_enum_dict = {}
    for error_name, (error_code, error_msg) in zip(error_names, error_values):
        error_enum_dict[error_code] = dict(name=error_name, code=error_code, message=error_msg)

    return error_enum_dict
