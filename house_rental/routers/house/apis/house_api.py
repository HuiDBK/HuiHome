#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 用户管理API模块 }
# @Date: 2022/02/27 21:48
from fastapi import Query, Path, Depends
from starlette.requests import Request

from house_rental.commons.exceptions.global_exception import AuthorizationException
from house_rental.logic.house_logic import house_logic
from house_rental.commons.responses import success_response, ErrorCodeEnum
from house_rental.routers.house.request_models import HouseListIn
from house_rental.routers.house.request_models.house_in import PublishHouseIn, HouseFacilityAddIn, HouseCollectIn


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


async def publish_house(request: PublishHouseIn):
    """ 发布房源信息 """
    data = await house_logic.publish_house_logic(request)
    return success_response(data)


async def add_house_facility(request: HouseFacilityAddIn):
    """ 添加房源设施 """
    data = await house_logic.add_house_facility_logic(request)
    return success_response(data)


async def user_house_collect(
        request: HouseCollectIn
):
    """ 添加房源设施 """
    data = await house_logic.user_house_collect_logic(**request.dict())
    return success_response(data)


async def get_user_house_collect(
        user_id: int = Path(..., description='用户id')
):
    """ 添加房源设施 """
    data = await house_logic.get_user_house_collect_logic(user_id)
    return success_response(data)
