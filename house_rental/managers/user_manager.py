#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 模块描述 }
# @Date: 2022/04/05 23:25
from house_rental.models.user_model import UserModel, UserProfile
from house_rental.managers import BaseManager
from house_rental.constants.enums import UserState


class UserManager(BaseManager):
    # 设置对应数据库模型
    model = UserModel

    @classmethod
    async def register(cls, user_item: dict):
        """ 用户注册 """
        user = await cls.model.create(**user_item, state=UserState.normal.value)
        return user

    @classmethod
    async def get_users_by_ids(cls, user_ids: list):
        """ 用户注册 """
        filter_params = dict(id__in=user_ids)
        return await cls.get_with_params(filter_params)


class UserProfileManager(BaseManager):

    model = UserProfile

    @classmethod
    async def create(cls, user_profile_item: dict):
        """ 创建用户详情 """
        user = await cls.model.create(**user_profile_item)
        return user

    @classmethod
    async def get_users_by_ids(cls, user_ids: list):
        """ 用户注册 """
        filter_params = dict(id__in=user_ids)
        return await cls.get_with_params(filter_params)


