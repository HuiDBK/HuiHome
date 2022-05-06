#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 项目路由模块 }
# @Date: 2022/02/27 21:37
from fastapi import APIRouter
from house_rental.routers import (
    user, house, admin, order, payment, common
)

api_router = APIRouter()

# 用户模块路由
api_router.include_router(user.router, prefix='/v1/user', tags=['用户模块'])
api_router.include_router(house.router, prefix='/v1/house', tags=['房源模块'])
api_router.include_router(order.router, prefix='/v1/order', tags=['租房订单模块'])
api_router.include_router(payment.router, prefix='/v1/payment', tags=['支付模块'])
api_router.include_router(common.router, prefix='/v1/common', tags=['公共路由模块'])
api_router.include_router(admin.router, prefix='/v1/admin', tags=['后台管理模块'])

