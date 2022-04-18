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
    async def username_existed(cls, username):
        """ 校验用户名是否重复 """
        filter_params = dict(username=username)
        result = await cls.filter_existed(filter_params)
        return result

    @classmethod
    async def mobile_existed(cls, mobile):
        """ 手机号重复校验 """
        filter_params = dict(mobile=mobile)
        result = await cls.filter_existed(filter_params)
        return result


class UserProfileManager(BaseManager):

    model = UserProfile

    @classmethod
    async def create(cls, user_profile_item: dict):
        """ 创建用户详情 """
        user = await cls.model.create(**user_profile_item)
        return user



