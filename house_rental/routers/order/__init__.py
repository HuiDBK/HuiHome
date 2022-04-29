#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 订单路由模块 }
# @Date: 2022/02/27 21:43
from fastapi import APIRouter
from .apis import order_api
from .response_models import order_out

router = APIRouter()

router.add_api_route(
    '/orders',
    order_api.create_order,
    methods=['post'],
    summary='创建租房订单'
)

router.add_api_route(
    '/orders/{user_id}',
    order_api.get_user_orders,
    response_model=order_out.UserOrderListOut,
    methods=['get'],
    summary='获取用户租房订单'
)
