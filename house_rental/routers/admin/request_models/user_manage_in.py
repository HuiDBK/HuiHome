#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 用户模块请求模型 }
# @Date: 2022/03/27 20:23
from typing import Optional, List

from pydantic import BaseModel, Field

from house_rental.commons.request_models import ListPageRequestModel
from house_rental.constants.enums import UserAuthStatus, UserState


class UserListQueryItem(BaseModel):
    """ 用户列表查询参数 """
    user_id:     Optional[int] = Field(description='用户id')
    mobile:      Optional[str] = Field(description='手机号')
    real_name:   Optional[str] = Field(description='用户真姓名')
    gender:      Optional[str] = Field(description='性别')
    career:      Optional[str] = Field(description='用户职业')
    state:       Optional[List[UserState]]      = Field(description='用户的状态')
    auth_status: Optional[List[UserAuthStatus]] = Field(description='用户实名认证状态')


class UserListInRequest(ListPageRequestModel):
    """ 用户列表入参 """
    query_params: Optional[UserListQueryItem] = Field(default={}, description='查询参数')
