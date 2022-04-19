#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 公共响应模型类 }
# @Date: 2022/04/14 4:10
from pydantic import BaseModel


class ResponseBaseModel(BaseModel):
    """ 统一响应模型 """
    code: int
    message: str
    data: dict


class ListResponseDataModel(BaseModel):
    """ 分页列表响应data模型 """
    total: int
    has_more: bool
    next_offset: int
    data_list: list


class ListResponseModel(ResponseBaseModel):
    """ 分页列表响应统一返回 """
    data: ListResponseDataModel


class SuccessModel(ResponseBaseModel):
    """ 请求成功响应模型 """
