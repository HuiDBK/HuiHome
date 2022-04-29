#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 订单模块入参 }
# @Date: 2022/04/29 10:30
from datetime import date

from pydantic import BaseModel, Field


class OrderCreateIn(BaseModel):
    """ 订单创建入参 """
    house_id: int = Field(description='房源id')
    start_date: date = Field(description='入住日期')
    end_date: date = Field(description='退租日期')

