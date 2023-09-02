#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 第三方服务配置 }
# @Date: 2022/04/21 11:46
import os
from house_rental.commons import settings

# 容联云短信验证码配置
RL_ACCID = '你的容联云ACCID'
RL_ACCTOKEN = '你的容联云ACCTOKEN'
RL_APPID = '你的容联云APPID'
RL_TEST_MOBILE = '你的容联云测试的手机号码'
RL_SMS_TEMPLATE_ID = '1'  # 短信模板

# 七牛云服务配置
QINIU_ACCESS_KEY = '你的七牛云ACCESS_KEY'
QINIU_SECRET_KEY = '你的七牛云SECRET_KEY'
QINIU_BUCKET_NAME = 'house-rental'
QINIU_DOMAIN = '你的七牛云DOMAIN'  # 七牛云存储域名

# 阿里支付服务配置
# 阿里支付宝沙箱应用ID
ALIPAY_APPID = '2021000116684030'

# 应用私钥文件路径
APP_PRIVATE_KEY_PATH = os.path.join(settings.BASE_DIR, 'commons/settings/keys/app_private_key.pem')

# 阿里支付公钥路径
ALIPAY_PUBLIC_KEY_PATH = os.path.join(settings.BASE_DIR, 'commons/settings/keys/alipay_public_key.pem')

# 设置阿里沙箱调试模式
ALIPAY_DEBUG = True

# 阿里支付页面地址
ALIPAY_URL = 'https://openapi.alipaydev.com/gateway.do'
ALIPAY_RETURN_URL = f'{settings.SYSTEM_DOMAIN}/api/v1/payment/alipay/callback/'
