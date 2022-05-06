#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 系统公告模块入参 }
# @Date: 2022/04/23 20:39
from typing import Optional, List
from pydantic import BaseModel, Field
from house_rental.commons.request_models import ListPageRequestModel


class NewsListQueryItem(BaseModel):
    """ 房源列表查询参数 """
    id: Optional[int] = Field(description='主键id')


class NewsListInRequest(ListPageRequestModel):
    """ 房源列表入参 """
    query_params: Optional[NewsListQueryItem] = Field(default={}, description='房源列表查询参数')
