#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 上下文工具模块 }
# @Date: 2022/04/27 15:56
import contextvars

from starlette.requests import Request

# 当前请求对象上下
REQUEST_CONTEXT: contextvars.ContextVar[Request] = contextvars.ContextVar('request', default=None)