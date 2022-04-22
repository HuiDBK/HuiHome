#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 项目常量模块 }
# @Date: 2022/03/06 21:46

APP_NAME = 'house_rental'
DB_NAME = 'house_rental'

# 允许的跨域请求
ALLOW_ORIGINS = [
    'http://localhost',
    'http://localhost:8080',
    'http://localhost:63342',
    'http://localhost:9528'
]

# 手机号正则
PHONE_REGEX = r'^0?(13|14|15|17|18)[0-9]{9}$'


# Redis Key 过期时间常量 单位秒
SMS_CODE_TIMEOUT = 5 * 60
