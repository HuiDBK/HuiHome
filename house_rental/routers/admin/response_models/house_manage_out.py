#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 后台用户管理响应模型模块 }
# @Date: 2022/04/22 14:59
from typing import Union
from pydantic import BaseModel, Field
from house_rental.constants.enums import HouseState, RentType, HouseType, RentState
from house_rental.commons.responses.response_model import ResponseBaseModel

#  用户列表出参
from house_rental.routers.user.response_models import UserProfileItem


class UserListItem(UserProfileItem):
    """ 用户列表数据项模型 """


class HouseInfoItem(BaseModel):
    """ 房源信息 """
    house_id: int = Field(description='房源id')
    title: str = Field(description='房源标题')
    index_img: Union[str, None] = Field(description='房源图片')
    address: str = Field(description='房源地址')
    rent_money: int = Field(description='月租金')
    state: HouseState = Field(description='房屋状态')
    rent_type: RentType = Field(description='租赁类型')
    house_type: HouseType = Field(description='房屋类型')
    rent_state: RentState = Field(description='出租状态')
    city: str = Field(description='所在城市')
    bedroom_num: int = Field(description='卧室数量')
    living_room_num: int = Field(default=0, description='客厅数量')


class HouseUpdateOut(ResponseBaseModel):
    """ 房源更新出参 """
    data = HouseInfoItem
