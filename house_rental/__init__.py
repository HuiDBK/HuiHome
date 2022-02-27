#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 房屋租赁系统初始化模块 }
# @Date: 2022/02/27 20:59
from fastapi import FastAPI
from house_rental.routers import api_router

app = FastAPI(title='房屋租赁系统')


@app.on_event('startup')
async def startup_event():
    """项目启动时准备环境"""

    # 加载路由
    app.include_router(api_router)

