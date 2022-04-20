#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 用户模块请求模型 }
# @Date: 2022/03/27 20:23
import re
from typing import Union
from house_rental import constants
from pydantic import Field, BaseModel, validator

from house_rental.constants.enums import UserRole


class UserRegisterIn(BaseModel):
    """ 用户注册入参 """
    username: str = Field(..., min_length=3, max_length=20, description='用户名')
    mobile: str = Field(..., min_length=11, description='用户手机号')
    sms_code: str = Field(..., min_length=6, max_length=6, description='手机验证码')
    password: str = Field(..., min_length=6, max_length=20, description='用户密码')
    role: UserRole = Field(UserRole.tenant.value, description='用户角色')

    @validator('mobile')
    def validate_phone(cls, field_value):
        """ 校验手机号 """
        pattern = re.compile(constants.PHONE_REGEX)
        result = pattern.match(field_value)
        if not result:
            raise ValueError(f'mobile {field_value}, 手机号格式错误')
        return field_value


class UserLoginIn(BaseModel):
    """ 用户登录入参 """
    account: str = Field(..., description='用户账号')
    password: str = Field(..., description='用户密码')


class UserProfileUpdateIn(BaseModel):
    """ 用户详情更新入参 """
    username: Union[str, None] = Field(description='用户名')
    mobile: Union[str, None] = Field(description='手机号')
    real_name: Union[str, None] = Field(description='用户真姓名')
    avatar: Union[str, None] = Field(description='用户头像')
    mail: Union[str, None] = Field(description='电子邮件')
    id_card: Union[str, None] = Field(description='身份证号')
    gender: Union[str, None] = Field(description='性别')
    hobby: Union[str, None] = Field(description='用户爱好')
    career: Union[str, None] = Field(description='用户职业')
    id_card_front: Union[str, None] = Field(description='身份证正面')
    id_card_back: Union[str, None] = Field(description='身份证反面')
