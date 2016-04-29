# -*- coding: utf-8 -*-
import os
import time
import json
from itertools import chain

from models     import Order
from models     import UserCoupon
from ops.order  import OrderService
from ops.coupon import CouponService
from ops.credit import CreditService

from constants import ORDER_STATUS


def cancel_order(order_id):
    ''' 取消已支付订单 '''
    order               = OrderService.get_order_by_id(order_id)
    assert order, '订单不存在'
    count               = 0
    if order.status in [ORDER_STATUS.NEW_ORDER, ORDER_STATUS.TO_PAY]:
        where               = Order.status.in_([ORDER_STATUS.NEW_ORDER, ORDER_STATUS.TO_PAY])
        count               = OrderService.update_order_status(order_id, ORDER_STATUS.CANCEL_BEFORE_PAY, order.user_id, where)
        if count:
            if order.credit_amount:
                CreditService.modify_credit(order.user_id, -(order.credit_amount))
            if order.coupon_id:
                CouponService.update_user_coupon_status(UserCoupon.id==order.coupon_id, 0)
    elif order.status==ORDER_STATUS.PAY_SUCCESS:
        where               = Order.status==ORDER_STATUS.PAY_SUCCESS
        count               = OrderService.update_order_status(order_id, ORDER_STATUS.CANCELED, order.user_id, where)
        if count:
            if order.credit_amount:
                repayment_amount    = OrderService.order_repayment_logs_amount(order_id)
                remain_to_repayment = order.credit_amount - repayment_amount
                CreditService.modify_credit(order.user_id, -remain_to_repayment)
                CreditService.cancel_pay_logs(order_id)
            if order.coupon_id:
                CouponService.update_user_coupon_status(UserCoupon.id==order.coupon_id, 0)
