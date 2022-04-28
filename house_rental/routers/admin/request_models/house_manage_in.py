#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 用户模块请求模型 }
# @Date: 2022/03/27 20:23
from typing import Union
from pydantic import Field
from house_rental.routers.house.response_models.house_out import HouseDetailDataItem


class HouseUpdateIn(HouseDetailDataItem):
    """ 房源信息更新入参 """
    house_id: Union[int, None] = Field(description='房源id')
