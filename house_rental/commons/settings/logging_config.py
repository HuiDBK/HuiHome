#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 项目日志配置模块 }
# @Date: 2022/05/14 15:18
import os
from house_rental.commons import settings

# 项目日志目录
LOGGING_DIR = os.path.join(os.path.dirname(settings.BASE_DIR), 'logs/')

# 项目运行时所有的日志文件
SERVER_LOG_FILE = os.path.join(LOGGING_DIR, 'server.log')

# 错误时的日志文件
ERROR_LOG_FILE = os.path.join(LOGGING_DIR, 'error.log')

# 项目日志滚动配置（日志文件超过10 MB就自动新建文件扩充）
LOGGING_ROTATION = "10 MB"

# 项目日志配置
LOGGING_CONF = {
    'server_handler': {
        'file': SERVER_LOG_FILE,
        'level': 'INFO',
        'rotation': LOGGING_ROTATION,
        'backtrace': False,
        'diagnose': False,
    },
    'error_handler': {
        'file': ERROR_LOG_FILE,
        'level': 'ERROR',
        'rotation': LOGGING_ROTATION,
        'backtrace': True,
        'diagnose': True,
    },
}
