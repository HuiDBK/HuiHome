#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 响应码模块 }
# @Date: 2022/04/13 23:22
from house_rental.constants.enums import BaseEnum


class ErrorCodeEnum(BaseEnum):
    """ 错误码枚举类 """

    OK = (0, 'SUCCESS')
    ERROR = (-1, 'FAILED')

    IMAGE_CODE_ERR = (4001, '图形验证码错误')
    THROTTLING_ERR = (4002, '访问过于频繁')
    NECESSARY_PARAM_ERR = (4003, '缺少必传参数')
    ACCOUNT_ERR = (4004, '账号或密码错误')
    AUTHORIZATION_ERR = (4005, '权限认证错误')
    CPWD_ERR = (4006, '密码不一致')
    MOBILE_ERR = (4007, '手机号错误')
    SMS_CODE_ERR = (4008, '短信验证码有误')
    ALLOW_ERR = (4009, '未勾选协议')
    SESSION_ERR = (4010, '用户未登录')
    REGISTER_FAILED_ERR = (4011, '注册失败')
    FACILITY_EXIST_ERR = (4012, '房屋设施已存在')
    PUBLISH_HOUSE_ERR = (4013, '发布房源失败')
    DATE_ERR = (4014, '日期错误')
    ORDER_EXIST_ERR = (4015, '订单已存在')
    ORDER_INFO_ERR = (4016, '订单信息错误')
    FORBIDDEN_ERR = (4017, '非法请求')
    REALNAME_AUTH_ERR = (4018, '实名认证错误')

    DB_ERR = (5000, '数据库错误')
    EMAIL_ERR = (5001, '邮箱错误')
    TEL_ERR = (5002, '固定电话错误')
    NODATA_ERR = (5003, '无数据')
    NEW_PWD_ERR = (5004, '新密码错误')
    OPENID_ERR = (5005, '无效的openid')
    PARAM_ERR = (5006, '参数错误')
    STOCK_ERR = (5007, '库存不足')
    SOCKET_ERR = (5008, '网络错误')
    SYSTEM_ERR = (5009, '系统错误')

    @property
    def code(self):
        """ 获取错误码 """
        return self.value[0]

    @property
    def msg(self):
        """ 获取错误码码信息 """
        return self.value[1]
