#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 数据库配置模块 }
# @Date: 2022/04/05 23:00
from house_rental.constants import constants

# mysql配置
MYSQL_CONFIG = {
    "connections": {
        "house": {
            "engine": "tortoise.backends.mysql",
            "credentials": {
                "host": "43.138.220.206",
                "port": 3307,
                "user": "root",
                "password": "123456",
                "database": f"{constants.DB_NAME}",
                "maxsize": 10
            }
        }
    },
    "apps": {
        f"{constants.APP_NAME}": {
            "models": ["house_rental.models"],
            "default_connection": "house"
        }
    }
}


# redis配置
REDIS_CONFIG = {
    'default': {
        'host': '43.138.220.206',
        # 'host': '127.0.0.1',
        'port': 6379,
        'db': 0,
        'password': '',
        'minsize': 1,
        'maxsize': 5,
        'timeout': 3
    }
}
