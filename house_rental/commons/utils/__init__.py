#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 项目工具模块 }
# @Date: 2022/04/05 22:57
from .redis_util import RedisUtil
from .redis_util import RedisKey
from .mask_util import MaskUtils


def add_param_if_true(params, key, value, is_check_none=True):
    """
    值不为空则添加到参数中
    :param params 要加入元素的字典
    :param key 要加入字典的key值
    :param value 要加入字典的value值
    :param is_check_none 是否只检查空值None, 默认True
            True: 不允许None, 但允许 0、False、空串、空列表、空字典等是有意义的
            False: 则不允许所有空值
    """
    if value or (is_check_none and value is not None):
        params[key] = value
