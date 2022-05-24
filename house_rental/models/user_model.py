#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 用户数据库模型模块 }
# @Date: 2022/03/06 17:41
from urllib.parse import urlparse

from tortoise import fields

from house_rental.commons import settings
from house_rental.constants import constants
from house_rental.constants.enums import UserRole, UserState, UserAuthStatus, RentalDemandState, HouseLightingEnum, \
    HouseElevatorDemandEnum
from house_rental.models import BaseOrmModel


class UserBasicModel(BaseOrmModel):
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


class UserProfileModel(BaseOrmModel):
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

    def save(self, **kwargs):
        """ 重写数据库保存 """
        # 如果图片数据传的是url不是七牛云的key则截取key保存
        if self.id_card_front and (self.id_card_front.startswith('http') or self.id_card_front.startswith('https')):
            self.id_card_front = urlparse(url=self.id_card_front).path[1:]

        if self.id_card_back and (self.id_card_back.startswith('http') or self.id_card_back.startswith('https')):
            self.id_card_back = urlparse(url=self.id_card_back).path[1:]

        return super().save(**kwargs)

    def to_dict(self):
        user_profile_dict = super().to_dict()
        user_profile_dict['user_id'] = self.id

        # 图片数据添加七牛云域名
        img_fields = ['avatar', 'id_card_front', 'id_card_back']
        for key in img_fields:
            if user_profile_dict.get(key):
                user_profile_dict[key] = settings.QINIU_DOMAIN + user_profile_dict.get(key)
        return user_profile_dict


class UserRentalDemandModel(BaseOrmModel):
    """ 用户租房需求数据库模型 """
    id = fields.IntField(pk=True)
    user_id = fields.IntField(description='用户id')
    demand_title = fields.CharField(max_length=255, description='租房需求标题')
    extend_content = fields.CharField(null=True, max_length=500, description='租房需求扩展内容')
    city = fields.CharField(max_length=255, description='期望城市')
    rent_type_list = fields.CharField(default='', max_length=255, description='租赁类型')
    house_type_list = fields.CharField(default='', max_length=255, description='房源类型')
    house_facilities = fields.CharField(default='', max_length=255, description='房源设施要求')
    traffic_info_json = fields.JSONField(default={}, null=True, description='交通要求')
    min_money_budget = fields.DecimalField(max_digits=10, decimal_places=2, description='最低金额预算')
    max_money_budget = fields.DecimalField(max_digits=10, decimal_places=2, description='最高金额预算')
    lighting = fields.IntEnumField(HouseLightingEnum, null=True, description='采光')
    floors = fields.CharField(default='', max_length=255, description='房屋楼层要求')
    elevator = fields.IntEnumField(HouseElevatorDemandEnum, null=True, description='电梯要求')
    commuting_time = fields.IntField(null=True, description='通勤时间')
    company_address = fields.CharField(max_length=255, null=True, description='公司地址')
    desired_residence_area = fields.CharField(max_length=255, null=True, description='期望居住地区')
    state = fields.CharEnumField(RentalDemandState, default=RentalDemandState.normal, description='租房需求状态')
    json_extend = fields.JSONField(default={}, null=True, description='扩展字段')

    def to_dict(self):
        # 转换#拼接的字段
        trans_fields = ['rent_type_list', 'house_type_list', 'house_facilities', 'floors']
        for field in trans_fields:
            value = getattr(self, field) or None
            value = value.split("#") if value else []
            setattr(self, field, value)
        return super().to_dict()

    class Meta:
        app = constants.APP_NAME
        table = 'user_rental_demand'
