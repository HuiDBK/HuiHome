#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 项目数据库模型模块 }
# @Date: 2022/02/27 22:14
from datetime import datetime

from tortoise import fields, Tortoise
from tortoise.models import Model


class BaseModel(Model):
    """ 数据库模型基类 """
    create_time = fields.DatetimeField(auto_now_add=True, description='创建时间')
    update_time = fields.DatetimeField(auto_now=True, description='更新时间')

    @classmethod
    def db_conn(cls, using=None):
        if not using:
            assert cls._meta.app, f"请检查{cls._meta.db_table}表的 Meta.app 配置"
            using = cls._meta.app
        conn = Tortoise.get_connection(using)
        return conn

    def to_dict(self):
        """ 数据模型对象转字典 """
        data_dict = dict()
        base_dict = self.__dict__
        for k, v in base_dict.items():
            if str(k).startswith('_'):
                # 前缀带下划线不要
                continue
            if str(k).endswith('_time') and isinstance(v, datetime):
                # 时间字段转成时间戳
                k = k[:-4] + 'ts'
                data_dict[k] = int(v.timestamp()) if v else None
                continue

            data_dict[k] = v
        return data_dict

    class Meta:
        abstract = True


# 循环依赖, 记得放在下面
from .user_model import (
    UserBasicModel,
    UserProfileModel
)
from .house_model import (
    HouseInfo,
    HouseDetail,
    FacilityInfo
)

from .house_mapping_model import HouseFacilityMapping

from .order_model import OrderModel
from .payment_trade_model import PaymentTradeModel
from .template_model import TemplateModel
