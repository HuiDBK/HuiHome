#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 后台房源管理逻辑模块 }
# @Date: 2022/04/24 1:07
from house_rental.managers.house_manager import HouseInfoManager, HouseDetailManager
from house_rental.routers.admin.request_models import HouseUpdateIn
from house_rental.routers.admin.response_models.house_manage_out import HouseInfoItem


async def update_house_info_logic(house_id: int, house_item: HouseUpdateIn):
    """ 更新房源信息逻辑 """
    house_info = await HouseInfoManager.get_by_id(house_id)
    house_detail = await HouseDetailManager.get_by_id(house_id)
    if house_info and not house_detail:
        house_detail = await HouseDetailManager.create(house_info.to_dict())
    house_item = {k: v for k, v in house_item.dict().items() if v is not None}

    if house_item:
        house_info.update_from_dict(house_item)
        house_detail.update_from_dict(house_item)
        await house_info.save()
        await house_detail.save()

    # 房源基本信息和房源详情信息组装到一起
    house_detail_item = house_detail.to_dict()
    house_detail_item.update(house_info.to_dict())

    return HouseInfoItem(**house_detail_item)