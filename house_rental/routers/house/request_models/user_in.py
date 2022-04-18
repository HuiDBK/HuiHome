#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 用户模块请求模型 }
# @Date: 2022/03/27 20:23
import re
from house_rental import constants
from pydantic import Field, BaseModel, validator

from house_rental.constants.enums import UserRole


class UserRegisterIn(BaseModel):
    """ 用户注册入参 """
    username: str = Field(..., description='用户名')
    phone: str = Field(..., min_length=11, description='用户手机号')
    user_password: str = Field(..., min_length=6, max_length=20, description='用户密码')
    role: UserRole = Field(UserRole.tenant.value, description='用户角色')

    @validator('phone')
    def validate_phone(cls, field_value):
        """ 校验手机号 """
        pattern = re.compile(constants.PHONE_REGEX)
        result = pattern.match(field_value)
        if not result:
            raise ValueError(f'phone {field_value}, 手机号格式错误')
        return field_value
