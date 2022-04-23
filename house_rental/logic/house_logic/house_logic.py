#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 房源逻辑模块 }
# @Date: 2022/04/23 20:32
from house_rental.constants.enums import RentType
from house_rental.managers.house_manager import HouseInfoManager
from house_rental.commons.utils import serialize_util
from house_rental.routers.house.response_models import HouseListItem, HomeHouseDataItem


async def get_home_house_list_logic(city: str):
    """
    获取首页房源列表, 最近整租、合租
    :return: 6整租、6合租
    """
    print(city)
    whole_house_list = await HouseInfoManager.get_recent_house(RentType.whole.value, city)
    share_house_list = await HouseInfoManager.get_recent_house(RentType.share.value, city)

    whole_house_list = [item.to_dict() for item in whole_house_list]
    share_house_list = [item.to_dict() for item in share_house_list]

    whole_house_list = serialize_util.obj2model(data_obj=whole_house_list, data_model=HouseListItem)
    share_house_list = serialize_util.obj2model(data_obj=share_house_list, data_model=HouseListItem)

    return HomeHouseDataItem(
        whole_house_list=whole_house_list,
        share_house_list=share_house_list
    )
