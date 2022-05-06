#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 区域路由API模块 }
# @Date: 2022/05/04 22:51
from house_rental.commons.responses import success_response

from house_rental.logic.common_logic import areas_logic


async def get_areas_info():
    """ 获取省市区数据 """
    data = await areas_logic.get_areas_info_logic()
    return success_response(data)
