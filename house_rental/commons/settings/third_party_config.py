#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 第三方服务配置 }
# @Date: 2022/04/21 11:46
import os
from house_rental.commons import settings

# 容联云短信验证码配置
RL_ACCID = '8a216da87ba59937017c1804686a1bf4'
RL_ACCTOKEN = '311e282f76914d1ab9f66dd314659efc'
RL_APPID = '8a216da87ba59937017c1804694f1bfa'
RL_TEST_MOBILE = '13033221752'
RL_SMS_TEMPLATE_ID = '1'  # 短信模板

# 七牛云服务配置
QINIU_ACCESS_KEY = 'mp7QT_CmSbh1ACJ3sZjyAnAihkC3-HtSlZO8EXz5'
QINIU_SECRET_KEY = 'zfeCWwOz2aKfrM-j1eE4j5s-Wy5ax_fqrpImMCsI'
QINIU_BUCKET_NAME = 'house-rental'
QINIU_DOMAIN = 'http://rao7r7ao3.hn-bkt.clouddn.com/'  # 七牛云存储域名

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
