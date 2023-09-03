#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 系统配置模块 }
# @Date: 2022/04/05 23:00
import os

# 系统个签
SYSTEM_SIGN = 'HuiHome'

# 后端系统域名
# SYSTEM_DOMAIN = 'http://huidbk.cn:8080'
SYSTEM_DOMAIN = 'http://127.0.0.1:8080'

# 前端域名
FRONT_DOMAIN = 'http://localhost:6868'
# FRONT_DOMAIN = 'http://huidbk.cn:6868'

# 项目基准路径（house_rental/house_rental）
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 项目静态目录（演示可以用）
STATIC_FILE_DIR = os.path.join(os.path.dirname(BASE_DIR), 'home_front/')

# 前端订单界面
FRONT_ORDER_URL = f'{FRONT_DOMAIN}/order.html'

# 系统密钥
SECRET = 'NmUzODk2ZGUtYmZjYy0xMWVjLWI5YTctZjQzMGI5YTUwMzQ2aHVp'

JWT_SECRET = 'NmUzODk2ZGUtYmZjYy0xMWVjLWI5YTctZjQzMGI5YTUwMzQ2aHVp'
JWT_EXPIRY_HOURS = 2
JWT_REFRESH_EXPIRY_DAYS = 14

# 不需要登录验证的接口
API_URL_WHITE_LIST = [
    '/docs',
    '/static',
    '/favicon.ico',
    '/openapi.json',
    '/api/v1/user/author',
    '/api/v1/user/login',
    '/api/v1/common/areas',
    '/api/v1/house/home_houses',
    '/api/v1/user/register',
    '/api/v1/user/verify/mobile',
    '/api/v1/user/verify/username',
    '/api/v1/payment/alipay/callback',
]

# 允许的跨域请求
ALLOW_ORIGINS = [
    # "*"
    # 'http://localhost',
    'http://huidbk.cn',
    'https://huidbk.cn',
    'http://huidbk.cn:6868',
    # 'http://localhost:8080',
    'http://43.138.173.93:6868',
    'http://43.138.173.93',
    # 'http://localhost:63343',
    # 'http://localhost:63342',
    # 'http://localhost:9999',
    # 'http://3w5q328382.51vip.biz',
]

# 放到模块下面防止循环依赖
# 数据库配置
from .db_config import MYSQL_CONFIG
from .db_config import REDIS_CONFIG

# 日志配置
from .logging_config import LOGGING_CONF

# 第三方服务配置
from .third_party_config import (
    QINIU_ACCESS_KEY, QINIU_SECRET_KEY, QINIU_BUCKET_NAME, QINIU_DOMAIN,
    ALIPAY_PUBLIC_KEY_PATH, APP_PRIVATE_KEY_PATH, ALIPAY_APPID,
    ALIPAY_DEBUG, ALIPAY_URL, ALIPAY_RETURN_URL,
    RL_ACCID, RL_APPID, RL_ACCTOKEN, RL_SMS_TEMPLATE_ID, RL_TEST_MOBILE
)
