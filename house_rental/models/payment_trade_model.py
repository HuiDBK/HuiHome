#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 支付交易流水数据库模型模块 }
# @Date: 2022/04/29 7:17
from tortoise import fields
from house_rental.constants import constants
from house_rental.constants.enums import PaymentSceneEnum
from house_rental.models import BaseOrmModel


class PaymentTradeModel(BaseOrmModel):
    """ 支付交易数据库模型 """
    id = fields.IntField(pk=True)
    order_id = fields.IntField(description='订单号')
    user_id = fields.IntField(description='用户id（谁的付的钱）')
    trade_no = fields.CharField(max_length=255, description='交易流水号')
    scene = fields.CharEnumField(PaymentSceneEnum, description='交易场景')
    trans_amount = fields.DecimalField(max_digits=10, decimal_places=2, description='交易金额')
    json_extend = fields.JSONField(default={}, null=True, description='扩展字段')

    class Meta:
        app = constants.APP_NAME
        table = 'payment_trade'
