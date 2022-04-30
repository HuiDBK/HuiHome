#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 订单数据库模型模块 }
# @Date: 2022/04/29 7:17
from tortoise import fields
from house_rental.commons.utils import time_util
from house_rental.constants import constants
from house_rental.constants.enums import OrderState
from house_rental.models import BaseModel


class OrderModel(BaseModel):
    """ 订单模型 """
    id = fields.IntField(pk=True)
    tenant_id = fields.IntField(description='租客id')
    landlord_id = fields.IntField(description='房东id')
    house_id = fields.IntField(description='房源id')
    contract_content = fields.TextField(description='合同内容')
    state = fields.CharEnumField(OrderState, description='订单状态')
    pay_money = fields.DecimalField(max_digits=10, decimal_places=2, description='支付总金额')
    deposit_fee = fields.DecimalField(max_digits=10, decimal_places=2, description='押金')
    bargain_money = fields.DecimalField(max_digits=10, decimal_places=2, description='房屋定金')
    rental_days = fields.IntField(description='租赁天数')
    start_date = fields.DateField(description='开始日期')
    end_date = fields.DateField(description='结束日期')
    json_extend = fields.JSONField(description='扩展字段')

    def to_dict(self):
        # 新增一个order_id参数返回
        order_dict = super().to_dict()
        order_dict['order_id'] = self.id
        order_dict['start_date'] = self.start_date.strftime(time_util.DATE_FORMAT_YMD)
        order_dict['end_date'] = self.end_date.strftime(time_util.DATE_FORMAT_YMD)
        return order_dict

    class Meta:
        app = constants.APP_NAME
        table = 'user_order'
