#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 用户数据库模型模块 }
# @Date: 2022/03/06 17:41
from tortoise import fields
from house_rental.constants import constants
from house_rental.constants.enums import UserRole, UserState
from house_rental.models import BaseModel


class UserModel(BaseModel):
    """ 用户模型 """
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=30, description='用户名')
    password = fields.CharField(max_length=30, description='用户密码')
    mobile = fields.CharField(max_length=30, description='手机号')
    role = fields.CharEnumField(UserRole, description='用户角色')
    state = fields.CharEnumField(UserState, description='用户状态')
    json_extend = fields.JSONField(description='扩展字段')

    class Meta:
        app = constants.APP_NAME
        table = 'user'


class UserProfile(BaseModel):
    """ 用户详情模型 """
    id = fields.IntField(pk=True)
    real_name = fields.CharField(max_length=30, description='用户真实姓名')
    avatar = fields.CharField(max_length=30, description='用户头像')
    mail = fields.CharField(max_length=30, description='邮箱')
    mobile = fields.CharField(max_length=30, description='手机号')
    id_card = fields.CharField(max_length=30, description='身份证号')
    user_desc = fields.CharField(max_length=200, description='用户简介')
    sex = fields.CharField(max_length=30, description='用户性别')
    hobby = fields.CharField(max_length=200, description='用户爱好')
    job = fields.CharField(max_length=30, description='职业')
    state = fields.CharEnumField(UserState, description='用户状态')
    json_extend = fields.JSONField(description='扩展字段')

    class Meta:
        app = constants.APP_NAME
        table = 'user_profile'
