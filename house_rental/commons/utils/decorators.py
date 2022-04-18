#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 装饰器模块 }
# @Date: 2022/04/05 23:34
import threading
from functools import wraps


def synchronized(func):
    """锁装饰器"""
    func.__lock__ = threading.Lock()

    @wraps(func)
    def lock_func(*args, **kwargs):
        with func.__lock__:
            return func(*args, **kwargs)

    return lock_func


def singleton(cls_):
    """单例类装饰器"""

    class wrap_cls(cls_):
        __instance = None

        @synchronized
        def __new__(cls, *args, **kwargs):
            if cls.__instance is None:
                cls.__instance = super().__new__(cls, *args, **kwargs)
                cls.__instance.__init = False
            return cls.__instance

        @synchronized
        def __init__(self, *args, **kwargs):
            if self.__init:
                return
            super().__init__(*args, **kwargs)
            self.__init = True

    wrap_cls.__name__ = cls_.__name__
    wrap_cls.__doc__ = cls_.__doc__
    wrap_cls.__qualname__ = cls_.__qualname__
    return wrap_cls
