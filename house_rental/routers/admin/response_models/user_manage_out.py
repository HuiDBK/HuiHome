#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 后台用户管理响应模型模块 }
# @Date: 2022/04/22 14:59
from typing import List
from pydantic import BaseModel, Field
from house_rental.constants.enums import UserRole
from house_rental.commons.responses.response_model import ListResponseModel, ListResponseDataModel

#  用户列表出参
from house_rental.routers.user.response_models import UserProfileItem


class UserListItem(UserProfileItem):
    """ 用户列表数据项模型 """


class UserListDataItem(ListResponseDataModel):
    """ 用户数据模型 """
    data_list: List[UserListItem] = Field(default=[], description="用户数据")


class UserListOut(ListResponseModel):
    """ 用户列表出参 """
    data: UserListDataItem
