#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 用户模块请求模型 }
# @Date: 2022/03/27 20:23
import re
from typing import Union
from house_rental import constants
from pydantic import Field, BaseModel, validator
from fastapi import File, UploadFile, Form

from house_rental.constants.enums import UserRole, UserAuthStatus


class UserRegisterIn(BaseModel):
    """ 用户注册入参 """
    username: str = Field(..., min_length=3, max_length=20, description='用户名')
    mobile: str = Field(..., min_length=11, description='用户手机号')
    sms_code: str = Field(..., min_length=6, max_length=6, description='手机验证码')
    password: str = Field(..., min_length=6, max_length=50, description='用户密码')
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


class UserPwdChangeIn(BaseModel):
    """ 用户修改密码入参 """
    src_password: str = Field(..., min_length=6, description='原密码')
    new_password: str = Field(..., min_length=6, description='新密码')
    confirm_password: str = Field(..., min_length=6, description='确认密码')


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
    auth_status: Union[UserAuthStatus, None] = Field(description='用户实名认证状态')


class UserRealNameAuthIn(BaseModel):
    """ 用户实名认证入参 """
    user_id: int = Field(..., description='用户id')
    real_name: str = Field(..., min_length=1, description='真实姓名')
    id_card: str = Field(..., min_length=18, description='身份证号')
    id_card_front: str = Field(..., description='身份证正面')
    id_card_back: str = Field(..., description='身份证背面')
