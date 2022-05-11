#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 系统枚举API模块 }
# @Date: 2022/05/07 21:38
from house_rental.commons.responses import success_response
from house_rental.logic.common_logic import enum_logci


async def get_error_enum():
    """ 获取系统错误枚举信息 """
    data = await enum_logci.get_error_enum_logic()
    return success_response(data)
