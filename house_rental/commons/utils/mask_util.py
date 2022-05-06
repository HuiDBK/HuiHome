#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 掩码模块 }
# @Date: 2022/04/08 16:27
import re


class MaskUtils(object):
    """ 掩码工具类 """

    # 元素掩码的格式 (匹配规则, 替换后的内容)
    # \1, \3 指的是取第几个分组数据相当于 group(1)、group(3)
    _regular_mapping = {
        'address': (r'(\w)', r'*'),  # 地址
        'name': (r'(.{1})(.{1})(.*)', r'\1*\3'),  # 名字
        'phone': (r'(\d{3})(.*)(\d{4})', r'\1****\3'),  # 电话号码
        'id_card': (r'(\d{6})(.*)(\d{4})', r'\1****\3'),  # 身份证
        'wechat_num': (r'(.{1})(.*)(.{1})', r'\1****\3'),  # 微信号
    }

    @classmethod
    def mask_address(cls, address: str):
        return cls._mask(origin_text=address, mask_type='address')

    @classmethod
    def mask_name(cls, name: str):
        return cls._mask(origin_text=name, mask_type='name')

    @classmethod
    def mask_phone(cls, phone: str):
        return cls._mask(origin_text=phone, mask_type='phone')

    @classmethod
    def mask_id_card(cls, id_card: str):
        return cls._mask(origin_text=id_card, mask_type='id_card')

    @classmethod
    def mask_wechat_num(cls, wechat_num: str):
        return cls._mask(origin_text=wechat_num, mask_type='wechat_num')

    @classmethod
    def _mask(cls, origin_text, mask_type='name'):
        """ 数据掩码 """
        rule_tuple = cls._regular_mapping.get(mask_type)
        return re.sub(*rule_tuple, str(origin_text))


def main():
    phone = '13033221752'

    phone = MaskUtils.mask_phone(phone)
    print(phone)

    name = MaskUtils.mask_name('刘民晖')
    print(name)


if __name__ == '__main__':
    main()
