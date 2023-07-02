#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 房屋租赁系统初始化模块 }
# @Date: 2022/02/27 20:59
from fastapi import FastAPI, Depends
from fastapi.exceptions import RequestValidationError

from house_rental import dao
from house_rental.commons import settings
from house_rental.commons.exceptions.exception_handler import (
    business_exception_handler,
    validation_exception_handler,
    global_exception_handler, authorization_exception_handler
)
from house_rental.commons.exceptions.global_exception import BusinessException, AuthorizationException
from house_rental.commons.utils.dependencies import request_context
from house_rental.middlewares import register_middlewares
from house_rental.routers import api_router

app = FastAPI(title='房屋租赁系统')

# 挂载静态文件方便演示也可单独部署前端
# app.mount("/static", StaticFiles(directory=settings.STATIC_FILE_DIR), name="static")

# 注册中间件
register_middlewares(app)


def create_global_exception_handler(_app: FastAPI):
    """ 创建全局异常处理器 """
    _app.add_exception_handler(RequestValidationError, validation_exception_handler)
    _app.add_exception_handler(AuthorizationException, authorization_exception_handler)
    _app.add_exception_handler(BusinessException, business_exception_handler)
    _app.add_exception_handler(Exception, global_exception_handler)


# 创建全局异常处理器
create_global_exception_handler(app)


@app.on_event('startup')
async def startup_event():
    """项目启动时准备环境"""

    # 配置项目日志器
    dao.init_logging(settings.LOGGING_CONF)

    # MySQL 初始化
    await dao.init_mysql(app, settings.db_config.MYSQL_CONFIG)

    # Redis 初始化
    await dao.init_redis(app, settings.db_config.REDIS_CONFIG)

    # 加载路由
    app.include_router(api_router, prefix='/api', dependencies=[
        # Depends(jwt_authentication),
        Depends(request_context),
    ])
