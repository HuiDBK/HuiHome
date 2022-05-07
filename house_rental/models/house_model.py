#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 房屋数据库模型模块 }
# @Date: 2022/03/06 20:47
from typing import Any
from urllib.parse import urlparse

from tortoise import fields
from tortoise.models import MODEL
from typing_extensions import Type

from house_rental.commons import settings
from house_rental.commons.utils import time_util
from house_rental.models import BaseOrmModel
from house_rental.constants import constants
from house_rental.constants.enums import RentType, HouseType, RentState, HouseDirectionEnum, HouseState, \
    HouseLightingEnum, RentTimeUnitEnum, HouseElevatorEnum


class HouseInfo(BaseOrmModel):
    """ 房屋信息表 """
    id = fields.IntField(pk=True)
    house_owner = fields.IntField(description='房屋拥有者')
    rent_type = fields.CharEnumField(RentType, description='出租类型, 整租 合租')
    house_type = fields.CharEnumField(HouseType, description='房屋类型，小区房、公寓、自家房')
    title = fields.CharField(max_length=30, description='房屋标题')
    index_img = fields.CharField(null=True, max_length=30, description='房屋首页图片')
    house_desc = fields.TextField(null=True, max_length=200, description='房屋描述')
    city = fields.CharField(max_length=30, description='房屋所在城市')
    district = fields.CharField(max_length=30, description='区县')
    address = fields.CharField(max_length=500, description='地址')
    rent_state = fields.CharEnumField(RentState, default=RentState.not_rent.value, description='出租状态')
    state = fields.CharEnumField(HouseState, default=HouseState.auditing.value, description='房屋状态')
    rent_money = fields.IntField(description='租赁金额 (单位/分)')
    bargain_money = fields.IntField(default=0, description='房屋预定金 (单位/分)')
    rent_time_unit = fields.CharEnumField(RentTimeUnitEnum, description='租赁时间单位，默认month（月结）')
    water_rent = fields.IntField(default=0, description='水费 (单位/分，元/100)')
    electricity_rent = fields.IntField(default=0, description='电费 (单位/分，元/100)')
    strata_fee = fields.IntField(default=0, description='管理费 (单位/分，元/100)')
    deposit_ratio = fields.IntField(default=0, description='租赁费用的押金倍数 (押几付几)')
    pay_ratio = fields.IntField(default=0, description='租赁费用的支付倍数 (押几付几)')
    bedroom_num = fields.IntField(description='卧室数量')
    living_room_num = fields.IntField(description='客厅数量')
    kitchen_num = fields.IntField(description='厨房数量')
    toilet_num = fields.IntField(description='卫生间数量')
    area = fields.IntField(description='房屋总体面积')
    publish_time = fields.DatetimeField(description='房源发布时间')
    json_extend = fields.JSONField(default={}, description='扩展字段')

    @classmethod
    def _init_from_db(cls: Type[MODEL], **kwargs: Any) -> MODEL:
        # 在模型从数据库初始化的时候就把金钱数据和一些浮点数都除100 再使用
        model_instance = super()._init_from_db(**kwargs)
        transition_fields = [
            'rent_money', 'bargain_money', 'water_rent', 'electricity_rent', 'strata_fee', 'area'
        ]
        for field in transition_fields:
            value = getattr(model_instance, field) / 100
            setattr(model_instance, field, value)
        return model_instance

    def to_dict(self):
        house_dict = super().to_dict()
        house_dict['house_id'] = self.id
        house_dict['index_img'] = settings.QINIU_DOMAIN + self.index_img if self.index_img else None
        return house_dict

    def save(self, **kwargs):
        """ 重写数据库保存 """
        # 如果图片数据传的是url不是七牛云的key则截取key保存
        if self.index_img.startswith('http') or self.index_img.startswith('https'):
            self.index_img = urlparse(url=self.index_img).path[1:]

        # 把金钱数据和一些浮点数都乘以100 保存到数据库
        transition_fields = [
            'rent_money', 'bargain_money', 'water_rent', 'electricity_rent', 'strata_fee', 'area'
        ]
        for field in transition_fields:
            value = getattr(self, field) * 100
            setattr(self, field, value)
        return super().save(**kwargs)

    class Meta:
        app = constants.APP_NAME
        table = 'house_info'


class HouseDetail(BaseOrmModel):
    """ 房屋详情表 """
    id = fields.IntField(pk=True)
    house_id = fields.IntField(description='房屋id')
    house_owner = fields.IntField(null=True, description='房房源拥有者id')
    contact_id = fields.IntField(description='联系人id')
    address = fields.CharField(max_length=200, description='房屋详细地址')
    room_num = fields.IntField(description='房间号')
    display_content = fields.JSONField(default={}, null=True, description='房屋展示内容')
    floor = fields.IntField(description='房屋所在楼层')
    max_floor = fields.IntField(description='房屋最大楼层')
    has_elevator = fields.IntEnumField(HouseElevatorEnum, description='是否有电梯')
    build_year = fields.CharField(max_length=20, null=True, description='建成年份')
    direction = fields.CharEnumField(HouseDirectionEnum, null=True, description='房屋朝向')
    lighting = fields.IntEnumField(HouseLightingEnum, null=True, description='房屋采光情况')
    near_traffic_json = fields.JSONField(null=True, description='附近交通信息')
    certificate_no = fields.CharField(max_length=50, null=True, description='房产证号')
    location_info = fields.JSONField(default={}, null=True, description='房源地理位置')
    json_extend = fields.JSONField(default={}, null=True, description='扩展字段')

    class Meta:
        app = constants.APP_NAME
        table = 'house_detail'

    def to_dict(self):
        house_dict = super().to_dict()
        if self.display_content:
            images = self.display_content.get('images', [])
            self.display_content['images'] = [f'{settings.QINIU_DOMAIN}{img}' for img in images]
        house_dict['display_content'] = self.display_content
        return house_dict


class FacilityInfo(BaseOrmModel):
    """ 房屋设施表 """
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=30, description='房屋设施名称')
    icon = fields.CharField(null=True, max_length=100, description='房屋设施图标')

    def to_dict(self):
        facility_dict = super().to_dict()
        facility_dict['facility_id'] = self.id
        facility_dict['icon'] = settings.QINIU_DOMAIN + self.icon if self.icon else None
        return facility_dict

    class Meta:
        app = constants.APP_NAME
        table = 'house_facility'
