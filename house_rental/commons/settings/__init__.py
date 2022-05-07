#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 系统配置模块 }
# @Date: 2022/04/05 23:00
import os

# 系统个签
SYSTEM_SIGN = 'HuiHome'

# 后端系统域名
SYSTEM_DOMAIN = 'http://127.0.0.1:8080'

# 前端域名
FRONT_DOMAIN = 'http://localhost:63342'

# 前端订单界面
FRONT_ORDER_URL = f'{FRONT_DOMAIN}/house_rental/home_front/order.html'

# 项目基准路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 系统密钥
SECRET = 'NmUzODk2ZGUtYmZjYy0xMWVjLWI5YTctZjQzMGI5YTUwMzQ2aHVp'

JWT_SECRET = 'NmUzODk2ZGUtYmZjYy0xMWVjLWI5YTctZjQzMGI5YTUwMzQ2aHVp'
JWT_EXPIRY_HOURS = 2
JWT_REFRESH_EXPIRY_DAYS = 14

# 不需要登录验证的接口
API_URL_WHITE_LIST = [
    '/docs',
    '/openapi.json',
    '/api/v1/user/login',
    '/api/v1/house/home_houses',
    '/api/v1/user/register',
    '/api/v1/user/mobile',
]

# 放到模块下面防止循环依赖
# 数据库配置
from .db_config import MYSQL_CONFIG
from .db_config import REDIS_CONFIG

# 第三方服务配置
from .third_party_config import (
    QINIU_ACCESS_KEY, QINIU_SECRET_KEY, QINIU_BUCKET_NAME, QINIU_DOMAIN,
    ALIPAY_PUBLIC_KEY_PATH, APP_PRIVATE_KEY_PATH, ALIPAY_APPID,
    ALIPAY_DEBUG, ALIPAY_URL, ALIPAY_RETURN_URL,
    RL_ACCID, RL_APPID, RL_ACCTOKEN, RL_SMS_TEMPLATE_ID, RL_TEST_MOBILE
)
