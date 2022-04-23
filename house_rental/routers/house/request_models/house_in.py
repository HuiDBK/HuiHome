#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 模块描述 }
# @Date: 2022/04/23 20:39
from typing import Optional, List
from pydantic import BaseModel, Field
from house_rental.commons.request_models import ListPageModel

from house_rental.constants.enums import RentType, HouseType, RentState, HouseState


class HouseListQueryItem(BaseModel):
    """ 房源列表查询参数 """
    house_id: Optional[int] = Field(description='房屋id')
    rent_money_range: Optional[List[int]] = Field(description='月租金范围')
    house_owner: Optional[int] = Field(description='房屋拥有者')
    title: Optional[str] = Field(description='房屋标题')
    address: Optional[str] = Field(description='房源地址')
    city: Optional[str] = Field(mdescription='所在城市')
    rent_type: Optional[List[RentType]] = Field(description='租赁类型')
    house_type: Optional[List[HouseType]] = Field(description='房屋类型')
    state: Optional[List[HouseState]] = Field(description='房源状态')
    rent_state: Optional[List[RentState]] = Field(description='房源出租状态')
    area: Optional[int] = Field(gt=0, description='面积')
    bedroom_num: Optional[int] = Field(gt=0, description='卧室数量')
    living_room_num: Optional[int] = Field(ge=0, description='客厅数量')
    kitchen_num: Optional[int] = Field(ge=0, description='厨房数量')
    toilet_num: Optional[int] = Field(ge=0, description='卫生间数量')


class HouseListIn(ListPageModel):
    """ 房源列表入参 """
    query_params: Optional[HouseListQueryItem] = Field(default={}, description='房源列表查询参数')
