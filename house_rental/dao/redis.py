from fastapi import FastAPI

from house_rental.commons.utils import RedisUtil


async def init_redis(_app: FastAPI, redis_conf):
    """
    初始化 Redis配置
    :param _app: FastAPI应用
    :param redis_conf: 数据库配置
    """
    await RedisUtil().init_redis_pool(redis_conf)
