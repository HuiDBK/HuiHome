#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 文件上传模块出参 }
# @Date: 2022/04/11 20:23
from typing import Union, List
from pydantic import Field, BaseModel
from house_rental.commons.responses.response_model import ResponseBaseModel


class UploadFileDataItem(BaseModel):
    """ 文件上传出参信息 """
    file_name: str = Field(description='文件名称')
    file_key:  str = Field(description='文件唯一key')
    file_url:  str = Field(description='访问文件的url地址')


class BatchUploadDataItem(BaseModel):
    """ 批量文件上传出参信息 """
    file_list: List[UploadFileDataItem] = Field(description='文件列表')


class UploadFileOut(ResponseBaseModel):
    """ 上传文件出参 """
    data: UploadFileDataItem


class BatchUploadFileOut(ResponseBaseModel):
    """ 批量上传文件出参 """
    data: BatchUploadDataItem
