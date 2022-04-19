#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 用户登录注册相关逻辑模块 }
# @Date: 2022/04/04 20:53
import re
from datetime import datetime, timedelta
from house_rental.models.user_model import UserModel
from house_rental.routers.user.response_models import TokenItem
from house_rental.routers.user.request_models import (
    UserRegisterIn,
    UserLoginIn
)
from house_rental.constants import constants
from house_rental.managers.user_manager import UserManager, UserProfileManager
from house_rental.commons.libs import sms
from house_rental.commons import settings
from house_rental.commons.utils import jwt_util
from house_rental.commons.utils import RedisUtil, RedisKey
from house_rental.commons.responses.response_code import ErrorCodeEnum
from house_rental.commons.exceptions.global_exception import BusinessException


async def username_verify_logic(username: str):
    """ 校验用户名是否存在 """
    filter_params = dict(username=username)
    result = await UserManager.filter_existed(filter_params)
    return {'verify_result': result}


async def user_mobile_verify_logic(mobile: str):
    """ 校验用户名是否存在 """
    filter_params = dict(mobile=mobile)
    result = await UserManager.filter_existed(filter_params)
    return {'verify_result': result}


async def verify_user_register_info(user_item: UserRegisterIn):
    """ 校验用户注册信息 """
    # 校验短信验证码
    sms_code_cache_info = RedisKey.mobile_sms_code(user_item.mobile)
    sms_code = await RedisUtil().get_with_cache_info(sms_code_cache_info)
    if sms_code != user_item.sms_code:
        raise BusinessException(ErrorCodeEnum.SMS_CODE_ERR.code, ErrorCodeEnum.SMS_CODE_ERR.msg)

    # 校验用户名是否存在
    filter_params = dict(username=user_item.username)
    result = await UserManager.filter_existed(filter_params)
    if result:
        raise BusinessException(ErrorCodeEnum.ACCOUNT_ERR.code, ErrorCodeEnum.ACCOUNT_ERR.msg)

    # 校验手机号是否存在
    filter_params = dict(mobile=user_item.mobile)
    result = await UserManager.filter_existed(filter_params)
    if result:
        raise BusinessException(ErrorCodeEnum.ACCOUNT_ERR.code, ErrorCodeEnum.ACCOUNT_ERR.msg)


async def generate_user_token(user: UserModel, with_refresh_token=True):
    """
    生成用户token
    :param user: 用户模型对象
    :param with_refresh_token: 是否生成用来刷新的token
    :return:
    """
    # 正常token时效2小时
    payload = dict(
        user_id=user.id,
        username=user.username,
        refresh=False
    )
    now = datetime.utcnow()
    expiry_time = now + timedelta(hours=settings.JWT_EXPIRY_HOURS)
    token = jwt_util.generate_jwt(payload, expiry_time)

    # 刷新token时效2周
    refresh_token = None
    if with_refresh_token:
        payload['refresh'] = True
        refresh_expiry_time = now + timedelta(days=settings.JWT_REFRESH_EXPIRY_DAYS)
        refresh_token = jwt_util.generate_jwt(payload, refresh_expiry_time)

    return token, refresh_token


async def user_register_logic(user_item: UserRegisterIn):
    """ 用户注册逻辑 """
    await verify_user_register_info(user_item)

    # 创建注册用户
    user = await UserManager.register(user_item.dict())
    user_profile_item = dict(
        id=user.id,
        mobile=user.mobile,
        state=user.state
    )
    await UserProfileManager.create(user_profile_item)

    # 注册成功则保存登录状态，签发token
    token, refresh_token = await generate_user_token(user)
    return {'token': token, 'refresh_token': refresh_token}


async def send_sms_code_logic(mobile: str):
    """ 发送短信验证码 """
    sms_code = sms.generate_sms_code()
    sms_code_cache_info = RedisKey.mobile_sms_code(mobile)
    await RedisUtil().set_with_cache_info(sms_code_cache_info, sms_code)
    sms_timeout = sms_code_cache_info.timeout // 60
    sms_tips = (sms_code, sms_timeout)

    # 由于短信服务申请比较严格，只能使用测试号码进行测试
    sms_resp_result = await sms.send_sms_code_message(sms_tips)
    if not sms_resp_result:
        # 发送短信验证码失败
        raise BusinessException(ErrorCodeEnum.THROTTLING_ERR.code, ErrorCodeEnum.THROTTLING_ERR.msg)
    return {'sms_result': sms_resp_result}


async def user_login_logic(account_item: UserLoginIn):
    """ 用户登录逻辑 """
    # 判断用户账号是手机号还是用户名
    pattern = re.compile(constants.PHONE_REGEX)
    result = pattern.match(account_item.account)
    filter_params = dict(password=account_item.password)
    if result:
        # 手机号
        filter_params['mobile'] = account_item.account
    else:
        # 用户名
        filter_params['username'] = account_item.account

    # 查询用户是否存在
    user = await UserManager.filter_first(filter_params)
    if not user:
        raise BusinessException().exc_data(ErrorCodeEnum.ACCOUNT_ERR)

    # 登录成功签发token, 保存用户状态
    token, refresh_token = await generate_user_token(user)
    return TokenItem(token=token, refresh_token=refresh_token).dict()
