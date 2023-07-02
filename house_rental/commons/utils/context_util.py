#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 上下文工具模块 }
# @Date: 2022/04/27 15:56
import contextvars
from typing import Union

from starlette.requests import Request

from house_rental.models import UserBasicModel

# 当前请求对象上下
REQUEST_CONTEXT: contextvars.ContextVar[Union[Request, None]] = contextvars.ContextVar('request', default=None)

# 当前登陆用户对象
CUR_USER: contextvars.ContextVar[Union[UserBasicModel, None]] = contextvars.ContextVar("cur_user", default=None)
