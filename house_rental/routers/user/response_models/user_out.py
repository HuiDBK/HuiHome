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


class TokenItem(BaseModel):
    """ token数据模型 """
    token: str = Field(description='token信息')
    refresh_token: str = Field(description='刷新后的token')


class VerifyItem(BaseModel):
    """ 数据校验模型 """
    verify_result: bool = Field(description='校验结果')


class UserRegisterOut(ResponseBaseModel):
    """ 用户注册出参 """
    data: TokenItem = Field(description='用户token')


class UserLoginOut(UserRegisterOut):
    """ 用户登录出参 """


class UserMobileVerifyOut(ResponseBaseModel):
    """ 用户手机号校验出参 """
    data: VerifyItem = Field(description='校验结果')


class UsernameVerifyOut(ResponseBaseModel):
    """ 用户名校验出参 """
    data: VerifyItem = Field(description='校验结果')
