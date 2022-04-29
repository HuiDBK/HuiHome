#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 后台订单逻辑模块 }
# @Date: 2022/04/29 23:21
from house_rental.commons.utils import serialize_util
from house_rental.managers.order_manager import OrderManager
from house_rental.routers.admin.request_models.order_manage_in import GetOrderListIn
from house_rental.routers.admin.response_models.order_manage_out import OrderListItem, OrderListDataItem


async def get_order_list_logic(order_item: GetOrderListIn):
    """ 获取订单列表逻辑 """
    total, order_list = await OrderManager.filter_page(
        filter_params=order_item.query_params,
        limit=order_item.limit,
        offset=order_item.offset,
        orderings=order_item.orderings
    )
    order_list = serialize_util.obj2DataModel(data_obj=order_list, data_model=OrderListItem)

    return OrderListDataItem(
        total=total,
        data_list=order_list,
        next_offset=order_item.offset + order_item.limit,
        has_more=False if (order_item.offset + order_item.limit) > total else True
    )
