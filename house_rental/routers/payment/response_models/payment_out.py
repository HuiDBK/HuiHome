#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 用户模块响应模型 }
# @Date: 2022/04/11 20:23
from pydantic import Field, BaseModel
from house_rental.commons.responses.response_model import ResponseBaseModel


class OrderPaymentDataItem(BaseModel):
    """ 订单支付出参信息 """
    order_id:   int = Field(description='订单id')
    alipay_url: str = Field(description='阿里支付url')


class OrderPaymentOut(ResponseBaseModel):
    """ 订单支付出参 """
    data = OrderPaymentDataItem
