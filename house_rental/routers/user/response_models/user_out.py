#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 用户模块响应模型 }
# @Date: 2022/04/11 20:23
from typing import Union, List
from pydantic import Field, BaseModel
from house_rental.constants.enums import UserRole, HouseLightingEnum, HouseElevatorDemandEnum, RentalDemandState
from house_rental.commons.responses.response_model import ResponseBaseModel, ListResponseDataModel, ListResponseModel


class UserItem(BaseModel):
    """ 用户数据模型 """
    id: int = Field(description='用户id')
    username: str = Field(description='用户名')
    mobile: str = Field(description='用户手机号')
    role: UserRole = Field(description='用户角色')


class TokenItem(BaseModel):
    """ token数据模型 """
    token: str = Field(description='token信息')
    refresh_token: Union[str, None] = Field(description='刷新后的token')


class UserPwdChangeOut(ResponseBaseModel):
    """ 用户密码更改出参 """
    data: TokenItem


class VerifyItem(BaseModel):
    """ 数据校验模型 """
    verify_result: bool = Field(description='校验结果')


class UserRegisterOut(ResponseBaseModel):
    """ 用户注册出参 """
    data: TokenItem = Field(description='用户token')


class UserLoginOut(UserRegisterOut):
    """ 用户登录出参 """


class UserMobileVerifyOut(ResponseBaseModel):
    """ 用户手机号校验出参 """
    data: VerifyItem = Field(description='校验结果')


class UsernameVerifyOut(ResponseBaseModel):
    """ 用户名校验出参 """
    data: VerifyItem = Field(description='校验结果')


class UserProfileItem(BaseModel):
    """ 用户详情信息 """
    user_id: str = Field(description='用户id')
    username: str = Field(description='用户名')
    mobile: str = Field(description='手机号')
    role: str = Field(description='用户角色')
    state: str = Field(description='用户状态')
    auth_status: str = Field(description='实名认证状态')
    auth_apply_ts: Union[int, None] = Field(description='实名认证申请时间（时间戳）')
    real_name: Union[str, None] = Field(description='用户真姓名')
    avatar: Union[str, None] = Field(description='用户头像')
    mail: Union[str, None] = Field(description='电子邮件')
    id_card: Union[str, None] = Field(description='身份证号')
    gender: Union[str, None] = Field(description='性别')
    hobby: Union[str, None] = Field(description='用户爱好')
    career: Union[str, None] = Field(description='用户职业')
    id_card_front: Union[str, None] = Field(description='身份证正面')
    id_card_back: Union[str, None] = Field(description='身份证反面')
    create_ts: Union[int, None] = Field(description='用户创建时间（时间戳）')


class UserProfileOut(ResponseBaseModel):
    """ 用户详情信息出参 """
    data: UserProfileItem


class UserRealNameAuthItem(BaseModel):
    """ 用户实名认证数据 """
    user_id: str = Field(description='用户id')
    state: str = Field(description='用户状态')
    real_name: Union[str, None] = Field(description='用户真姓名')
    id_card: Union[str, None] = Field(description='身份证号')
    auth_status: str = Field(description='实名认证状态')
    id_card_front: Union[str, None] = Field(description='身份证正面')
    id_card_back: Union[str, None] = Field(description='身份证反面')


class UserRealNameAuthOut(ResponseBaseModel):
    """ 用户实名认证出参 """
    data: UserRealNameAuthItem


class RentalDemandListItem(BaseModel):
    """ 租房需求列表项数据 """
    id: int = Field(description='主键id')
    user_id: int = Field(description='用户id')
    demand_title: str = Field(description='租房需求标题')
    city: str = Field(description='期望城市')
    rent_type_list: Union[List[str]] = Field(default=[], description='租赁类型')
    house_type_list: Union[List[str]] = Field(default=[], description='房源类型')
    house_facilities: Union[List[int]] = Field(default=[], description='房源设施要求')
    min_money_budget: float = Field(description='最低金额预算')
    max_money_budget: float = Field(description='最高金额预算')
    lighting: HouseLightingEnum = Field(default=None, null=True, description='采光')
    floors: Union[List[int]] = Field(default=[], description='房屋楼层要求')
    elevator: HouseElevatorDemandEnum = Field(default=None, description='电梯要求')
    commuting_time: Union[int, None] = Field(description='通勤时间')
    company_address: Union[str, None] = Field(description='公司地址')
    desired_residence_area: Union[str, None] = Field(description='期望居住地区')
    state: RentalDemandState = Field(default=RentalDemandState.normal, description='租房需求状态')
    extend_content: Union[str, None] = Field(description='租房其他需求')
    create_ts: Union[float, None] = Field(description='创建时间')


class RentalDemandListDataItem(ListResponseDataModel):
    """ 租房需求列表数据 """
    data_list: List[RentalDemandListItem] = Field(description='租房需求列表数据')


class RentalDemandListOut(ListResponseModel):
    """ 租房需求列表出参 """
    data: RentalDemandListDataItem


class RentalDemandDetailDataItem(RentalDemandListItem):
    """ 租房需求详情数据 """
    user_info: UserItem = Field(description='用户信息')


class RentalDemandDetailOut(ListResponseModel):
    """ 租房需求详情出参 """
    data: RentalDemandDetailDataItem
