#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 后台用户管理路由模块 }
# @Date: 2022/02/27 21:43
from fastapi import APIRouter
from .apis import user_manage_api, house_manage_api
from .response_models import user_manage_out, house_manage_out

router = APIRouter()
router_v2 = APIRouter()

router.add_api_route(
    '/user/users',
    user_manage_api.get_user_list,
    methods=['post'],
    response_model=user_manage_out.UserListOut,
    summary='获取用户列表'
)

router.add_api_route(
    '/houses/{house_id}',
    house_manage_api.update_house_info,
    methods=['put'],
    response_model=house_manage_out.HouseUpdateOut,
    summary='更新房源信息'
)
