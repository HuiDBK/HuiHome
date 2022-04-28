#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 房屋租赁系统初始化模块 }
# @Date: 2022/02/27 20:59
import aioredis
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from tortoise.contrib.fastapi import register_tortoise

from house_rental import constants
from house_rental.commons import settings
from house_rental.commons.utils.dependencies import jwt_authentication, request_context
from house_rental.routers import api_router
from house_rental.commons.utils.redis_util import RedisUtil
from house_rental.middlewares.middlewares import AuthorizationMiddleware
from house_rental.commons.exceptions.exception_handler import (
    business_exception_handler,
    validation_exception_handler,
    global_exception_handler, authorization_exception_handler
)
from house_rental.commons.exceptions.global_exception import BusinessException, AuthorizationException

app = FastAPI(title='房屋租赁系统')


@app.on_event('startup')
async def startup_event():
    """项目启动时准备环境"""

    # 加载路由
    app.include_router(api_router, prefix='/api', dependencies=[Depends(request_context)])

    # 注册中间件
    await register_middlewares(app)

    # 创建全局异常处理器
    await create_global_exception_handler(app)

    # 数据库初始化
    await db_init(app)


async def create_global_exception_handler(_app: FastAPI):
    """ 创建全局异常处理器 """
    _app.add_exception_handler(RequestValidationError, validation_exception_handler)
    _app.add_exception_handler(AuthorizationException, authorization_exception_handler)
    _app.add_exception_handler(BusinessException, business_exception_handler)
    _app.add_exception_handler(Exception, global_exception_handler)


async def register_middlewares(_app: FastAPI):
    """注册中间件"""
    middleware_list = [AuthorizationMiddleware]
    for middleware in middleware_list:
        _app.add_middleware(middleware)

    # 设置跨域中间件
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=constants.ALLOW_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


async def init_mysql(_app: FastAPI, db_config: dict):
    """
    初始化MySQL
    :param _app: FastAPI应用
    :param db_config: 数据库配置
    db_config
        {
            'connections': {
                'default': {
                    'engine': 'tortoise.backends.asyncpg',
                    'credentials': {
                        'host': 'localhost',
                        'port': '5432',
                        'user': 'tortoise',
                        'password': 'qwerty123',
                        'database': 'test',
                    }
                },
            },
            'apps': {
                'models': {
                    'models': ['__main__'],             # model所在的目录
                    'default_connection': 'default',    # 对应使用的数据库连接
                }
            }
        }
    """
    [v["credentials"].setdefault("pool_recycle", 3540) for _, v in db_config["connections"].items()]
    register_tortoise(
        _app,
        config=db_config,
        generate_schemas=False,  # 如果数据库为空, 则自动生成对应数据表, 生产环境不要开
        add_exception_handlers=False,  # 生产环境不要开, 会泄露调试信息
    )


async def init_redis(_app: FastAPI, redis_conf):
    """
    初始化 Redis配置
    :param _app: FastAPI应用
    :param redis_conf: 数据库配置
    """
    await RedisUtil().init_redis_pool(redis_conf)


async def db_init(_app: FastAPI):
    """ 数据库初始化 MySQL and Redis """

    await init_mysql(_app, settings.MYSQL_CONFIG)

    await init_redis(_app, settings.REDIS_CONFIG)
