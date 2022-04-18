#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 房屋映射数据库模型模块 }
# @Date: 2022/03/13 1:03
from tortoise import fields
from house_rental.models import BaseModel
from house_rental.constants import constants


class HouseFacilityMapping(BaseModel):
    """ 房屋与房屋设施关联表 """
    id = fields.IntField(pk=True)
    house_id = fields.IntField(description='房屋id')
    facility_id = fields.IntField(description='房屋设施id')

    class Meta:
        app = constants.APP_NAME
        table = 'house_facility_mapping'


class HouseRentalMapping(BaseModel):
    """ 房屋租赁映射管理表 """
    id = fields.IntField(pk=True)
    renter_id = fields.IntField(description='租客id')
    house_id = fields.IntField(description='房屋id')
    contract_id = fields.IntField(description='合同id')

    class Meta:
        app = constants.APP_NAME
        table = 'house_rent_mapping'


class HouseAppointmentMapping(BaseModel):
    """ 房屋预定映射管理表 """
    id = fields.IntField(pk=True)
    renter_id = fields.IntField(description='租客id')
    house_id = fields.IntField(description='房屋id')
    contract_id = fields.IntField(description='合同id')

    class Meta:
        app = constants.APP_NAME
        table = 'house_rent_mapping'
