#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 支付模块请求模型 }
# @Date: 2022/03/27 20:23
from pydantic import Field, BaseModel
from typing import Optional

from house_rental.constants.enums import PaymentSceneEnum


class OrderPaymentIn(BaseModel):
    """ 订单支付入参 """
    start_date: Optional[str]    = Field(description='开始入住日期')
    end_date:   Optional[str]    = Field(description='结束日期')
    pay_scene:  PaymentSceneEnum = Field(description='支付场景（全额、预定）')
