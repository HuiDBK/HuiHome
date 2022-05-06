#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 系统公告响应出参模块 }
# @Date: 2022/05/06 20:24
from typing import List

from pydantic import BaseModel, Field

from house_rental.commons.responses.response_model import ListResponseDataModel, ListResponseModel
from house_rental.constants.enums import SystemNoticeSceneEnum, SystemNoticeState


class NewsListItem(BaseModel):
    id: str = Field(description='主键id')
    title: str = Field(max_length=255, description='标题')
    content: str = Field(description='内容')
    scene: SystemNoticeSceneEnum = Field(description='公告场景')
    state: SystemNoticeState = Field(description='公告状态')
    create_ts: float = Field(description='创建时间')


class NewsListDataItem(ListResponseDataModel):
    """ 房源列表数据 """
    data_list: List[NewsListItem] = Field(description='房源列表数据')


class NewsListOut(ListResponseModel):
    """ 房源列表出参 """
    data: NewsListDataItem
