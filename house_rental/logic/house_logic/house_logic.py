#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 房源逻辑模块 }
# @Date: 2022/04/23 20:32
from typing import Union

from house_rental.constants.enums import RentType
from house_rental.managers.house_manager import HouseInfoManager
from house_rental.commons.utils import serialize_util, add_param_if_true
from house_rental.routers.house.request_models import HouseListIn
from house_rental.routers.house.request_models.house_in import HouseListQueryItem
from house_rental.routers.house.response_models import HouseListItem, HomeHouseDataItem
from house_rental.routers.house.response_models.house_out import HouseListDataItem


async def get_home_house_list_logic(city: str):
    """
    获取首页房源列表, 最近整租、合租
    :return: 6整租、6合租
    """
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


def format_house_query_params(query_params: Union[HouseListQueryItem, dict]) -> dict:
    """ 格式化房源信息查询参数 """
    if not query_params:
        return {}

    if isinstance(query_params, HouseListQueryItem):
        query_params = query_params.dict()

    # 去除空值None
    query_params = {k: v for k, v in query_params.items() if v is not None}

    # 租金范围查询条件转换
    add_param_if_true(query_params, 'rent_money__range', query_params.pop('rent_money_range', None))

    # 房源类型、租赁类型、状态、出租状态列表参数转换
    list_params = ['house_type', 'rent_type', 'state', 'rent_state']
    for key in list_params:
        add_param_if_true(query_params, f'{key}__in', query_params.pop(key, None))

    # 房源标题、地址、所在城市支持模糊查询
    like_params = ['title', 'address', 'city']
    for key in like_params:
        add_param_if_true(query_params, f'{key}__icontains', query_params.pop(key, None))
    return query_params


async def get_house_list_logic(item: HouseListIn):
    """ 获取房源列表 """
    query_params = format_house_query_params(item.query_params)
    total, house_data_list = await HouseInfoManager.filter_page(
        filter_params=query_params,
        orderings=item.orderings,
        offset=item.offset,
        limit=item.limit
    )
    house_data_list = [item.to_dict() for item in house_data_list]
    house_data_list = serialize_util.obj2model(data_obj=house_data_list, data_model=HouseListItem)

    return HouseListDataItem(
        total=total,
        data_list=house_data_list,
        next_offset=item.offset + item.limit,
        has_more=False if (item.offset + item.limit) > total else True
    )


async def get_house_detail(house_id: int):
    """ 获取房源详情 """
    pass
