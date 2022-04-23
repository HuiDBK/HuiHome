#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 模块描述 }
# @Date: 2022/04/23 20:39
from pydantic import BaseModel, Field
from house_rental.commons.request_models import ListPageModel
from house_rental.constants.enums import RentType


class HomeHouseIn(BaseModel):
    """ 首页房源入参 """
    rent_type: RentType = Field(..., description='租赁类型（整租、合租）')

    pass
