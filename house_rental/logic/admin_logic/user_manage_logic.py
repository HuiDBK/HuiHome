#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 后台用户管理逻辑模块 }
# @Date: 2022/04/22 14:38
from typing import Union
from house_rental.commons import settings
from house_rental.commons.utils import add_param_if_true
from house_rental.logic.common_logic import get_list_page_response_data
from house_rental.managers.user_manager import UserBasicManager, UserProfileManager
from house_rental.routers.admin.request_models import UserListInRequest
from house_rental.routers.admin.request_models.user_manage_in import UserListQueryItem
from house_rental.routers.admin.response_models import UserListItem


def format_user_info_query_params(query_params: Union[UserListQueryItem, dict]) -> dict:
    """ 格式化用户信息查询参数 """
    if not query_params:
        return {}
    if isinstance(query_params, UserListQueryItem):
        query_params = query_params.dict()

    # 去除空值None
    query_params = {k: v for k, v in query_params.items() if v is not None}

    # 用户id字段转换
    add_param_if_true(query_params, 'id', query_params.pop('user_id', None))

    # 用户真实姓名支持模糊查询
    add_param_if_true(query_params, 'real_name__icontains', query_params.pop('real_name', None))

    # 用户状态和用户实名认证状态条件转换
    user_status_keys = ['state', 'auth_status']
    for key in user_status_keys:
        add_param_if_true(query_params, f'{key}__in', query_params.pop(key, None))

    return query_params


async def get_user_list_logic(page_item: UserListInRequest):
    """ 获取用户列表信息逻辑 """
    query_params = format_user_info_query_params(page_item.query_params)
    total, user_profiles = await UserProfileManager.filter_page(
        filter_params=query_params,
        or_params=dict(id=7),
        orderings=page_item.orderings,
        offset=page_item.offset,
        limit=page_item.limit
    )
    user_ids = [user_profile.id for user_profile in user_profiles]
    users = await UserBasicManager.get_users_by_ids(user_ids)

    user_profile_dict = {user_profile.id: user_profile for user_profile in user_profiles}
    user_data_list = [user.to_dict() for user in users]

    for user in user_data_list:
        # 添加用户详情数据
        user_id = user.get('id')
        user_profile = user_profile_dict.get(user_id)
        user.update(user_profile.to_dict())

    # 出参数据转换
    response_data = get_list_page_response_data(
        total=total,
        data_list=user_data_list,
        data_model=UserListItem,
        offset=page_item.offset, limit=page_item.limit
    )
    return response_data
