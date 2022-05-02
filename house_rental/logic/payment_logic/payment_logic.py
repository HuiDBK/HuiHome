#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 支付逻辑模块 }
# @Date: 2022/05/01 0:15
from tortoise.transactions import in_transaction
from house_rental.commons import settings
from starlette.responses import RedirectResponse
from house_rental.commons.libs.payment import create_alipay
from house_rental.commons.utils import context_util
from house_rental.commons.libs import payment
from house_rental.constants.enums import PaymentSceneEnum, OrderState, RentState
from house_rental.logic.common_logic import generate_contract_content
from house_rental.managers.house_manager import HouseInfoManager
from house_rental.managers.order_manager import OrderManager
from house_rental.managers.payment_trade_manager import PaymentTradeManager
from house_rental.routers.payment.request_models import OrderPaymentIn
from house_rental.commons.exceptions.global_exception import BusinessException
from house_rental.commons.responses.response_code import ErrorCodeEnum
from house_rental.routers.payment.response_models.payment_out import OrderPaymentDataItem


async def alipay_order_callback_logic():
    """ 支付宝支付回调逻辑处理 """
    cur_request = context_util.REQUEST_CONTEXT.get()
    query_params = {k: v for k, v in cur_request.query_params.items()}

    # 校验是否是支付宝重定向过来的请求
    sign = query_params.pop('sign', None)  # 去除sign利用支付宝支付去校验

    # 由于pay_scene是在支付接口中手动设置所以要去除pay_scene去校验,
    pay_scene = query_params.pop('pay_scene', None)  # 订单支付场景

    alipay = create_alipay()
    success = alipay.verify(query_params, sign)
    if not success:
        raise BusinessException().exc_data(ErrorCodeEnum.FORBIDDEN_ERR)

    # 获取订单支付数据并保存
    order_id = query_params.get('out_trade_no')  # 订单号
    trade_no = query_params.get('trade_no')  # 订单支付流水号
    trans_amount = query_params.get('total_amount')  # 订单交易金额

    order = await OrderManager.get_by_id(order_id)
    if not order:
        raise BusinessException().exc_data(ErrorCodeEnum.ORDER_INFO_ERR)

    # 根据pay_scene更新订单状态和房源状态
    house_info = await HouseInfoManager.get_by_id(order.house_id)
    if pay_scene == PaymentSceneEnum.full_payment.value:
        # 全额支付状态改为 payed 已支付
        order.state = OrderState.payed.value
        house_info.rent_state = RentState.rent.value

    elif pay_scene == PaymentSceneEnum.balance_payment.value:
        # 支付余款状态改为 payed 已支付
        order.state = OrderState.payed.value
        house_info.rent_state = RentState.rent.value

        # 支付余款时传的订单id发生了改变要同步交易流水信息, 换成最新的订单的id
        # 此时订单表的 trade_no 还不是最新的所以可以获取之前的交易记录, 最后保存时会更新
        payment_trade = await PaymentTradeManager.get_payment_trade_by_trade_no(order.trade_no)
        payment_trade.order_id = order.id
        await payment_trade.save(update_fields=['order_id'])

    elif pay_scene == PaymentSceneEnum.deposit_payment:
        # 定金支付，状态改成 ordered 已预订
        order.state = OrderState.ordered.value
        house_info.rent_state = RentState.ordered.value

    await house_info.save(update_fields=['rent_state'])

    # 将交易信息保存到交易流水表中
    payment_trade_info = dict(
        order_id=order.id,
        user_id=order.tenant_id,  # 租客id
        trade_no=trade_no,
        scene=pay_scene,
        trans_amount=trans_amount,
    )
    await PaymentTradeManager.create(payment_trade_info)

    # 更新状态和最新的流水号
    order.trade_no = trade_no
    await order.save(update_fields=['state', 'trade_no'])

    # 重定向到前端订单界面
    return RedirectResponse(url='http://localhost:63342/house_rental/home_front/order.html')


async def alipay_order_logic(order_id, order_item: OrderPaymentIn):
    """ 订单支付逻辑 (支付宝)"""
    # 先查询订单信息
    order = await OrderManager.get_by_id(order_id)
    if not order:
        raise BusinessException().exc_data(ErrorCodeEnum.ORDER_INFO_ERR)

    if order_item.pay_scene == PaymentSceneEnum.balance_payment.value \
            and order.state == OrderState.ordered.value:
        # 已预订支付余款，由于支付宝同一个订单号不能支付多次
        # 先把创建新的订单然后把旧的订单删掉, 这样订单号就不同了但数据一样
        async with in_transaction():
            order_dict = order.to_dict()
            order_dict.pop('id', None)
            await order.delete()
            order = await OrderManager.create(order_dict)

    # 判断是否需要修改租房开始日期和结束日期
    start_date = order_item.start_date if order_item else None
    end_date = order_item.end_date if order_item else None

    order_dict = order.to_dict()
    if start_date and end_date and \
            (start_date != order_dict.get('start_date') or end_date != order_dict.get('end_date')):
        # 如果传递参数但数据库的日期不一致才更新订单信息与合同信息
        order.start_date = start_date
        order.end_date = end_date
        await order.save(update_fields=['start_date', 'end_date'])
        contract_content = await generate_contract_content(order.id)
        order.contract_content = contract_content
        await order.save(update_fields=['contract_content'])

    alipay = payment.create_alipay()

    # 计算支付金额
    # 全额 => order.pay_money
    # 定金支付 => order.bargain_money

    total_amount = 0
    if order_item.pay_scene == PaymentSceneEnum.full_payment.value:
        total_amount = order.pay_money
    elif order_item.pay_scene == PaymentSceneEnum.deposit_payment.value:
        total_amount = order.bargain_money
    elif order_item.pay_scene == PaymentSceneEnum.balance_payment.value \
            and order.state == OrderState.ordered.value:
        # 支付余款 => 支付的总金额 - 房源预定金
        total_amount = order.pay_money - order.bargain_money
    total_amount = float(total_amount)

    # 1、生成订单信息字符串（再回调时会自动返回）
    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=order.id,  # 外部订单流水号
        total_amount=total_amount,  # 支付总金额
        subject=f'{settings.SYSTEM_SIGN}:{order.id}',
        pay_flag=order_item.pay_scene,
        return_url=f'{settings.ALIPAY_RETURN_URL}?pay_scene={order_item.pay_scene}',  # 拼接一个支付标记参数用于回调更新订单状态判断
    )

    # 拼接生成支付界面登录url
    # 真实环境电脑网站支付网关：https://openapi.alipay.com/gateway.do? + order_string
    # 沙箱环境电脑网站支付网关：https://openapi.alipaydev.com/gateway.do? + order_string
    alipay_url = f'{settings.ALIPAY_URL}?{order_string}'

    return OrderPaymentDataItem(order_id=order.id, alipay_url=alipay_url)
