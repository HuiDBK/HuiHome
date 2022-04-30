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
from house_rental.routers.house.response_models.house_out import HouseDetailDataItem
from house_rental.routers.order.response_models.order_out import UserOrderListItem


class OrderHouseInfoItem(HouseDetailDataItem):
    """ 订单房源信息 """


class OrderListItem(UserOrderListItem):
    """ 用户列表数据项模型 """
    house_info: OrderHouseInfoItem = Field(description='房源信息')


class OrderListDataItem(ListResponseDataModel):
    """ 用户数据模型 """
    data_list: List[OrderListItem] = Field(default=[], description="用户数据")


class OrderListOut(ListResponseModel):
    """ 订单列表出参 """
    data: OrderListDataItem
