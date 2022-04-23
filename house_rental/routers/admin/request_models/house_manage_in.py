#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 用户模块请求模型 }
# @Date: 2022/03/27 20:23
from typing import Optional, Union
from pydantic import Field, BaseModel
from house_rental.commons.request_models import ListPageModel
from house_rental.constants.enums import HouseState, RentType, HouseType, RentState


class HouseUpdateIn(BaseModel):
    """ 房源信息更新入参 """
    title: Optional[str] = Field(description='房源标题')
    index_img: Optional[str] = Field(description='房源图片')
    address: Optional[str] = Field(description='房源地址')
    rent_money: Optional[str] = Field(description='月租金')
    state: Optional[HouseState] = Field(description='房屋状态')
    rent_type: Optional[RentType] = Field(description='租赁类型')
    house_type: Optional[HouseType] = Field(description='房屋类型')
    rent_state: Optional[RentState] = Field(description='出租状态')
    city: Optional[str] = Field(description='所在城市')
    bedroom_num: Optional[int] = Field(description='卧室数量')
    living_room_num: Optional[int] = Field(description='客厅数量')
