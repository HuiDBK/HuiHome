#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 房源逻辑模块 }
# @Date: 2022/04/23 20:32
from house_rental.constants.enums import RentType
from house_rental.managers.house_manager import HouseInfoManager
from house_rental.commons.utils import serialize_util
from house_rental.routers.house.request_models import HouseListIn
from house_rental.routers.house.response_models import HouseListItem, HomeHouseDataItem
from house_rental.routers.house.response_models.house_out import HouseListDataItem


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


async def get_house_list_logic(item: HouseListIn):
    """ 获取房源列表 """
    print(item.dict())
    filter_params = None
    if item.query_params:
        filter_params = {k: v for k, v in item.query_params.dict().items() if v is not None}
        print(filter_params)
        if filter_params.get('rent_money_range'):
            # 租金范围查询条件转换
            filter_params['rent_money__range'] = filter_params.get('rent_money_range')
            del filter_params['rent_money_range']

    total, house_data_list = await HouseInfoManager.filter_page(
        filter_params=filter_params,
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
