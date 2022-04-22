#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 后台用户管理逻辑模块 }
# @Date: 2022/04/22 14:38
from house_rental.commons import settings
from house_rental.logic.common_logic import get_list_page_response_data
from house_rental.managers.user_manager import UserManager, UserProfileManager
from house_rental.routers.admin.request_models import UserListIn
from house_rental.routers.admin.response_models import UserListItem


async def get_user_list_logic(page_item: UserListIn):
    """ 获取用户列表信息 逻辑"""
    total, user_profiles = await UserProfileManager.filter_page(
        filter_params=page_item.query_params,
        orderings=page_item.orderings,
        offset=page_item.offset,
        limit=page_item.limit
    )
    user_ids = [user_profile.id for user_profile in user_profiles]
    users = await UserManager.get_users_by_ids(user_ids)

    user_profile_dict = {user_profile.id: user_profile for user_profile in user_profiles}
    user_data_list = [user.to_dict() for user in users]

    for user in user_data_list:
        # 添加用户详情数据
        user_id = user.get('id')
        user_profile = user_profile_dict.get(user_id)
        user.update(user_profile.to_dict())
        user['user_id'] = user_id

        # 把图片数据补充完整
        id_card_front = user_profile.id_card_front
        id_card_back = user_profile.id_card_front
        user['id_card_front'] = settings.QINIU_DOMAIN + id_card_front if id_card_front else None
        user['id_card_back'] = settings.QINIU_DOMAIN + id_card_back if id_card_back else None

    # 出参数据转换
    response_data = get_list_page_response_data(
        total=total,
        data_list=user_data_list,
        data_model=UserListItem,
        offset=page_item.offset, limit=page_item.limit
    )
    return response_data
