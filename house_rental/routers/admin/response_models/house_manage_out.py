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
from house_rental.routers.house.response_models.house_out import HouseDetailDataItem
from house_rental.routers.user.response_models import UserProfileItem


class UserListItem(UserProfileItem):
    """ 用户列表数据项模型 """


class HouseInfoItem(HouseDetailDataItem):
    """ 房源信息 """


class HouseUpdateOut(ResponseBaseModel):
    """ 房源更新出参 """
    data = HouseInfoItem
