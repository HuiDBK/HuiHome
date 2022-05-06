#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 项目枚举模块 }
# @Date: 2022/03/06 18:21
from enum import Enum


class BaseEnum(Enum):
    """枚举基类"""

    @classmethod
    def get_member_values(cls):
        return [item.value for item in cls._member_map_.values()]

    @classmethod
    def get_member_names(cls):
        return [name for name in cls._member_names_]


class StrEnum(str, BaseEnum):
    """字符串枚举"""
    pass


class IntEnum(int, BaseEnum):
    """整型枚举"""
    pass


class UserRole(StrEnum):
    """用户角色"""
    admin = 'admin'  # 管理员
    tenant = 'tenant'  # 租客
    landlord = 'landlord'  # 房东
    steward = 'steward'  # 管家


class UserState(StrEnum):
    """用户状态"""
    normal = 'normal'
    deleted = 'deleted'


class UserAuthStatus(StrEnum):
    """用户实名认证状态"""
    unauthorized = 'unauthorized'  # 未实名认证
    authorized = 'authorized'  # 已实名认证
    auditing = 'auditing'  # 审核中
    unapprove = 'unapprove'  # 审核未通过


class RentType(StrEnum):
    """出租类型"""
    whole = 'whole'  # 整租
    share = 'share'  # 合租

    def __str__(self):
        return self.value


class RentState(StrEnum):
    """出租状态"""
    rent = 'rent'  # 已出租
    not_rent = 'not_rent'  # 未出租
    ordered = 'ordered'  # 已预订


class OrderState(StrEnum):
    """订单状态"""
    no_pay = 'no_pay'  # 未支付
    payed = 'payed'  # 已支付
    ordered = 'ordered'  # 已支付定金、已预订
    canceled = 'canceled'  # 已取消
    finished = 'finished'  # 订单已结束（合同结束）
    deleted = 'deleted'  # 已删除


class RentTimeUnitEnum(StrEnum):
    """ 租赁时间单位枚举 """
    day = 'day'  # 日结
    month = 'month'  # 月结
    quarter = 'quarter'  # 季度结
    half_year = 'half_year'  # 半年结
    year = 'year'  # 年结


class HouseDirectionEnum(StrEnum):
    """房屋朝向"""
    north = 'north'
    south = 'south'
    east = 'east'
    west = 'west'


class HouseElevatorEnum(IntEnum):
    """ 房屋电梯情况 """
    no = 0  # 没有
    yes = 1  # 有


class HouseElevatorDemandEnum(IntEnum):
    """ 房屋电梯情况 """
    not_Required = 0  # 不需要
    required = 1  # 需要
    no_requirement = 2  # 无要求


class HouseLightingEnum(IntEnum):
    """ 房屋采光情况 """
    bad = 0  # 差
    general = 1  # 一般
    normal = 2  # 正常
    good = 3  # 良好
    excellent = 4  # 极好


class HouseType(StrEnum):
    """房屋类型"""
    department = 'department'  # 公寓
    community = 'community'  # 小区
    residential = 'residential'  # 普通住宅

    def __str__(self):
        return self.value


class HouseState(StrEnum):
    """ 房屋状态 """
    up = 'up'  # 已上架
    down = 'down'  # 已下架
    auditing = 'auditing'  # 审核中状态
    deleted = 'deleted'  # 已删除


class RedisDataType(StrEnum):
    """ Redis 数据类型 """
    STRING = 'STRING'
    LIST = 'LIST'
    HASH = 'HASH'
    SET = 'SET'
    ZSET = 'ZSET'


class RequestMethodEnum(StrEnum):
    """ 请求方法枚举 """
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'


class TemplateSceneEnum(StrEnum):
    """ 模板场景枚举 """
    electronic_contract = 'electronic_contract'  # 电子合同


class PaymentSceneEnum(StrEnum):
    """ 支付场景 """
    full_payment = 'full_payment'  # 全额支付
    deposit_payment = 'deposit_payment'  # 定金支付
    balance_payment = 'balance_payment'  # 已预订成功支付余款


class RentalDemandState(StrEnum):
    """ 租房需求状态 """
    normal = 'normal'
    deleted = 'deleted'


class SystemNoticeSceneEnum(StrEnum):
    """ 系统公告场景 """
    notice = 'notice'  # 公告
    advertising = 'advertising'  # 广告


class SystemNoticeState(StrEnum):
    """ 系统公告状态 """
    normal = 'normal'  # 正常
    deleted = 'deleted'  # 删除
