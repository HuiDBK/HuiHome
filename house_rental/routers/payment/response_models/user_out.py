#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 用户模块响应模型 }
# @Date: 2022/04/11 20:23
from pydantic import Field, BaseModel

from house_rental.constants.enums import UserRole


class UserItem(BaseModel):
    """ 用户数据模型 """
    id: int = Field(description='用户id')
    username: str = Field(description='用户名')
    phone: str = Field(description='用户手机号')
    role: UserRole = Field(description='用户角色')


class UserRegisterOut(BaseModel):
    """ 用户注册出参 """
    pass
