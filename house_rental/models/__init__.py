#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 项目数据库模型模块 }
# @Date: 2022/02/27 22:14
from tortoise import fields
from tortoise.models import Model


class BaseModel(Model):
    """ 数据库模型基类 """
    create_time = fields.DatetimeField(auto_now_add=True, description='创建时间')
    update_time = fields.DatetimeField(auto_now=True, description='更新时间')

    def to_dict(self):
        """ 数据模型对象转字典 """
        data_dict = dict()
        base_dict = self.__dict__
        for k, v in base_dict.items():
            if str(k).startswith('_'):
                # 前缀带下划线不要
                continue
            data_dict[k] = v
        return data_dict

    class Meta:
        abstract = True


# 循环依赖, 记得放在下面
from .user_model import (
    UserModel,
    UserProfile
)
from .house_model import (
    HouseInfo,
    HouseDetail
)
