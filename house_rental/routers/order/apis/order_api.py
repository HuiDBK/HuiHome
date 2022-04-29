#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 订单API模块 }
# @Date: 2022/04/29 10:25
from fastapi import Path
from house_rental.logic.order_logic import order_logic
from house_rental.commons.responses import success_response
from house_rental.routers.order.request_models import OrderCreateIn


async def create_order(request: OrderCreateIn):
    """ 创建租房订单 """
    data = await order_logic.create_order_logic(request)
    return success_response(data)


async def get_user_orders(user_id: int = Path(..., description='用户id')):
    """ 获取用户租房订单 """
    data = await order_logic.get_user_orders_logic(user_id)
    return success_response(data)
