#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 房源模块公共数据模型 }
# @Date: 2022/04/28 17:17
from pydantic import BaseModel, Field


class HouseDisplayContentItem(BaseModel):
    """ 房源展示内容信息 """
    images: list = Field(description='房源图片内容')
    videos: list = Field(description='房源视频内容')


class HouseLocationItem(BaseModel):
    """ 房源地理位置信息 """
    nl: str = Field(description='北纬')
    sl: str = Field(description='南纬')
