#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 模块描述 }
# @Date: 2022/04/12 17:31
from starlette.middleware.cors import CORSMiddleware

from .middlewares import AuthorizationMiddleware
from fastapi import FastAPI

from house_rental import constants


def register_middlewares(_app: FastAPI):
    """注册中间件"""
    middleware_list = [
        AuthorizationMiddleware,
        # PreventCrawlerMiddleware,
    ]
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
