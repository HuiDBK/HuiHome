#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 用户模块请求模型 }
# @Date: 2022/03/27 20:23
import re
from typing import Union, Optional, List
from house_rental import constants
from pydantic import Field, BaseModel, validator

from house_rental.commons.request_models import ListPageRequestModel
from house_rental.constants.enums import (
    UserRole, UserAuthStatus, RentType, HouseType, HouseElevatorDemandEnum, HouseLightingEnum
)


class UserRegisterIn(BaseModel):
    """ 用户注册入参 """
    username: str = Field(..., min_length=3, max_length=20, description='用户名')
    mobile:   str = Field(..., min_length=11, description='用户手机号')
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
    account:  str = Field(..., description='用户账号')
    password: str = Field(..., description='用户密码')


class UserPwdChangeIn(BaseModel):
    """ 用户修改密码入参 """
    src_password:     str = Field(..., min_length=6, description='原密码')
    new_password:     str = Field(..., min_length=6, description='新密码')
    confirm_password: str = Field(..., min_length=6, description='确认密码')


class UserRentalDemandPublishIn(BaseModel):
    """ 用户租房需求发布入参 """
    # todo 全部对齐有点难调，可以想想自己写个脚本自己检测并自动调整，定义一些调整的规范就好了
    id:                     Optional[int]                     =    Field(description='主键id')
    demand_title:           str                               =    Field(..., max_length=255, description='租房需求标题')
    city:                   str                               =    Field(..., max_length=255, description='期望城市')
    min_money_budget:       float                             =    Field(description='最低金额预算')
    max_money_budget:       float                             =    Field(description='最高金额预算')
    desired_residence_area: Optional[str]                     =    Field(max_length=255, null=True, description='期望居住地区')
    traffic_info_json:      Optional[dict]                    =    Field(default={}, description='交通要求')
    house_facilities:       Optional[List[int]]               =    Field(default=[], description='房源设施要求')
    floors:                 Optional[List[int]]               =    Field(description='房屋楼层要求')

    rent_type_list:         Optional[List[RentType]]          =    Field(description='租赁类型')
    house_type_list:        Optional[List[HouseType]]         =    Field(description='房源类型')
    lighting:               Optional[HouseLightingEnum]       =    Field(description='采光要求')
    elevator:               Optional[HouseElevatorDemandEnum] =    Field(description='电梯要求')

    commuting_time:         Optional[int]                     =    Field(description='通勤时间')
    company_address:        Optional[str]                     =    Field(max_length=255, description='公司地址')
    extend_content:         Optional[str]                     =    Field(max_length=500, description='租房需求扩展内容')


class UserProfileUpdateIn(BaseModel):
    """ 用户详情更新入参 """
    username:    Union[str, None] = Field(description='用户名')
    mobile:      Union[str, None] = Field(description='手机号')
    real_name:   Union[str, None] = Field(description='用户真姓名')
    avatar:      Union[str, None] = Field(description='用户头像')
    mail:        Union[str, None] = Field(description='电子邮件')
    id_card:     Union[str, None] = Field(description='身份证号')
    gender:      Union[str, None] = Field(description='性别')
    hobby:       Union[str, None] = Field(description='用户爱好')
    career:      Union[str, None] = Field(description='用户职业')
    auth_status: Union[UserAuthStatus, None] = Field(description='用户实名认证状态')


class UserRealNameAuthIn(BaseModel):
    """ 用户实名认证入参 """
    user_id:       int = Field(..., description='用户id')
    real_name:     str = Field(..., min_length=1, description='真实姓名')
    id_card:       str = Field(..., min_length=18, description='身份证号')
    id_card_front: str = Field(..., description='身份证正面')
    id_card_back:  str = Field(..., description='身份证背面')


class RentalDemandListQuery(BaseModel):
    user_id: Optional[int] = Field(description='用户id')


class UserRentalDemandListIn(ListPageRequestModel):
    """ 用户租房列表入参 """
    query_params: Optional[RentalDemandListQuery] = Field(default={}, description='房源列表查询参数')
