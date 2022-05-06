#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 后台用户管理API模块 }
# @Date: 2022/02/27 21:48
from fastapi import Query
from house_rental.logic.admin_logic.user_manage_logic import get_user_list_logic
from house_rental.routers.admin.request_models import UserListInRequest
from house_rental.commons.responses import success_response


async def get_user_list(request: UserListInRequest):
    """ 获取用户列表 """
    data = await get_user_list_logic(request)
    return success_response(data)
