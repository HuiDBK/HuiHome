#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 用户管理API模块 }
# @Date: 2022/02/27 21:48
from fastapi import Query
from house_rental.logic.house_logic import house_logic
from house_rental.commons.responses import success_response


async def get_home_house_list(city: str = Query(..., description='房源所在城市')):
    """ 获取首页房源列表 """
    data = await house_logic.get_home_house_list_logic(city)
    return success_response(data)
