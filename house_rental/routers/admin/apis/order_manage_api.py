#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 后台订单API模块 }
# @Date: 2022/04/29 23:10
from house_rental.logic.admin_logic.order_logic import get_order_list_logic
from house_rental.routers.admin.request_models.order_manage_in import GetOrderListIn
from house_rental.commons.responses import success_response


async def get_order_list(request: GetOrderListIn):
    """ 获取订单列表 """
    data = await get_order_list_logic(request)
    return success_response(data)
