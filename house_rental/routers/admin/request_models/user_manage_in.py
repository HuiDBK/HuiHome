#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 用户模块请求模型 }
# @Date: 2022/03/27 20:23
from typing import Optional

from pydantic import BaseModel, Field

from house_rental.commons.request_models import ListPageModel
from house_rental.constants.enums import UserAuthStatus


class UserListQueryItem(BaseModel):
    """ 用户列表查询参数 """
    username: Optional[str] = Field(description='用户名')
    mobile: Optional[str] = Field(description='手机号')
    real_name: Optional[str] = Field(description='用户真姓名')
    avatar: Optional[str] = Field(description='用户头像')
    mail: Optional[str] = Field(description='电子邮件')
    id_card: Optional[str] = Field(description='身份证号')
    gender: Optional[str] = Field(description='性别')
    hobby: Optional[str] = Field(description='用户爱好')
    career: Optional[str] = Field(description='用户职业')
    auth_status: Optional[UserAuthStatus] = Field(description='用户实名认证状态')


class UserListIn(ListPageModel):
    """ 用户列表入参 """
    query_params: Optional[UserListQueryItem] = Field(default={}, description='查询参数')
