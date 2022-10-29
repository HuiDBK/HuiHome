#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 区域数据库模型管理模块 }
# @Date: 2022/04/29 11:12
from typing import List
from house_rental.managers import BaseManager
from house_rental.models import AreasModel


class AreasManager(BaseManager):
    model = AreasModel

    @classmethod
    async def get_all_areas(cls) -> List[dict]:
        """ 获取全部的省市区信息 """
        sql = """
        SELECT
            province.id AS province_id,
            province.NAME AS province,
            city.id AS city_id,
            city.NAME AS city,
            GROUP_CONCAT( district.NAME ) AS districts 
        FROM
            areas AS district
            JOIN areas AS city ON district.parent_id = city.id
            JOIN areas AS province ON city.parent_id = province.id
        GROUP BY
            city.NAME 
        ORDER BY
            province.id
        """
        count, data_ret = await cls.execute_sql(sql)
        return data_ret

    @classmethod
    async def get_all_province(cls):
        """ 获取所有省份数据 """
        filter_params = dict(parent_id__isnull=True)
        return await cls.get_with_params(filter_params)

    @classmethod
    async def get_areas_by_id(cls, id):
        """ 根据区域id获取模该区域下的所有数据 """
        filter_params = dict(parent_id=id)
        return await cls.get_with_params(filter_params)

    @classmethod
    async def get_all_city(cls):
        """ 获取所有城市数据 """
        province_list = await cls.get_all_province()
        province_ids = [item.id for item in province_list]
        filter_params = dict(parent_id__in=province_ids)
        return await cls.get_with_params(filter_params)

    @classmethod
    async def get_all_district(cls):
        """ 获取所有区县数据 """
        city_list = await cls.get_all_city()
        city_ids = [item.id for item in city_list]
        filter_params = dict(parent_id__in=city_ids)
        return await cls.get_with_params(filter_params)
