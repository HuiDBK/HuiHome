#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 用户模块响应模型 }
# @Date: 2022/04/11 20:23
from typing import Union, List
from pydantic import Field, BaseModel
from house_rental.constants.enums import UserRole, RentType
from house_rental.commons.responses.response_model import ResponseBaseModel


class HouseListItem(BaseModel):
    """ 房源列表项信息 """
    house_id: int = Field(description='房源id')
    title: str = Field(description='房源标题')
    index_img: Union[str, None] = Field(description='房源图片')
    address: str = Field(description='房源地址')
    rent_money: int = Field(description='月租金')
    rent_type: RentType = Field(description='租赁类型')
    city: str = Field(description='所在城市')
    bedroom_num: int = Field(description='卧室数量')
    living_room_num: int = Field(default=0, description='客厅数量')


class HomeHouseDataItem(BaseModel):
    """ 首页房源数据信息 """
    whole_house_list: List[HouseListItem] = Field(description='整租房源列表')
    share_house_list: List[HouseListItem] = Field(description='合租房源列表')


class HomeHouseInfoOut(ResponseBaseModel):
    """ 首页房源信息出参 """
    data: HomeHouseDataItem
