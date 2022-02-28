#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 用户初始化模块 }
# @Date: 2022/02/27 21:43
from fastapi import APIRouter
from .apis import user_manage

router = APIRouter()
router_v2 = APIRouter()

router.add_api_route(
    '/author',
    user_manage.get_author_info,
    methods=['get'],
    summary='获取作者信息'
)

# 用户模块 api版本v2
router_v2.add_api_route(
    '/author',
    user_manage.get_author_info_v2,
    methods=['get'],
    summary='获取作者信息v2'
)
