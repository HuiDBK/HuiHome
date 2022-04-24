#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 用户管理API模块 }
# @Date: 2022/02/27 21:48
from fastapi import Query, Path
from house_rental.logic.house_logic import house_logic
from house_rental.commons.responses import success_response
from house_rental.routers.house.request_models import HouseListIn


async def get_home_house_list(city: str = Query(..., description='房源所在城市')):
    """ 获取首页房源列表 """
    data = await house_logic.get_home_house_list_logic(city)
    return success_response(data)


async def get_house_list(request: HouseListIn):
    """ 获取房源列表 """
    data = await house_logic.get_house_list_logic(request)
    return success_response(data)


async def get_house_detail(house_id: int = Path(..., description='房源id')):
    """ 获取房源详情 """
    data = await house_logic.get_house_detail_logic(house_id)
    return success_response(data)


async def get_all_house_facility():
    """ 获取所有的房屋设施信息 """
    data = await house_logic.get_all_house_facility_logic()
    return success_response(data)
