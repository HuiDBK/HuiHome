#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 用户登录注册相关逻辑模块 }
# @Date: 2022/04/04 20:53
import re

from fastapi import BackgroundTasks
from datetime import datetime, timedelta

from house_rental.commons.utils.decorators import list_page
from house_rental.constants.enums import UserAuthStatus, UserRole
from house_rental.models.user_model import UserBasicModel, UserRentalDemandModel
from house_rental.routers.user.request_models.user_in import UserRealNameAuthIn, UserRentalDemandPublishIn, \
    UserRentalDemandListIn
from house_rental.routers.user.response_models import (
    TokenItem, VerifyItem, UserProfileItem, UserRealNameAuthItem
)
from house_rental.routers.user.request_models import (
    UserRegisterIn, UserLoginIn, UserProfileUpdateIn, UserPwdChangeIn
)
from house_rental.constants import constants
from house_rental.managers.user_manager import UserBasicManager, UserProfileManager, UserRentalDemandManager
from house_rental.commons.libs import sms
from house_rental.commons import settings
from house_rental.commons.utils import jwt_util, add_param_if_true, serialize_util, context_util, MaskUtils
from house_rental.commons.utils import RedisUtil, RedisKey
from house_rental.commons.responses.response_code import ErrorCodeEnum
from house_rental.commons.exceptions.global_exception import BusinessException
from house_rental.routers.user.response_models.user_out import RentalDemandListItem, RentalDemandListDataItem, \
    RentalDemandDetailDataItem


async def username_verify_logic(username: str):
    """ 校验用户名是否存在 """
    filter_params = dict(username=username)
    result = await UserBasicManager.filter_existed(filter_params)
    return VerifyItem(verify_result=result)


async def user_mobile_verify_logic(mobile: str):
    """ 校验用户名是否存在 """
    filter_params = dict(mobile=mobile)
    result = await UserBasicManager.filter_existed(filter_params)
    return VerifyItem(verify_result=result)


async def verify_user_register_info(user_item: UserRegisterIn):
    """ 校验用户注册信息 """
    # 校验短信验证码
    sms_code_cache_info = RedisKey.mobile_sms_code(user_item.mobile)
    sms_code = await RedisUtil().get_with_cache_info(sms_code_cache_info)
    if sms_code != user_item.sms_code:
        raise BusinessException(ErrorCodeEnum.SMS_CODE_ERR.code, ErrorCodeEnum.SMS_CODE_ERR.msg)

    # 校验用户名是否存在
    filter_params = dict(username=user_item.username)
    result = await UserBasicManager.filter_existed(filter_params)
    if result:
        raise BusinessException(ErrorCodeEnum.ACCOUNT_ERR.code, ErrorCodeEnum.ACCOUNT_ERR.msg)

    # 校验手机号是否存在
    filter_params = dict(mobile=user_item.mobile)
    result = await UserBasicManager.filter_existed(filter_params)
    if result:
        raise BusinessException(ErrorCodeEnum.ACCOUNT_ERR.code, ErrorCodeEnum.ACCOUNT_ERR.msg)


async def generate_user_token(user: UserBasicModel, with_refresh_token=True):
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
        role=user.role,
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
    user = await UserBasicManager.register(user_item.dict())
    user_profile_item = dict(
        id=user.id,
        mobile=user.mobile,
        state=user.state
    )
    await UserProfileManager.create(user_profile_item)

    # 注册成功则保存登录状态，签发token
    token, refresh_token = await generate_user_token(user)
    return TokenItem(token=token, refresh_token=refresh_token)


async def send_sms_code_logic(mobile: str):
    """ 发送短信验证码 """

    sms_code_cache_info = RedisKey.mobile_sms_code(mobile)
    result = await RedisUtil().get_with_cache_info(sms_code_cache_info)
    if result:
        # 5分钟中内重复发送短信验证码不处理
        return

    sms_code = sms.generate_sms_code()
    await RedisUtil().set_with_cache_info(sms_code_cache_info, sms_code)
    sms_timeout = sms_code_cache_info.timeout // 60
    sms_tips = (sms_code, sms_timeout)

    # 由于短信服务申请比较严格，只能使用测试号码进行测试
    await sms.send_sms_code_message(sms_tips)


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
    user = await UserBasicManager.filter_first(filter_params)
    if not user:
        raise BusinessException().exc_data(ErrorCodeEnum.ACCOUNT_ERR)

    # 登录成功签发token, 保存用户状态
    token, refresh_token = await generate_user_token(user)
    return TokenItem(token=token, refresh_token=refresh_token)


async def get_user_profile_logic(user_id: int):
    """ 获取用户详情信息逻辑 """
    user = await UserBasicManager.get_by_id(user_id)
    user_profile = await UserProfileManager.get_by_id(user_id)
    user, user_profile = user.to_dict(), user_profile.to_dict()
    user_profile.update(user)
    user_profile['user_id'] = user.get('id')
    return UserProfileItem(**user_profile)


async def update_user_profile_logic(user_id: int, user_profile_item: UserProfileUpdateIn):
    """ 更新用户详情信息 """
    user = await UserBasicManager.get_by_id(user_id)
    user_profile = await UserProfileManager.get_by_id(user_id)

    # 去除空值
    user_profile_item = {k: v for k, v in user_profile_item.dict().items() if v is not None}
    user.update_from_dict(user_profile_item)
    user_profile.update_from_dict(user_profile_item)
    await user.save()
    await user_profile.save()

    # 把更新后数据返回
    user, user_profile = user.to_dict(), user_profile.to_dict()
    user_profile.update(user)
    user_profile['user_id'] = user.get('id')
    return UserProfileItem(**user_profile)


async def user_name_auth_logic(
        auth_item: UserRealNameAuthIn
):
    """ 用户实名认证逻辑 """
    user_profile = await UserProfileManager.get_by_id(auth_item.user_id)
    update_params = auth_item.dict()
    update_params['auth_apply_time'] = datetime.utcnow()
    update_params['auth_status'] = UserAuthStatus.auditing.value
    user_profile.update_from_dict(update_params)
    add_param_if_true(update_params, 'id', update_params.pop('user_id'))
    await user_profile.save(update_fields=list(update_params.keys()))
    user_profile = user_profile.to_dict()
    return UserRealNameAuthItem(**user_profile)


async def user_password_change_logic(user_id, user_pwd_item: UserPwdChangeIn):
    """ 用户修改密码逻辑 """
    filter_params = dict(id=user_id, password=user_pwd_item.src_password)
    user = await UserBasicManager.filter_first(filter_params)
    if not user:
        raise BusinessException().exc_data(ErrorCodeEnum.ACCOUNT_ERR)

    if user_pwd_item.new_password != user_pwd_item.confirm_password:
        raise BusinessException().exc_data(ErrorCodeEnum.CPWD_ERR)

    # 更新密码和token
    user.password = user_pwd_item.new_password
    await user.save(update_fields=['password'])
    token, refresh_token = await generate_user_token(user, with_refresh_token=False)
    return TokenItem(token=token, refresh_token=refresh_token)


def format_rental_demand_params(rental_demand: UserRentalDemandPublishIn):
    """ 格式化租房需求参数 """
    rental_demand_dict = {k: v for k, v in rental_demand.dict().items() if v is not None}

    # 房源类型、租赁类型、设施、楼层需求列表 每一项都拼接 # 存储字符串
    for key in ['rent_type_list', 'house_type_list', 'house_facilities', 'floors']:
        rental_demand_dict[key] = '#'.join(
            map(str, set(rental_demand_dict.get(key, [])))
        )

    return rental_demand_dict


async def publish_or_update_user_rental_demand_logic(user_id: int, rental_demand: UserRentalDemandPublishIn):
    """ 用户发布或更新租房需求 """
    rental_demand_dict = format_rental_demand_params(rental_demand)
    rental_demand_dict['user_id'] = user_id
    model_id = rental_demand_dict.get('id')
    await UserRentalDemandManager.create_or_update(rental_demand_dict, model_id)


@list_page
async def get_user_rental_demands_logic(rental_demand_item: UserRentalDemandListIn):
    """ 获取用户的租房需求列表 """
    query_params = rental_demand_item.query_params.dict() if rental_demand_item.query_params else {}
    query_params = {k: v for k, v in query_params.items()}

    total, user_rental_demands = await UserRentalDemandManager.filter_page(
        filter_params=query_params,
        orderings=rental_demand_item.orderings,
        limit=rental_demand_item.limit,
        offset=rental_demand_item.offset
    )

    user_rental_demands = serialize_util.data_to_model(data_obj=user_rental_demands, data_model=RentalDemandListItem)
    return RentalDemandListDataItem(total=total, data_list=user_rental_demands)


async def get_rental_demand_detail_logic(demand_id: int):
    """ 获取租房需求详情信息 """
    rental_demand = await UserRentalDemandManager.get_by_id(demand_id)
    # 补充用户信息
    user_basic: UserBasicModel = await UserBasicManager.get_by_id(rental_demand.user_id)

    cur_user = context_util.CUR_USER.get()
    if cur_user.role != UserRole.admin and cur_user.id != user_basic.id:
        # 非管理员且查询其他用户的租房需求对手机号进行掩码操作
        user_basic.mobile = MaskUtils.mask(origin_text=user_basic.mobile, mask_type=MaskUtils.PHONE)

    return RentalDemandDetailDataItem(
        **rental_demand.to_dict(),
        user_info=user_basic.to_dict()
    )
