#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 项目模板数据库模型 }
# @Date: 2022/04/30 12:33
from tortoise import fields

from house_rental.constants.enums import TemplateSceneEnum
from house_rental.models import BaseModel
from house_rental.constants import constants


class TemplateModel(BaseModel):
    """ 模板模型 """
    id = fields.IntField(pk=True, description='模板id')
    template_content = fields.TextField(description='模板内容')
    render_params = fields.JSONField(description='模板渲染参数')
    api_params = fields.JSONField(description='生成模板需要的接口参数')
    scene = fields.CharEnumField(TemplateSceneEnum, description='模板场景')
    json_extend = fields.JSONField(description='扩展字段')

    class Meta:
        app = constants.APP_NAME
        table = 'template'
