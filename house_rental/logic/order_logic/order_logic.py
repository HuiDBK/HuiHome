#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 订单逻辑模块 }
# @Date: 2022/04/29 10:27
import asyncio
from datetime import date
from house_rental.commons.utils import context_util, serialize_util
from house_rental.constants.enums import OrderState
from house_rental.logic.common_logic import generate_contract_content
from house_rental.managers.house_manager import HouseDetailManager, HouseInfoManager
from house_rental.managers.order_manager import OrderManager
from house_rental.managers.user_manager import UserProfileManager
from house_rental.routers.order.request_models import OrderCreateIn
from house_rental.commons.exceptions.global_exception import BusinessException
from house_rental.commons.responses.response_code import ErrorCodeEnum
from house_rental.routers.order.response_models.order_out import UserOrderListItem, UserOrderDataItem


async def create_order_logic(user_id, order_item: OrderCreateIn):
    """ 创建租房预定订单逻辑 """
    # 判断入住和退租日期是否合理
    today = date.today()
    if order_item.start_date < today or order_item.end_date <= today \
            or order_item.start_date > order_item.end_date:
        raise BusinessException().exc_data(ErrorCodeEnum.DATE_ERR)

    # 获取房源拥有者
    house_detail = await HouseDetailManager.get_by_id(order_item.house_id)
    if not house_detail:
        raise BusinessException().exc_data(ErrorCodeEnum.NODATA_ERR)

    # 同一租客id和同房源id的订单只有在当前订单处于结束状态才可以继续创建，避免重复创建
    # 不允许的状态
    not_allow_state = set(OrderState.get_member_values()) - set(OrderState.finished.value)
    filter_params = dict(
        tenant_id=user_id,
        house_id=house_detail.id,
        state__in=not_allow_state
    )
    result = await OrderManager.filter_existed(filter_params)
    if result:
        raise BusinessException().exc_data(ErrorCodeEnum.ORDER_EXIST_ERR)

    # 计算支付总金额 => 租金 * 租金扣押比率 + 租金 * 支付比率 + 管理费
    house_info = await HouseInfoManager.get_by_id(house_detail.id)
    pay_money = house_info.rent_money * house_info.deposit_ratio + \
                house_info.rent_money * house_info.pay_ratio + \
                house_info.strata_fee

    # 押金 => 租金 * 租金扣押比率
    deposit_fee = house_info.rent_money * house_info.deposit_ratio

    # 房屋预定金
    bargain_money = house_info.bargain_money

    # 创建订单
    rental_days = (order_item.end_date - order_item.start_date).days
    order_data = dict(
        tenant_id=user_id,
        landlord_id=house_detail.house_owner,
        house_id=house_detail.id,
        start_date=order_item.start_date,
        end_date=order_item.end_date,
        rental_days=rental_days,
        pay_money=pay_money,
        bargain_money=bargain_money,
        deposit_fee=deposit_fee,
        state=OrderState.no_pay.value
    )
    order = await OrderManager.create(order_data)
    contract_content = await generate_contract_content(order.id)
    order.contract_content = contract_content
    await order.save(update_fields=['contract_content'])


async def get_user_orders_logic(user_id):
    """ 获取用户租房订单（全部） """
    user_orders = await OrderManager.get_user_orders_by_user_id(user_id)

    # 补充订单信息
    house_ids = list(set([order.house_id for order in user_orders]))  # 房屋id列表
    landlord_ids = list(set([order.landlord_id for order in user_orders]))  # 房东id列表

    house_info, user_profile, landlord_profiles = await asyncio.gather(*[
        HouseInfoManager.get_houses_by_ids(house_ids),  # 房源信息
        UserProfileManager.get_by_id(user_id),  # 用户信息
        UserProfileManager.get_users_by_ids(landlord_ids)  # 房东信息
    ])

    # 先把房源、房东信息变成大字典方便订单补
    landlord_info_dict = {item.id: item for item in landlord_profiles}
    house_info_dict = {item.id: item for item in house_info}
    user_orders = [order.to_dict() for order in user_orders]
    for user_order in user_orders:
        house_info = house_info_dict.get(user_order.get('house_id'))
        landlord_info = landlord_info_dict.get(user_order.get('landlord_id'))
        user_order['user_info'] = user_profile.to_dict()
        user_order['house_info'] = house_info.to_dict()
        user_order['landlord_info'] = landlord_info.to_dict()
    user_orders = serialize_util.obj2DataModel(data_obj=user_orders, data_model=UserOrderListItem)
    return UserOrderDataItem(user_orders=user_orders)
