#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 系统配置模块 }
# @Date: 2022/04/05 23:00
from .db_config import MYSQL_CONFIG
from .db_config import REDIS_CONFIG
from .third_party_config import QINIU_ACCESS_KEY
from .third_party_config import QINIU_SECRET_KEY
from .third_party_config import QINIU_BUCKET_NAME
from .third_party_config import QINIU_DOMAIN

JWT_SECRET = 'NmUzODk2ZGUtYmZjYy0xMWVjLWI5YTctZjQzMGI5YTUwMzQ2aHVp'
JWT_EXPIRY_HOURS = 2
JWT_REFRESH_EXPIRY_DAYS = 14

# 容联云短信验证码配置
accId = '8a216da87ba59937017c1804686a1bf4'
accToken = '311e282f76914d1ab9f66dd314659efc'
appId = '8a216da87ba59937017c1804694f1bfa'
test_mobile = '13033221752'
sms_template_id = '1'  # 短信模板
sms_code_ttl = 5  # 短信验证码有效时间 单位/分钟

# 不需要登录验证的接口
API_URL_WHITE_LIST = [
    '/api/v1/user/login',
    '/api/v1/user/register',
    '/api/v1/user/mobile',
]
