#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 后台用户管理API模块 }
# @Date: 2022/02/27 21:48
from fastapi import Path, Body
from house_rental.logic.admin_logic.house_manage_logic import update_house_info_logic
from house_rental.commons.responses import success_response
from house_rental.routers.admin.request_models.house_manage_in import HouseUpdateIn


async def update_house_info(
        house_id: int = Path(..., description='房屋id'),
        request: HouseUpdateIn = Body(..., description='房屋更新信息')
):
    """ 更新房源信息 """
    data = await update_house_info_logic(house_id, request)
    return success_response(data)
