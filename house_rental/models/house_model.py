#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 房屋数据库模型模块 }
# @Date: 2022/03/06 20:47
from tortoise import fields

from house_rental.commons import settings
from house_rental.models import BaseModel
from house_rental.constants import constants
from house_rental.constants.enums import RentType, HouseType, RentState, HouseDirectionEnum, HouseState, \
    HouseLightingEnum, RentTimeUnitEnum


class HouseInfo(BaseModel):
    """ 房屋信息表 """
    id = fields.IntField(pk=True)
    rent_type = fields.CharEnumField(RentType, description='出租类型, 整租 合租')
    house_type = fields.CharEnumField(HouseType, description='房屋类型，小区房、公寓、自家房')
    title = fields.CharField(max_length=30, description='房屋标题')
    index_img = fields.CharField(max_length=30, description='房屋首页图片')
    house_desc = fields.TextField(max_length=200, description='房屋描述')
    city = fields.CharField(max_length=30, description='房屋所在城市')
    district = fields.CharField(max_length=30, description='区县')
    rent_state = fields.CharEnumField(RentState, description='出租状态')
    state = fields.CharEnumField(HouseState, description='房屋状态')
    rent_money = fields.IntField(description='租赁金额 (单位/分)')
    rent_time_unit = fields.CharEnumField(RentTimeUnitEnum, description='租赁时间单位，默认month（月结）')
    water_rent = fields.IntField(description='水费 (单位/分，元/100)')
    electricity_rent = fields.IntField(description='电费 (单位/分，元/100)')
    strata_fee = fields.IntField(description='管理费 (单位/分，元/100)')
    deposit_ratio = fields.IntField(description='租赁费用的押金倍数 (押几付几)')
    pay_ratio = fields.IntField(description='租赁费用的支付倍数 (押几付几)')
    bedroom_num = fields.IntField(description='卧室数量')
    living_room_num = fields.IntField(description='客厅数量')
    kitchen_num = fields.IntField(description='厨房数量')
    toilet_num = fields.IntField(description='卫生间数量')
    area = fields.IntField(description='房屋总体面积')
    json_extend = fields.JSONField(default={}, description='扩展字段')

    def to_dict(self):
        house_dict = super().to_dict()
        house_dict['house_id'] = self.id
        house_dict['index_img'] = settings.QINIU_DOMAIN + self.index_img
        return house_dict

    class Meta:
        app = constants.APP_NAME
        table = 'house_info'


class HouseDetail(BaseModel):
    """ 房屋详情表 """
    id = fields.IntField(pk=True)
    house_id = fields.IntField(description='房屋id')
    house_owner = fields.IntField(description='房房源拥有者id')
    contact_id = fields.IntField(description='联系人id')
    address = fields.CharField(max_length=200, description='房屋详细地址')
    room_num = fields.IntField(description='房间号')
    display_content = fields.JSONField(description='房屋展示内容')
    floor = fields.IntField(description='房屋所在楼层')
    max_floor = fields.IntField(description='房屋最大楼层')
    has_elevator = fields.BooleanField(description='是否有电梯')
    build_year = fields.DateField(description='建成年份')
    direction = fields.CharEnumField(HouseDirectionEnum, description='房屋朝向')
    lighting = fields.IntEnumField(HouseLightingEnum, description='房屋采光情况')
    near_traffic_json = fields.JSONField(null=True, description='附近交通信息')
    certificate_no = fields.CharField(max_length=50, description='房产证号')
    json_extend = fields.JSONField(default={}, description='扩展字段')

    class Meta:
        app = constants.APP_NAME
        table = 'house_detail'


class FacilityInfo(BaseModel):
    """ 房屋设施表 """
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=30, description='房屋设施名称')
    icon = fields.CharField(max_length=100, description='房屋设施图标')

    def to_dict(self):
        facility_dict = super().to_dict()
        facility_dict['facility_id'] = self.id
        facility_dict['icon'] = settings.QINIU_DOMAIN + self.icon
        return facility_dict

    class Meta:
        app = constants.APP_NAME
        table = 'house_facility'
