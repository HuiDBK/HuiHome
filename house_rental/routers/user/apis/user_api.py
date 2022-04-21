#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 用户管理API模块 }
# @Date: 2022/02/27 21:48
from fastapi import Path, Form, Body, UploadFile, File
from house_rental.logic.user_logic import user_logic
from house_rental.commons.responses import success_response
from house_rental.routers.user.request_models import (
    UserRegisterIn, UserLoginIn, UserProfileUpdateIn
)


async def user_register(request: UserRegisterIn):
    """ 用户注册 """
    data = await user_logic.user_register_logic(request)
    return success_response(data)


async def user_login(request: UserLoginIn):
    """ 用户登录 """
    data = await user_logic.user_login_logic(request)
    return success_response(data)


async def user_mobile_verify(
        mobile: str = Path(..., min_length=11, max_length=11, description='手机号')
):
    """ 用户手机号重复校验 """
    data = await user_logic.user_mobile_verify_logic(mobile)
    return success_response(data)


async def username_verify(
        username: str = Path(..., min_length=3, max_length=20, description='用户名')
):
    """ 用户名重复校验 """
    data = await user_logic.username_verify_logic(username)
    return success_response(data)


async def send_sms_code(
        mobile: str = Path(..., min_length=11, max_length=11, description='手机号')
):
    """ 发送短信验证码 """
    data = await user_logic.send_sms_code_logic(mobile)
    return success_response(data)


async def user_profile(
        user_id: int = Path(..., description='用户id')
):
    """ 获取用户详情信息 """
    data = await user_logic.get_user_profile_logic(user_id)
    return success_response(data)


async def update_user_profile(
        user_id: int = Path(..., description='用户id'),
        request: UserProfileUpdateIn = Body(..., description='用户详情信息')
):
    """ 更新用户详情信息 """
    data = await user_logic.update_user_profile_logic(user_id, request)
    return success_response(data)


async def user_name_auth(
        user_id: int = Path(..., description='用户id'),
        real_name: str = Form(..., min_length=1, description='真实姓名'),
        id_card: str = Form(..., min_length=18, description='身份证号'),
        id_card_front: UploadFile = File(..., description='身份证正面'),
        id_card_back: UploadFile = File(..., description='身份证背面')
):
    """ 用户实名认证接口 """
    data = await user_logic.user_name_auth_logic(
        user_id, real_name, id_card, id_card_front, id_card_back
    )
    return success_response(data)


async def get_author_info():
    """测试函数，获取作者信息"""
    author_info = {
        'name': 'hui',
        'e-mail': 'huidbk@163.com',
        'desc': '业精于勤荒于嬉, 行成于思毁于随'
    }
    return author_info


async def get_author_info_v2():
    """测试函数，获取作者信息 v2版本"""
    author_info = {
        'name': 'hui',
        'e-mail': 'huidbk@163.com',
        'version': 'api/v2',
        'desc': '业精于勤荒于嬉, 行成于思毁于随'
    }
    return author_info
