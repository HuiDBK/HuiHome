#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 公共请求模型模块 }
# @Date: 2022/04/22 14:32
from typing import List
from pydantic import BaseModel, Field


class ListPageModel(BaseModel):
    """ 分页请求模型 """
    orderings: List = Field(default=None, description='排序字段')
    offset: int = Field(default=0, ge=0, description='分页偏移量')
    limit: int = Field(default=10, gt=0, description='每页显示数量')
