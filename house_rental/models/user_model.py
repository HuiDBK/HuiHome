#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 用户数据库模型模块 }
# @Date: 2022/03/06 17:41
from tortoise import fields

from house_rental.commons import settings
from house_rental.constants import constants
from house_rental.constants.enums import UserRole, UserState, UserAuthStatus
from house_rental.models import BaseModel


class UserBasicModel(BaseModel):
    """ 用户模型 """
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=30, description='用户名')
    password = fields.CharField(max_length=30, description='用户密码')
    mobile = fields.CharField(max_length=11, description='手机号')
    role = fields.CharEnumField(UserRole, description='用户角色')
    state = fields.CharEnumField(UserState, default=UserState.normal, description='用户状态')
    json_extend = fields.JSONField(description='扩展字段')

    def to_dict(self):
        """ 重写不返回密码数据 """
        user_dict = super().to_dict()
        user_dict['user_id'] = self.id
        del user_dict['password']
        return user_dict

    class Meta:
        app = constants.APP_NAME
        table = 'user_basic'


class UserProfileModel(BaseModel):
    """ 用户详情模型 """
    id = fields.IntField(pk=True)
    real_name = fields.CharField(max_length=30, description='用户真实姓名')
    avatar = fields.CharField(max_length=30, description='用户头像')
    mobile = fields.CharField(max_length=30, description='手机号')
    email = fields.CharField(max_length=30, description='用户邮箱')
    id_card = fields.CharField(max_length=30, description='身份证号')
    user_desc = fields.CharField(max_length=200, description='用户简介')
    gender = fields.CharField(max_length=30, description='用户性别')
    hobby = fields.CharField(max_length=200, description='用户爱好')
    career = fields.CharField(max_length=30, description='职业')
    auth_status = fields.CharEnumField(UserAuthStatus, default=UserAuthStatus.unauthorized, description='实名认证状态')
    auth_apply_time = fields.DatetimeField(description='实名认证申请时间')
    state = fields.CharEnumField(UserState, description='用户状态')
    id_card_front = fields.CharField(max_length=200, description='身份证正面')
    id_card_back = fields.CharField(max_length=200, description='身份证反面')
    json_extend = fields.JSONField(description='扩展字段')

    class Meta:
        app = constants.APP_NAME
        table = 'user_profile'

    def to_dict(self):
        user_profile_dict = super().to_dict()
        user_profile_dict['user_id'] = self.id

        # 图片数据添加七牛云域名
        img_fields = ['avatar', 'id_card_front', 'id_card_back']
        for key in img_fields:
            if user_profile_dict.get(key):
                user_profile_dict[key] = settings.QINIU_DOMAIN + user_profile_dict.get(key)
        return user_profile_dict
