#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 订单响应出参模块 }
# @Date: 2022/04/29 16:18
from datetime import date, datetime
from typing import List, Union
from pydantic import BaseModel, Field
from house_rental.commons.responses.response_model import ResponseBaseModel
from house_rental.constants.enums import OrderState


class UserOrderListItem(BaseModel):
    """ 用户订单列表项数据 """
    order_id: int = Field(description='订单id')
    tenant_id: int = Field(description='租客id')
    landlord_id: int = Field(description='房东id')
    house_id: int = Field(description='房源id')
    start_date: date = Field(description='开始日期')
    end_date: date = Field(description='结束日期')
    state: OrderState = Field(description='订单状态')
    contract_content: Union[str, None] = Field(description='合同内容')
    pay_money: str = Field(description='支付金额')
    deposit_fee: str = Field(description='押金')
    rental_days: int = Field(description='租赁天数')
    create_ts: int = Field(description='创建时间')


class UserOrderDataItem(BaseModel):
    """ 用户订单数据项 """
    user_orders: List[UserOrderListItem] = Field(description='用户订单列表')


class UserOrderListOut(ResponseBaseModel):
    """ 用户订单列表出参 """
    data: UserOrderDataItem
