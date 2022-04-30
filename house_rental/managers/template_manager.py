#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 订单数据库模型管理模块 }
# @Date: 2022/04/29 11:12
from house_rental.managers import BaseManager
from house_rental.models import TemplateModel


class TemplateManager(BaseManager):
    model = TemplateModel

    @classmethod
    async def get_templates_by_ids(cls, template_ids: list):
        """ 根据订单id列表获取订单信息 """
        filter_params = dict(id__in=template_ids)
        return await cls.get_with_params(filter_params)
