#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 后台订单请求模型入参模块 }
# @Date: 2022/04/29 23:11
from typing import Optional
from datetime import date
from pydantic import BaseModel, Field

from house_rental.commons.request_models import ListPageRequestModel
from house_rental.constants.enums import OrderState


class OrderListQueryItem(BaseModel):
    """ 订单列表查询参数信息 """
    order_id:    Optional[int] = Field(description='订单id')
    tenant_id:   Optional[int] = Field(description='租客id')
    landlord_id: Optional[int] = Field(description='房东id')
    house_id:    Optional[int] = Field(description='房源id')
    start_date:  Optional[int] = Field(description='开始日期')
    end_date:    Optional[int] = Field(description='结束日期')
    pay_money:   Optional[str] = Field(description='支付金额')
    deposit_fee: Optional[str] = Field(description='押金')
    rental_days: Optional[int] = Field(description='租赁天数')
    state:       Optional[OrderState] = Field(description='订单状态')


class GetOrderListInRequest(ListPageRequestModel):
    """ 获取订单列表入参 """
    query_params: Optional[OrderListQueryItem] = Field(description='查询参数')
