#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 房源数据库模型管理模块 }
# @Date: 2022/04/05 23:25
from typing import List
from house_rental.constants.enums import RentType, HouseState, RentState
from house_rental.managers import BaseManager
from house_rental.models.house_model import HouseInfo, HouseDetail, FacilityInfo
from house_rental.models.house_mapping_model import HouseFacilityMapping


class HouseInfoManager(BaseManager):
    model = HouseInfo

    @classmethod
    async def get_houses_by_ids(cls, house_ids: list):
        """ 获取房源数据 """
        filter_params = dict(id__in=house_ids)
        return await cls.get_with_params(filter_params)

    @classmethod
    async def get_recent_house(cls, rent_type: RentType, city: str = None, limit: int = 6):
        """
        根据租赁类型和所在城市获取最近已上架未出租的房源信息
        默认返回六条
        """

        filter_params = dict(
            rent_type=rent_type,
            city__icontains=city,
            state=HouseState.up.value,
            rent_state=RentState.not_rent.value
        )
        if not city:
            filter_params.pop('city', None)

        return await cls.model.filter(**filter_params).order_by('publish_time').limit(limit)


class HouseDetailManager(BaseManager):
    model = HouseDetail

    @classmethod
    async def get_houses_by_ids(cls, user_ids: list):
        """ 获取房源数据 """
        filter_params = dict(id__in=user_ids)
        return await cls.get_with_params(filter_params)


class HouseFacilityManager(BaseManager):
    model = FacilityInfo

    @classmethod
    async def get_all_facility_info(cls):
        """ 获取所有的房屋设施 """
        return await cls.model.all()

    @classmethod
    async def get_facility_info_by_ids(cls, facility_ids: list):
        """ 根据设施id列表获取设施信息 """
        filter_params = dict(id__in=facility_ids)
        return await cls.get_with_params(filter_params)

    @classmethod
    async def get_facility_by_house_id(cls, house_id: int):
        """ 根据房屋id获取房源设施数据 """
        house_facility_ids = await HouseFacilityMapping.filter(house_id=house_id).values_list('facility_id', flat=True)
        return await cls.get_facility_info_by_ids(house_facility_ids)

    @classmethod
    async def set_house_facility(cls, house_id, house_facility_ids):
        """ 设置房源设施 """
        house_facility_mappings = [
            HouseFacilityMapping(house_id=house_id, facility_id=facility_id)
            for facility_id in house_facility_ids
        ]
        return await HouseFacilityMapping.bulk_create(objects=house_facility_mappings)
