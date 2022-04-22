#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 用户模块请求模型 }
# @Date: 2022/03/27 20:23
from pydantic import Field, BaseModel
from house_rental.commons.request_models import ListPageModel


class UserListIn(ListPageModel):
    """ 用户列表入参 """
