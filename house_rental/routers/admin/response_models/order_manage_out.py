#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 后台订单管理响应模型模块 }
# @Date: 2022/04/22 14:59
from datetime import date
from typing import List, Union
from pydantic import BaseModel, Field
from house_rental.commons.responses.response_model import ListResponseModel, ListResponseDataModel
from house_rental.constants.enums import OrderState


class OrderListItem(BaseModel):
    """ 用户列表数据项模型 """
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


class OrderListDataItem(ListResponseDataModel):
    """ 用户数据模型 """
    data_list: List[OrderListItem] = Field(default=[], description="用户数据")


class OrderListOut(ListResponseModel):
    """ 订单列表出参 """
    data: OrderListDataItem
