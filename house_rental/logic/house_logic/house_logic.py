#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 房源逻辑模块 }
# @Date: 2022/04/23 20:32
import json
from datetime import datetime
from typing import Union

from tortoise.transactions import in_transaction

from house_rental.commons.utils import RedisUtil, RedisKey, context_util
from house_rental.commons.exceptions.global_exception import BusinessException
from house_rental.commons.responses import ErrorCodeEnum
from house_rental.commons.utils.decorators import cache_json, list_page, real_auth_required
from house_rental.constants.enums import RentType, RequestMethodEnum
from house_rental.managers.house_manager import HouseInfoManager, HouseDetailManager, HouseFacilityManager
from house_rental.commons.utils import serialize_util, add_param_if_true
from house_rental.managers.user_manager import UserProfileManager
from house_rental.routers.house.request_models import HouseListInRequest
from house_rental.routers.house.request_models.house_in import HouseListQueryItem, PublishHouseIn, HouseFacilityAddIn
from house_rental.routers.house.response_models import HouseListItem, HomeHouseDataItem
from house_rental.routers.house.response_models.house_out import HouseListDataItem, HouseDetailDataItem, \
    HouseContactDataItem, HouseFacilitiesDataItem, HouseFacilityListItem, UserHouseCollectDataItem


# @cache_json(cache_info=RedisKey.home_houses())
async def get_home_house_list_logic(city: str):
    """
    获取首页房源列表, 最近整租、合租
    :return: 默认6整租、6合租
    """
    whole_house_list = await HouseInfoManager.get_recent_house(RentType.whole.value, city)
    share_house_list = await HouseInfoManager.get_recent_house(RentType.share.value, city)

    whole_house_list = [item.to_dict() for item in whole_house_list]
    share_house_list = [item.to_dict() for item in share_house_list]

    whole_house_list = serialize_util.obj2DataModel(data_obj=whole_house_list, data_model=HouseListItem)
    share_house_list = serialize_util.obj2DataModel(data_obj=share_house_list, data_model=HouseListItem)

    return HomeHouseDataItem(
        whole_house_list=whole_house_list,
        share_house_list=share_house_list
    )


def format_house_query_params(query_params: Union[HouseListQueryItem, dict]) -> dict:
    """ 格式化房源信息查询参数 """
    if not query_params:
        return {}

    if isinstance(query_params, HouseListQueryItem):
        query_params = query_params.dict()

    # 去除空值None
    query_params = {k: v for k, v in query_params.items() if v}

    add_param_if_true(query_params, 'id', query_params.pop('house_id', None))

    # 租金范围查询条件转换
    query_params['rent_money_range'] = [money * 100 for money in query_params.get('rent_money_range', [])]
    add_param_if_true(query_params, 'rent_money__range', query_params.pop('rent_money_range', None), False)

    # 面积
    query_params['area_range'] = [area * 100 for area in query_params.get('area_range', [])]
    add_param_if_true(query_params, 'area__range', query_params.pop('area_range', None), False)

    # 房源类型、租赁类型、状态、出租状态参数转换, 支持列表和单个查询
    list_params = ['house_type', 'rent_type', 'state', 'rent_state']
    for key in list_params:
        value = query_params.get(key)
        if isinstance(value, list):
            add_param_if_true(query_params, f'{key}__in', query_params.pop(key, None))

    # 房源标题、地址、所在城市支持模糊查询
    like_params = ['title', 'address', 'city']
    for key in like_params:
        add_param_if_true(query_params, f'{key}__icontains', query_params.pop(key, None))
    return query_params


@list_page
async def get_house_list_logic(item: HouseListInRequest):
    """ 获取房源列表 """
    query_params = format_house_query_params(item.query_params)
    total, house_data_list = await HouseInfoManager.filter_page(
        filter_params=query_params,
        orderings=item.orderings,
        offset=item.offset,
        limit=item.limit
    )
    house_data_list = [item.to_dict() for item in house_data_list]
    house_data_list = serialize_util.obj2DataModel(data_obj=house_data_list, data_model=HouseListItem)
    # return total, house_data_list
    return HouseListDataItem(total=total, data_list=house_data_list)


async def get_house_detail_logic(house_id: int):
    """ 获取房源详情逻辑 """

    # 先看redis缓存是否有
    house_detail_cache_info = RedisKey.house_detail(house_id)
    house_detail_json = await RedisUtil().get_with_cache_info(house_detail_cache_info)
    if house_detail_json:
        house_detail_info = json.loads(house_detail_json)
        return HouseDetailDataItem(**house_detail_info)

    house_info = await HouseInfoManager.get_by_id(house_id)
    house_detail = await HouseDetailManager.get_by_id(house_id)

    # 获取房源设施信息
    house_facility_list = await HouseFacilityManager.get_facility_by_house_id(house_id)
    house_facility_list = [item.to_dict() for item in house_facility_list]

    # 获取房源联系人信息 contact_id -> json_extend -> house_owner
    # 1、先看contact_id有没有被设置如果没有则走2
    # 2、先在房源详情的json_extend有没有contract_info字段的房屋联系人信息
    # 3、如果2没有则获取房屋拥有者信息
    contract_info = house_detail.json_extend.get('contact_info', {}) if house_detail.json_extend else {}
    choose_result = house_detail.contact_id or contract_info or house_detail.house_owner

    if isinstance(choose_result, int):
        # 说明是联系人id或者房源拥有者
        user_profile = await UserProfileManager.get_by_id(choose_result)
        house_contact_info = user_profile.to_dict()
    else:
        # 说明在json_extend设置了房源联系人信息
        house_contact_info = contract_info

    house_contact_info = HouseContactDataItem(**house_contact_info)

    # 房源信息组装
    house_info, house_detail = house_info.to_dict(), house_detail.to_dict()
    house_info.update(**house_detail)

    house_detail_info = HouseDetailDataItem(
        **house_info,
        house_facility_list=house_facility_list,
        house_contact_info=house_contact_info
    )

    # 设置房屋详情缓存
    await RedisUtil().set_with_cache_info(house_detail_cache_info, house_detail_info.json())
    return house_detail_info


@cache_json(RedisKey.house_facilities())
async def get_all_house_facility_logic():
    """ 获取所有的房屋设施信息 """
    house_facilities = await HouseFacilityManager.get_all_facility_info()
    house_facilities = [item.to_dict() for item in house_facilities]
    hose_facilities_info = HouseFacilitiesDataItem(house_facility_list=house_facilities)
    return hose_facilities_info


@real_auth_required
async def publish_house_logic(house_item: PublishHouseIn):
    """ 发布房源信息 """
    # 获取房源基本信息并保存
    async with in_transaction():
        # 开始事务
        try:
            house_detail, house_info = await _publish_house_logic(house_item)
        except Exception as e:
            print(e)
            raise BusinessException().exc_data(ErrorCodeEnum.PUBLISH_HOUSE_ERR)

    # 组装出参信息
    contact_info = house_detail.json_extend.get('contact_info', {}) if house_detail.json_extend else {}
    house_contact_info = contact_info or house_item.house_contact_info
    print(house_contact_info)
    house_info, house_detail = house_info.to_dict(), house_detail.to_dict()
    house_info.update(**house_detail)

    return HouseDetailDataItem(
        **house_info,
        house_contact_info=house_contact_info
    )


async def _publish_house_logic(house_item):
    """ 发布房源信息 """
    house_dict = house_item.dict()
    house_dict['publish_time'] = datetime.utcnow()
    house_info = await HouseInfoManager.create(house_dict)

    # 获取房源详情信息并保存
    house_dict['house_id'] = house_info.id
    house_detail = await HouseDetailManager.create(house_dict)

    # 获取房源设施信息并保存
    house_facility_ids = [item.facility_id for item in house_item.house_facility_list]
    await HouseFacilityManager.set_house_facility(house_info.id, house_facility_ids)

    # 获取房源联系人信息并保存, 如果没有设置, 默认设置房源拥有者为联系人
    house_contact_info = house_item.house_contact_info
    contact_id = house_contact_info.user_id if house_contact_info else house_item.house_owner
    if contact_id:
        # 有更新房源信息
        house_detail.contract_id = contact_id
    else:
        # 如果设置了联系人信息但没有用户id, 只是有联系电话和邮箱则保存到房源详情的json_extend中
        house_detail.json_extend = dict(
            contact_info=dict(
                user_id=house_contact_info.user_id,
                real_name=house_contact_info.real_name,
                mobile=house_contact_info.mobile,
                email=house_contact_info.email
            )
        )
    await house_detail.save(update_fields=['contact_id', 'json_extend'])
    return house_detail, house_info


async def add_house_facility_logic(facility_item: HouseFacilityAddIn):
    """ 添加房源设施逻辑 """
    house_facility = await HouseFacilityManager.filter_existed(dict(name=facility_item.name))
    if house_facility:
        raise BusinessException().exc_data(ErrorCodeEnum.FACILITY_EXIST_ERR)
    facility_item = facility_item.dict()
    house_facility = await HouseFacilityManager.create(facility_item)
    return HouseFacilityListItem(**house_facility.to_dict())


async def user_house_collect_logic(user_id, house_id: int):
    """ 用户房源收藏/取消逻辑 """
    cur_request = context_util.REQUEST_CONTEXT.get()
    collect_cache_info = RedisKey.user_house_collect(user_id)
    redis_client = await RedisUtil().get_redis_conn()

    if cur_request.method == RequestMethodEnum.POST.value:
        # post请求 => 用户收藏房源
        redis_client.sadd(key=collect_cache_info.key, member=house_id)
    elif cur_request.method == RequestMethodEnum.DELETE.value:
        # delete请求 => 用户取消收藏
        redis_client.srem(key=collect_cache_info.key, member=house_id)


async def get_user_house_collect_logic(user_id):
    """ 获取用户房源收藏逻辑 """
    # 先从redis获取用户收藏过的房源id
    collect_cache_info = RedisKey.user_house_collect(user_id)
    redis_client = await RedisUtil().get_redis_conn()
    user_house_collects = await redis_client.smembers(collect_cache_info.key)
    house_ids = [int(house_id) for house_id in user_house_collects]

    house_collect_list = await HouseInfoManager.get_houses_by_ids(house_ids)
    house_collect_list = serialize_util.obj2DataModel(house_collect_list, data_model=HouseListItem)
    return UserHouseCollectDataItem(user_house_collects=house_collect_list)
