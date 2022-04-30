#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 支付API模块 }
# @Date: 2022/05/01 0:07
from typing import Union

from fastapi import Path, Body
from house_rental.commons.responses import success_response
from house_rental.logic.payment_logic import payment_logic


async def alipay_order_api(
        order_id: int = Path(..., description='订单id'),
        request: Union[dict] = Body(description='订单请求入参')
):
    """ 订单支付接口（阿里支付宝）"""
    data = await payment_logic.alipay_order_logic(order_id, request)
    return success_response(data)
