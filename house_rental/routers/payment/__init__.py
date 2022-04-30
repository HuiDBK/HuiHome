#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 订单支付模块 }
# @Date: 2022/02/27 21:43
from fastapi import APIRouter
from .apis import payment_api

router = APIRouter()

router.add_api_route(
    '/alipay/orders/{order_id}',
    payment_api.alipay_order_api,
    methods=['get'],
    summary='订单支付（支付宝）'
)