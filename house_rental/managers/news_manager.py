#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 区域数据库模型管理模块 }
# @Date: 2022/04/29 11:12
from house_rental.managers import BaseManager
from house_rental.models import SystemNoticeModel


class SystemNoticeManager(BaseManager):
    model = SystemNoticeModel
