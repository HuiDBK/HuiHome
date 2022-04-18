#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 用户模块响应模型 }
# @Date: 2022/04/11 20:23
from pydantic import Field, BaseModel

from house_rental.constants.enums import UserRole
from house_rental.commons.responses.response_model import ResponseBaseModel


class UserItem(BaseModel):
    """ 用户数据模型 """
    id: int = Field(description='用户id')
    username: str = Field(description='用户名')
    mobile: str = Field(description='用户手机号')
    role: UserRole = Field(description='用户角色')


class UserRegisterOut(ResponseBaseModel):
    """ 用户注册出参 """
    data: UserItem = Field(description='用户数据')
