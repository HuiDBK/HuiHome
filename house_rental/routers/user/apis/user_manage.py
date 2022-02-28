#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 用户管理API模块 }
# @Date: 2022/02/27 21:48


async def get_author_info():
    """测试函数，获取作者信息"""
    author_info = {
        'name': 'hui',
        'e-mail': 'huidbk@163.com',
        'desc': '业精于勤荒于嬉, 行成于思毁于随'
    }
    return author_info


async def get_author_info_v2():
    """测试函数，获取作者信息 v2版本"""
    author_info = {
        'name': 'hui',
        'e-mail': 'huidbk@163.com',
        'version': 'api/v2',
        'desc': '业精于勤荒于嬉, 行成于思毁于随'
    }
    return author_info



