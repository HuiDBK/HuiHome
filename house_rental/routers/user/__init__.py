#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 用户初始化模块 }
# @Date: 2022/02/27 21:43
from fastapi import APIRouter
from .apis import user_api
from .response_models import user_out
from house_rental.commons.responses.response_model import SuccessModel

router = APIRouter()
router_v2 = APIRouter()

router.add_api_route(
    '/author',
    user_api.get_author_info,
    methods=['get'],
    summary='获取作者信息'
)

router.add_api_route(
    '/mobile/{mobile}/verify',
    user_api.user_mobile_verify,
    response_model=user_out.UserMobileVerifyOut,
    methods=['get'],
    summary='用户手机号校验'
)

router.add_api_route(
    '/username/{username}/verify',
    user_api.username_verify,
    response_model=user_out.UsernameVerifyOut,
    methods=['get'],
    summary='用户名校验'
)

router.add_api_route(
    '/sms_code/{mobile}',
    user_api.send_sms_code,
    response_model=SuccessModel,
    methods=['get'],
    summary='发送短信验证码'
)

router.add_api_route(
    '/register',
    user_api.user_register,
    response_model=user_out.UserRegisterOut,
    methods=['post'],
    summary='用户注册'
)

router.add_api_route(
    '/register',
    user_api.user_register,
    response_model=user_out.UserRegisterOut,
    methods=['post'],
    summary='用户注册'
)

router.add_api_route(
    '/login',
    user_api.user_login,
    response_model=user_out.UserLoginOut,
    methods=['post'],
    summary='用户登录'
)

# 用户模块 api版本v2
router_v2.add_api_route(
    '/author',
    user_api.get_author_info_v2,
    methods=['get'],
    summary='获取作者信息v2'
)
