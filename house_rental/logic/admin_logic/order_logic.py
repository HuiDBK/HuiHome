#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 后台订单逻辑模块 }
# @Date: 2022/04/29 23:21
import asyncio

from house_rental.commons.utils import serialize_util
from house_rental.managers.house_manager import HouseInfoManager
from house_rental.managers.order_manager import OrderManager
from house_rental.managers.user_manager import UserProfileManager
from house_rental.routers.admin.request_models.order_manage_in import GetOrderListInRequest
from house_rental.routers.admin.response_models.order_manage_out import OrderListItem, OrderListDataItem


async def get_order_list_logic(order_item: GetOrderListInRequest):
    """ 获取订单列表逻辑 """
    query_params = order_item.query_params.dict() if order_item.query_params else {}
    query_params = {k: v for k, v in query_params.items() if v is not None}
    total, order_list = await OrderManager.filter_page(
        filter_params=query_params,
        limit=order_item.limit,
        offset=order_item.offset,
        orderings=order_item.orderings
    )

    # 补充订单信息
    house_ids = list(set([order.house_id for order in order_list]))  # 房屋id列表
    landlord_ids = list(set([order.landlord_id for order in order_list]))  # 房东id列表
    tenant_ids = list(set([order.tenant_id for order in order_list]))  # 租客id列表

    house_info, user_profiles, landlord_profiles = await asyncio.gather(*[
        HouseInfoManager.get_houses_by_ids(house_ids),  # 房源信息
        UserProfileManager.get_users_by_ids(tenant_ids),  # 用户信息
        UserProfileManager.get_users_by_ids(landlord_ids)  # 房东信息
    ])

    # 先把房源、房东、租客信息变成大字典方便订单补
    landlord_info_dict = {item.id: item for item in landlord_profiles}
    house_info_dict = {item.id: item for item in house_info}
    user_info_dict = {item.id: item for item in user_profiles}

    order_list = [order.to_dict() for order in order_list]
    for order in order_list:
        house_info = house_info_dict.get(order.get('house_id'))
        landlord_info = landlord_info_dict.get(order.get('landlord_id'))
        user_info = user_info_dict.get(order.get('tenant_id'))
        order['user_info'] = user_info.to_dict()
        order['house_info'] = house_info.to_dict()
        order['landlord_info'] = landlord_info.to_dict()

    order_list = serialize_util.data_to_model(data_obj=order_list, data_model=OrderListItem)

    return OrderListDataItem(
        total=total,
        data_list=order_list,
        next_offset=order_item.offset + order_item.limit,
        has_more=False if (order_item.offset + order_item.limit) > total else True
    )
