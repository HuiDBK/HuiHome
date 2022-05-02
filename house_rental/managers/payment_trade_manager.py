#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 订单支付流水数据库模型管理器模块 }
# @Date: 2022/04/29 11:12
from house_rental.managers import BaseManager
from house_rental.models.payment_trade_model import PaymentTradeModel


class PaymentTradeManager(BaseManager):
    # 设置对应数据库模型
    model = PaymentTradeModel

    @classmethod
    async def get_payment_trades_by_ids(cls, payment_trade_ids: list):
        """ 根据支付流水表id列表获取支付流水信息 """
        filter_params = dict(id__in=payment_trade_ids)
        return await cls.get_with_params(filter_params)

    @classmethod
    async def get_payment_trades_by_order_id(cls, order_id: int):
        """ 根据订单id获取交易流水信息 """
        filter_params = dict(order_id=order_id)
        return await cls.get_with_params(filter_params)

    @classmethod
    async def get_payment_trade_by_trade_no(cls, trade_no: str):
        """ 根据交易流水号获取交易流水信息 """
        filter_params = dict(trade_no=trade_no)
        return await cls.filter_first(filter_params)
