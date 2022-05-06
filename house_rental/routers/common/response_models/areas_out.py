#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 区域出参 }
# @Date: 2022/05/04 23:16
from typing import List

from pydantic import BaseModel, Field
from house_rental.commons.responses.response_model import ResponseBaseModel


class AreaInfoItem(BaseModel):
    """ 区域信息 """
    id: int = Field(description='区域id')
    name: str = Field(description='区域名称')
    parent_id: int = Field(description='区域父级id')


class CityListItem(AreaInfoItem):
    """ 城市列表项 """
    district_list: List[AreaInfoItem] = Field(description='区县列表')


class ProvinceListItem(BaseModel):
    """ 省份列表项 """
    id: int = Field(description='区域id')
    name: str = Field(description='区域名称')
    city_list: List[CityListItem] = Field(description='城市列表')


class AreasDataItem(BaseModel):
    """ 所有区域信息 """
    area_list: List[ProvinceListItem] = Field(description='省份列表')


class AreasOut(ResponseBaseModel):
    data: AreasDataItem
