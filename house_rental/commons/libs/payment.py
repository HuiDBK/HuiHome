#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 第三方支付模块 }
# @Date: 2022/05/01 2:32
from alipay import AliPay

from house_rental.commons import settings


def create_alipay():
    """ 创建支付宝支付对象 """
    with open(settings.ALIPAY_PUBLIC_KEY_PATH, mode='r') as file:
        app_public_key = file.read()

    with open(settings.APP_PRIVATE_KEY_PATH, mode='r') as file:
        app_private_key = file.read()

    # 创建支付宝支付对象
    alipay = AliPay(
        appid=settings.ALIPAY_APPID,
        app_notify_url=None,
        app_private_key_string=app_private_key,
        alipay_public_key_string=app_public_key,
        sign_type="RSA2",
        debug=settings.ALIPAY_DEBUG
    )
    return alipay
