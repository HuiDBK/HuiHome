#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { Redis 工具模块 }
# @Date: 2022/04/17 0:13
import aioredis
from house_rental.commons import settings
from house_rental.commons.utils.decorators import singleton
from house_rental.constants import constants
from house_rental.constants.enums import RedisDataType


class RedisCacheInfo(object):
    """ 统一缓存信息类 """

    def __init__(self, key, timeout=60, data_type=RedisDataType.STRING.value):
        """
        缓存信息类初始化
        :param key: 缓存的key
        :param timeout: 缓存过期时间, 单位秒
        :param data_type: 缓存采用的数据结构 (不传并不影响，用于标记业务采用的是什么数据结构)
        """
        self.key = key
        self.timeout = timeout
        self.data_type = data_type


class RedisKey(object):
    """ Redis Key 统一管理"""

    @classmethod
    def mobile_sms_code(cls, mobile) -> RedisCacheInfo:
        """
        获取手机验证码 Redis key
        :param mobile: 手机号
        :return:
        """
        sms_code_cache_info = RedisCacheInfo(
            key=f'{constants.APP_NAME}:user:sms_code:{mobile}',
            timeout=constants.SMS_CODE_TIMEOUT
        )
        return sms_code_cache_info

    @classmethod
    def user_house_collect(cls, user_id) -> RedisCacheInfo:
        """
        获取用户房源收藏 Redis key
        :param user_id: 用户id
        :return:
        """
        house_collect_cache_info = RedisCacheInfo(
            key=f'{constants.APP_NAME}:house:{user_id}',
            timeout=constants.SMS_CODE_TIMEOUT,
            data_type=RedisDataType.LIST.value
        )
        return house_collect_cache_info


@singleton
class RedisUtil(object):
    """ Redis 工具类"""

    def __init__(self, redis_client: aioredis.Redis = None):
        """
        Redis 工具类初始化
        :param redis_client: redis客户端
        """
        self.default_conn = 'default'  # 默认连接名
        self.redis_client = redis_client

    async def init_redis_pool(self, redis_conf: dict):
        """
        初始化redis连接池
        :param redis_conf: redis配置
        """
        for conn_name, conf in redis_conf.items():
            redis_pool = await self._create_redis_pool(**conf)
            self.__setattr__(conn_name, redis_pool)
        if not self.redis_client:
            self.redis_client = await self.get_redis_conn()

    async def _create_redis_pool(self, host, port, db, password, **kwargs) -> aioredis.Redis:
        """ 创建redis连接池【显式传参】 """
        minsize = kwargs.get('minsize') or 1
        maxsize = kwargs.get('maxsize') or 5
        timeout = kwargs.get('timeout') or 3

        redis_pool = await aioredis.create_redis_pool(
            f"redis://:{password}@{host}:{port}/{db}?encoding=utf-8",
            minsize=minsize,
            maxsize=maxsize,
            timeout=timeout
        )
        return redis_pool

    async def get_redis_conn(self, conn_name=None) -> aioredis.Redis:
        """
        获取redis连接
        :param conn_name: 连接名, 不传获取默认连接
        :return: redis_pool
        """
        conn_name = conn_name or self.default_conn
        redis_setting = settings.REDIS_CONFIG.get(conn_name)
        if not redis_setting:
            return
        if hasattr(self, conn_name):
            return self.__getattribute__(conn_name)

        redis_pool = await self._create_redis_pool(**redis_setting)
        self.__setattr__(conn_name, redis_pool)
        return redis_pool

    async def set_with_cache_info(self, redis_cache_info: RedisCacheInfo, value):
        """
        根据 RedisCacheInfo 设置 Redis 缓存
        :param redis_cache_info: RedisCacheInfo缓存信息对象
        :param value: 缓存的值
        :return:
        """
        await self.redis_client.setex(redis_cache_info.key, redis_cache_info.timeout, value)

    async def get_with_cache_info(self, redis_cache_info: RedisCacheInfo):
        """
        根据 RedisCacheInfo 获取 Redis 缓存
        :param redis_cache_info: RedisCacheInfo 缓存信息对象
        :return:
        """
        cache_info = await self.redis_client.get(redis_cache_info.key)
        return cache_info

    async def del_with_cache_info(self, redis_cache_info: RedisCacheInfo):
        """
        根据 RedisCacheInfo 删除 Redis 缓存
        :param redis_cache_info: RedisCacheInfo缓存信息对象
        :return:
        """
        await self.redis_client.delete(redis_cache_info.key)
