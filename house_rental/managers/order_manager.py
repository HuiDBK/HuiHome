#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 订单数据库模型管理模块 }
# @Date: 2022/04/29 11:12
from house_rental.constants.enums import OrderState, UserRole
from house_rental.managers import BaseManager
from house_rental.managers.user_manager import UserBasicManager
from house_rental.models.order_model import OrderModel


class OrderManager(BaseManager):
    # 设置对应数据库模型
    model = OrderModel

    @classmethod
    async def get_orders_by_ids(cls, order_ids: list):
        """ 根据订单id列表获取订单信息 """
        filter_params = dict(id__in=order_ids)
        return await cls.get_with_params(filter_params)

    @classmethod
    async def get_user_orders_by_user_id(cls, user_id: int):
        """ 根据用户id获取订单信息 """
        # 判断用户角色
        user = await UserBasicManager.get_by_id(user_id)
        filter_params = dict()
        if user.role == UserRole.tenant.value:
            # 租客
            filter_params['tenant_id'] = user_id
        elif user.role == UserRole.landlord.value:
            # 房东
            filter_params['landlord_id'] = user_id
        return await cls.get_with_params(filter_params)
