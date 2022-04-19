#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 时间工具模块 }
# @Date: 2022/04/19 22:10
import time
from datetime import datetime, timedelta

"""
通用日期格式 YYYY-mm-dd hh:mm:ss.fff
"""
DATE_FORMAT_NORMAL = '%Y-%m-%d %H:%M:%S.%f'

DATE_FORMAT_DB = '%Y-%m-%dT%H:%M:%S'

DATE_FORMAT_YMD = '%Y-%m-%d'

DATETIME_FORMAT_NORMAL = '%Y-%m-%d %H:%M:%S'


def str_to_timestamp(str_date, _format=DATETIME_FORMAT_NORMAL):
    """ 字符串日期转时间戳 """
    try:
        return time.mktime(time.strptime(str_date[:19], _format))
    except:
        return str_date


def ts_to_datetime(timestamp):
    """ 时间戳转成datetime """
    return datetime.fromtimestamp(timestamp)


def time_to_timestamp(_time: time):
    return (_time.hour * 60 + _time.minute) * 60 + _time.second


def now_ms_timestamp():
    """ 获取当前时间戳 单位/毫秒 """
    return int(datetime.now().timestamp() * 1000)


def now_s_timestamp():
    """ 获取当前时间戳 单位/秒 """
    return int(datetime.now().timestamp())


def to_datetime_str(timestamp):
    """ 时间戳转成标准时间格式 """
    timestamp = int(timestamp)
    return datetime.fromtimestamp(timestamp).strftime(DATETIME_FORMAT_NORMAL)


def get_now_time(format_str):
    return __get_now_time(format_str)


def __get_now_time(format_str):
    return datetime.now().strftime(format_str)


def get_time():
    return time.time()


async def diff_seconds(datetime_1: datetime, datetime_2: datetime):
    diff = datetime_1 - datetime_2
    return diff.total_seconds()


async def diff_hours(datetime_1: datetime, datetime_2: datetime):
    return await diff_seconds(datetime_1, datetime_2) // 3600


async def hours_to_seconds(hours):
    return timedelta(hours=hours).total_seconds()

