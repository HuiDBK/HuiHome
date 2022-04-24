#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 用户初始化模块 }
# @Date: 2022/02/27 21:43
from fastapi import APIRouter
from .apis import house_api
from house_rental.routers.house.response_models import house_out

router = APIRouter()

router.add_api_route(
    '/home_houses',
    house_api.get_home_house_list,
    methods=['get'],
    response_model=house_out.HomeHouseInfoOut,
    summary='获取首页房源'
)

router.add_api_route(
    '/houses',
    house_api.get_house_list,
    methods=['post'],
    response_model=house_out.HouseListOut,
    summary='获取房源列表信息'
)


router.add_api_route(
    '/houses/{house_id}',
    house_api.get_house_detail,
    methods=['get'],
    response_model=house_out.HouseDetailOut,
    summary='获取房源详情信息'
)


router.add_api_route(
    '/facilities',
    house_api.get_all_house_facility,
    methods=['get'],
    response_model=house_out.HouseFacilitiesOut,
    summary='获取全部房屋设施信息'
)