#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 装饰器模块 }
# @Date: 2022/04/05 23:34
import json
import threading
import hashlib
from functools import wraps
from pydantic import BaseModel
from house_rental.constants import constants


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
                           f'{param_args_str}:{param_kwargs_str}'
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
