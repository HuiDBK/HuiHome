#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 用户登录注册相关逻辑模块 }
# @Date: 2022/04/04 20:53
from house_rental.routers.user.request_models import UserRegisterIn
from house_rental.managers.user_manager import UserManager, UserProfileManager
from house_rental.commons.exceptions.global_exception import BusinessException
from house_rental.commons.responses.response_code import ErrorCodeEnum
from house_rental.routers.user.response_models.user_out import UserRegisterOut
from house_rental.commons.utils.redis_util import RedisUtil, RedisKey


async def verify_user_register_info(user_item: UserRegisterIn):
    """ 校验用户注册信息 """
    # 校验短信验证码
    sms_code_cache_info = RedisKey.mobile_sms_code(user_item.mobile)
    sms_code = await RedisUtil().get_with_cache_info(sms_code_cache_info)

    # 校验用户名是否存在
    filter_params = dict(username=user_item.username)
    result = await UserManager.filter_existed(filter_params)
    if result:
        raise BusinessException(ErrorCodeEnum.USER_ERR.code, ErrorCodeEnum.USER_ERR.msg)

    # 校验手机号是否存在
    filter_params = dict(mobile=user_item.mobile)
    result = await UserManager.filter_existed(filter_params)
    if result:
        raise BusinessException(ErrorCodeEnum.USER_ERR.code, ErrorCodeEnum.USER_ERR.msg)


async def user_register_logic(user_item: UserRegisterIn):
    """ 用户注册逻辑 """
    print(user_item.dict())
    filter_params = dict(mobile=user_item.mobile)
    user = await UserManager.filter_first(filter_params)
    return user.to_dict()
    await verify_user_register_info(user_item)

    # 创建注册用户
    user = await UserManager.register(user_item.dict())
    user_profile_item = dict(
        id=user.id,
        mobile=user.mobile,
        state=user.state
    )
    print(user_profile_item)
    await UserProfileManager.create(user_profile_item)
    return user
