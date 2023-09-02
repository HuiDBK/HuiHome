#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 数据库配置模块 }
# @Date: 2022/04/05 23:00
from house_rental.constants import constants

# mysql配置
MYSQL_CONFIG = {
    "connections": {
        f"{constants.APP_NAME}": {
            "engine": "tortoise.backends.mysql",
            "credentials": {
                "host": "127.0.0.1",
                "port": 3306,
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
            "default_connection": f"{constants.APP_NAME}"
        }
    }
}


# redis配置
REDIS_CONFIG = {
    'default': {
        'host': '127.0.0.1',
        'port': 6379,
        'db': 0,
        'password': "",
        'minsize': 1,
        'maxsize': 5,
        'timeout': 3
    }
}
