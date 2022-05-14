#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 装饰器模块 }
# @Date: 2022/04/05 23:34
import json
import threading
import hashlib
from loguru import logger
from functools import wraps
from pydantic import BaseModel

from house_rental.commons import settings
from house_rental.commons.utils import context_util
from house_rental.commons.responses import ErrorCodeEnum
from house_rental.commons.request_models import ListPageRequestModel
from house_rental.commons.responses.response_model import ListResponseDataModel
from house_rental.constants import constants
from house_rental.constants.enums import UserAuthStatus, UserRole
from house_rental.managers.user_manager import UserProfileManager
from house_rental.commons.exceptions.global_exception import (
    AuthorizationException, BusinessException
)


def synchronized(func):
    """锁装饰器"""
    func.__lock__ = threading.Lock()

    @wraps(func)
    def lock_func(*args, **kwargs):
        with func.__lock__:
            return func(*args, **kwargs)

    return lock_func


def singleton(cls_):
    """单例类装饰器"""

    class wrap_cls(cls_):
        __instance = None

        @synchronized
        def __new__(cls, *args, **kwargs):
            if cls.__instance is None:
                cls.__instance = super().__new__(cls, *args, **kwargs)
                cls.__instance.__init = False
            return cls.__instance

        @synchronized
        def __init__(self, *args, **kwargs):
            if self.__init:
                return
            super().__init__(*args, **kwargs)
            self.__init = True

    wrap_cls.__name__ = cls_.__name__
    wrap_cls.__doc__ = cls_.__doc__
    wrap_cls.__qualname__ = cls_.__qualname__
    return wrap_cls


def real_auth_required(func):
    """ 实名认证装饰器 """

    @wraps(func)
    async def warp(*args, **kwargs):
        """
        通过请求上下文的user对象来判断用户有没有实名认证
        """
        cur_request = context_util.REQUEST_CONTEXT.get()
        user = cur_request.user or None

        if not user:
            raise AuthorizationException()

        if user.role == UserRole.admin.value:
            # 管理员不需要实名认证
            return await func(*args, **kwargs)

        # 此时不同直接通过 user.auth_status 来验证
        # 应该通过 user_id 去数据库中查询最新的状态
        user_profile = await UserProfileManager.get_by_id(user.id)
        if user_profile.auth_status != UserAuthStatus.authorized.value:
            raise BusinessException().exc_data(ErrorCodeEnum.REALNAME_AUTH_ERR)

        return await func(*args, **kwargs)

    return warp


def list_page(func):
    """ 分页数据封装装饰器 """

    @wraps(func)
    async def warp(*args, **kwargs):
        """
        寻找函数参数 ListPageRequestModel 的实例 有获取 limit、offset
        所有分页请求入参都继承 ListPageRequestModel
        """

        limit, offset = None, None
        # 位置参数中寻找
        for arg in args:
            if limit is not None and offset is not None:
                break

            if isinstance(arg, ListPageRequestModel):
                limit, offset = arg.limit, arg.offset

        # 关键字参数中寻找
        for key, value in kwargs.items():
            if limit is not None and offset is not None:
                break

            if isinstance(value, ListPageRequestModel):
                # 关键字参数值是否是 ListPageRequestModel
                limit, offset = value.limit, value.offset
            elif key == 'limit':
                # 也支持关键参数 key 为 limit 和 offset的情况
                limit = value
            elif key == 'offset':
                offset = value

        if limit is None or offset is None:
            # 没有成功赋值, 则不支持
            logger.debug('不支持分页数据封装')

        # 执行函数获取分页响应的数据, 有两种情况
        # 1 返回使用了pydantic model ListResponseDataModel (尽量使用这种来返回业务数据)
        # 2 返回 total data_list (元组)
        data_obj = await func(*args, **kwargs)

        # 分页数据返回的参数都必须遵守 ListResponseDataModel
        if isinstance(data_obj, ListResponseDataModel):
            # ListResponseDataModel 处理
            data_obj.next_offset = offset + limit
            data_obj.has_more = False if data_obj.next_offset > data_obj.total else True

        elif isinstance(data_obj, tuple):
            # 元组 处理
            total = data_obj[0] if isinstance(data_obj[0], int) else data_obj[1]
            data_list = data_obj[1] if isinstance(data_obj[1], list) else data_obj[0]
            data_obj = ListResponseDataModel(
                total=total,
                data_list=data_list,
                next_offset=offset + limit,
                has_more=False if offset + limit > total else True
            )

        list_page_resp = data_obj

        return list_page_resp

    return warp


def cache_json(cache_info=None, key=None, timeout=60):
    """
    缓存装饰器 (适合缓存字符串json数据)
    :param key: 缓存的key
    :param timeout: 缓存的时间 默认60秒
    :param cache_info: 封装好的缓存信息对象 RedisCacheInfo
    :return:
    """
    if cache_info:
        # 有封装的缓存对象
        key = cache_info.key
        timeout = cache_info.timeout

    def cache_decorator(api_func):
        @wraps(api_func)
        async def warp(*args, **kwargs):
            # 1、没有设置key则根据接口函数的信息和系统密钥自动生成（尽量设置key）
            nonlocal key
            if not key:
                # 应用名:函数所在模块:函数名:函数位置参数:函数关键字参数:系统密钥 进行hash
                param_args_str = ','.join([str(arg) for arg in args])
                param_kwargs_str = ','.join(sorted([f'{k}:{v}' for k, v in kwargs.items()]))
                hash_str = f'{constants.APP_NAME}:{api_func.__module__}:{api_func.__name__}:' \
                           f'{param_args_str}:{param_kwargs_str}:{settings.SECRET}'
                has_result = hashlib.md5(hash_str.encode()).hexdigest()

                # 根据哈希结果生成key
                key = f'{constants.APP_NAME}:{api_func.__module__}:{api_func.__name__}:{has_result}'

            # 2、先查看是否有缓存
            from house_rental.commons.utils.redis_util import RedisUtil
            redis_client = await RedisUtil().get_redis_conn()
            cache_data = await redis_client.get(key)
            if cache_data:
                return json.loads(cache_data)

            # 3、执行接口函数获取结果
            api_result = await api_func(*args, **kwargs)

            # 4、设置缓存
            if isinstance(api_result, BaseModel):
                # 结果是pydantic的模型对象处理
                api_result_json = api_result.json()
            elif isinstance(api_result, dict):
                # 字典
                api_result_json = json.dumps(api_result)
            else:
                # 其他可以json序列化的
                api_result_json = json.dumps(api_result)

            await redis_client.setex(key, timeout, api_result_json)
            return api_result

        return warp

    return cache_decorator
