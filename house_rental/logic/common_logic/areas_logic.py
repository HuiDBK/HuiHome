#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 区域信息逻辑模块 }
# @Date: 2022/05/04 22:57
from house_rental.commons.utils import RedisKey
from house_rental.commons.utils.decorators import cache_json
from house_rental.managers.areas_manager import AreasManager
from house_rental.routers.common.response_models.areas_out import AreasDataItem


@cache_json(RedisKey.areas())
async def get_areas_info_logic():
    """
    获取省市区数据
    :return [
        {
            id:省份id,
            name:省份名称,
            city_list:[ 省份下城市
                {
                    id: 城市id,
                    name: 城市名称,
                    parent_id: 父级id,
                    district_list: [
                        id: 区县id,
                        name: 区县名称,
                        parent_id: 父级id,
                    ]
                }
            ]
        },
        ...
    ]
    """
    area_list = list()
    area_item = dict()
    province_list = await AreasManager.get_all_province()
    for province in province_list:
        area_item['id'] = province.id
        area_item['name'] = province.name

        city_list = await AreasManager.get_areas_by_id(province.id)
        city_list = [item.to_dict() for item in city_list]
        for city in city_list:
            # 城市补充区县信息
            district_list = await AreasManager.get_areas_by_id(city.get('id'))
            city['district_list'] = [item.to_dict() for item in district_list]

        # 省份补充城市信息
        area_item['city_list'] = city_list
        area_list.append(area_item)
        area_item = {}
    return AreasDataItem(area_list=area_list)
