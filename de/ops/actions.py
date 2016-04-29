# -*- coding: utf-8 -*-

from sqlalchemy         import and_

from models             import db
from models             import Item
from models             import Hospital
from models             import ItemCat
from models             import ItemSubCat
from models             import Order
from ops.order          import OrderService
from ops.coupon         import CouponService
from ops.credit         import CreditService



class ActionService(object):

    @staticmethod
    def change_order_coupon(user_id, order_id, old_coupon_id, new_coupon_id):
        ''' 更换优惠券操作 '''
        old_coupon      = CouponService.get_user_coupon(old_coupon_id) if old_coupon_id else 0
        new_coupon      = CouponService.get_user_coupon(new_coupon_id) if new_coupon_id else 0
        assert  old_coupon!=None, '旧优惠券不存在'
        assert new_coupon!=None, '新优惠券不存在'
        old_coupon_price= old_coupon.price if old_coupon else 0
        new_coupon_price= new_coupon.price if new_coupon else 0
        where           = and_(
            Order.coupon_id==old_coupon_id,
            Order.id==order_id,
            Order.user_id==user_id
            )
        assert (new_coupon_price or old_coupon_price), '必须至少存在一个优惠券'

        order           = OrderService.get_user_order(order_id, user_id)
        credit          = CreditService.get_user_credit(user_id)

        assert (new_coupon_price or 0) <= order.total, '优惠券金额不能超过订单总额'
        data            = {
            'coupon_amount' : new_coupon_price,
            'coupon_id'     : new_coupon_id,
            'credit_cmount' : new_credit_amount,
            'price'         : order.price,
            }

        success         = False
        diff_price      = old_coupon_price - new_coupon_price
        if diff_price<0:
            #使用了一张面值更大的优惠券
            if float(order.price)+diff_price>=0:
                data['price'] = float(order.price)+diff_price
            elif order.price>0:
                data['price'] = 0
                result        = CreditService.modify_credit(user_id, (float(order.price)+diff_price), commit=False)
            elif float(order.price)+diff_price<0:
                result        = CreditService.modify_credit(user_id, diff_price, commit=False)

        if diff_price>0:
            #使用了一张面值更小的优惠券
            #需要用更大的额度 或现金
            credit_remain   = credit.total - credit.used
            if order.price:
                data['price'] = order.price+diff_price
            elif credit_remain>=diff_price:
                result          = CreditService.modify_credit(user_id, diff_price, commit=False)
                data['credit_amount'] = Order.credit_amount + credit_remain
                if result:
                    db.session.commit()
                    success     = True
                else:
                    db.session.rollback()
                    success     = False
            else:
                data['price'] = diff_price - credit_remain
                data['credit_amount'] = Order.credit_amount + credit_remain

                result          = CreditService.modify_credit(user_id, credit_remain, commit=False)
                if result:
                    db.session.commit()
                    success     = True
                else:
                    db.session.rollback()
                    success     = False

        if success:
            count   = OrderService.update_order(where, commit=False)
            if count:
                db.session.commit()
                return success
    
        return False







