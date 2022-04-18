#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 模块描述 }
# @Date: 2022/04/05 23:24
from typing import Union
from tortoise.models import Model
from house_rental.models import BaseModel


class BaseManager(object):
    """ 数据库模型 Manager基类 """
    model: Model = None

    @classmethod
    def model_test(cls):
        print(cls)
        print(cls.model)

    @classmethod
    async def get_with_params(cls, filter_params: dict):
        """"""
        return cls.model.filter(**filter_params).order_by('id').all()

    @classmethod
    async def filter_first(
            cls,
            filter_params: dict,
            orderings: list = None
    ) -> Union[BaseModel, None]:
        """
        首条筛选：条件筛选 + 排序规则 + 取第一个
        """
        if not orderings:
            orderings = ['id']
        return await cls.model.filter(**filter_params).order_by(*orderings).first()

    @classmethod
    async def filter_count(cls, filter_params: dict) -> int:
        """
        Count统计
        """
        return await cls.model.filter(**filter_params).count()

    @classmethod
    async def filter_existed(cls, filter_params: dict) -> bool:
        """
        存在性判断
        """
        return await cls.model.filter(**filter_params).exists()
