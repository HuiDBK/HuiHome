#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 区域数据库模型 }
# @Date: 2022/04/30 12:33
from tortoise import fields

from tortoise.models import Model
from house_rental.constants import constants


class AreasModel(Model):
    """ 模板模型 """
    id = fields.IntField(pk=True, description='模板id')
    name = fields.CharField(max_length=50, description='区域名称')
    parent_id = fields.IntField(description='父级id')

    def to_dict(self):
        area_item = dict(
            id=self.id,
            name=self.name,
            parent_id=self.parent_id
        )
        return area_item

    class Meta:
        app = constants.APP_NAME
        table = 'areas'
