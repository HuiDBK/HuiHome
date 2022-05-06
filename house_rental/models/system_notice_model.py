#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 系统公告模型 }
# @Date: 2022/05/03 18:50
from tortoise import fields

from house_rental.constants import constants
from house_rental.constants.enums import SystemNoticeSceneEnum, SystemNoticeState
from house_rental.models import BaseOrmModel


class SystemNoticeModel(BaseOrmModel):
    """ 系统公告模型 """
    id = fields.IntField(pk=True, description='主键id')
    title = fields.CharField(max_length=255, description='标题')
    content = fields.TextField(description='内容')
    scene = fields.CharEnumField(SystemNoticeSceneEnum, description='公告场景')
    state = fields.CharEnumField(SystemNoticeState, description='公告状态')
    json_extend = fields.JSONField(default={}, null=True, description='扩展字段')

    class Meta:
        app = constants.APP_NAME
        table = 'system_notice'
