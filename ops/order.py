# -*- coding: utf-8 -*-
import json
from collections import defaultdict
from sqlalchemy import and_

from models         import db
from models         import Order
from models         import UserCoupon
from models         import UserCredit
from models         import ServiceCode
from models         import OrderLog
from models         import Repayment
from models         import Repayment
from models         import PayLogOrderNo
from models         import PeriodPayLog
from util.utils     import random_str
from util.utils     import random_no
from util.utils     import get_time_str_from_dt
from util.utils     import dt_obj
from util.utils     import format_price
from util.sqlerr    import SQL_DUPLICATE
from util.sqlerr    import SQL_DUPLICATE_ORDER_NO
from util.sqlerr    import SQL_DUPLICATE_COUPON
from util.sqlerr    import SQL_REF_COUPON_NOT_EXIST
from ops.utils      import get_page
from ops.utils      import get_items
from ops.utils      import count_items
from constants      import ORDER_STATUS
from constants      import SERVICE_STATUS


class OrderService(object):
    ''' '''
    @staticmethod
    def add_order(user_id, item_id, hospital_id, \
            price, credit_amount, total_fee, coupon_amount, total, \
            credit_choice_id, user_coupon_id, order_no, credit_verified, \
            status=ORDER_STATUS.NEW_ORDER):
        try:
            coupon_id   = user_coupon_id or None #外键约束 不能为0
            credit_choice_id = credit_choice_id or None
            order       = Order(
                total_fee           = total_fee,
                user_id             = user_id,
                item_id             = item_id,
                hospital_id         = hospital_id,
                total               = total,
                credit_choice_id    = credit_choice_id,
                coupon_id           = coupon_id,
                order_no            = order_no,
                credit_amount       = credit_amount,
                price               = price,
                status              = status,
                coupon_amount       = coupon_amount,
                credit_verified     = credit_verified
                )
            db.session.add(order)
            db.session.commit()
            return order.id
        except Exception as e:
            db.session.rollback()
            import traceback
            traceback.print_exc()
            if SQL_DUPLICATE_ORDER_NO.search(str(e)):
                print 'duplicate order no'
            assert 0, '服务器忙'

    @staticmethod
    def update_order(where, commit=True, **kw):
        count       = Order.query.filter(where).update(kw, synchronize_session=False)
        db.session.commit()
        return count

    @staticmethod
    def get_user_order(order_id, user_id):
        query   = and_(
            Order.id==order_id,
            Order.user_id==user_id
            )
        return Order.query.filter(query).first()

    @staticmethod
    def create_servicecode(order_id):
        random_code     = random_str()
        service_code    = ServiceCode.query.filter(ServiceCode.code==random_code).first()
        while service_code:
            random_code     = random_str()
            service_code    = ServiceCode.query.filter(ServiceCode.code==random_code).first()
        try:
            service         = ServiceCode(order_id=order_id, code=random_code)
            db.session.add(service)
            db.session.commit()
            return random_code
        except Exception as e:
            db.session.rollback()

    @staticmethod
    def get_servicecode(order_id):
        return ServiceCode.query.filter(ServiceCode.order_id==order_id).first()

    @staticmethod
    def get_paged_orders(**kw):
        return get_page(Order, {}, **kw)

    @staticmethod
    def get_orders(where):
        ''' 订单列表 '''
        return Order.query.filter(where).all()
    @staticmethod
    def create_no():
        ''' 随机生成订单号 第12位插入一个'''
        now     = dt_obj.now()
        timestr = get_time_str_from_dt(now, format='%Y%m%d%H%M%S%f')
        random_number    = random_no(4)
        print now, timestr, random_number
        return timestr[:12] + random_number + timestr[12:]

    @staticmethod
    def get_order_by_orderno(order_no):
        ''' '''
        return Order.query.filter(Order.order_no==order_no).first()

    @staticmethod
    def update_order_status(order_id, status, user_id=None, where=None):
        query       = and_()
        query.append(Order.id==order_id)
        if user_id: query.append(Order.user_id==user_id)
        if where is not None: query.append(where)
        count       = Order.query.filter(query).update({'status':status},synchronize_session=False)
        if count:
            log     = OrderLog(order_id=order_id, status=status)
            db.session.add(log)
        db.session.commit()
        return count

    @staticmethod
    def repayment(user_id, pay_method, coupon_id, price, data, order_no):
        try:
            repayment = Repayment(
                pay_method=pay_method, coupon_id=coupon_id,
                user_id=user_id, price=price, order_no=order_no,
                data=data)
            db.session.add(repayment)
            db.session.commit()
            return repayment.id
        except Exception as e:
            print 'except'
            print str(e)
            db.session.rollback()
            if SQL_REF_COUPON_NOT_EXIST.search(str(e)):
                print '优惠券不存在'
            elif SQL_DUPLICATE_ORDER_NO.search(str(e)):
                print '订单号已存在'
            elif SQL_DUPLICATE_COUPON.search(str(e)):
                print '优惠券已被使用'

    @staticmethod
    def update_repayment(where, **kw):
        ''' 更新还款单状态 '''
        count   = Repayment.query.filter(where).update(kw, synchronize_session=False)
        db.session.commit()
        return count

    @staticmethod
    def book_surgery(order_id, book_time):
        ''' 预约时间手术 '''
        query   = and_(
            ServiceCode.order_id==order_id,
            ServiceCode.status==SERVICE_STATUS.STANDBY
            )
        data    = {
            'status'    : SERVICE_STATUS.BOOKED,
            'book_time' : book_time
            }
        count   = ServiceCode.query.filter(query).update(data)
        db.session.commit()
        return count

    @staticmethod
    def cancel_book(order_id):
        ''' 取消预约 '''
        query   = and_(
            ServiceCode.order_id==order_id,
            ServiceCode.status==SERVICE_STATUS.BOOKED
            )
        data    = {
            'status'    : SERVICE_STATUS.STANDBY,
            }
        count   = ServiceCode.query.filter(query).update(data)
        db.session.commit()
        return count

    @staticmethod
    def verify_servicecode(order_id, service_code):
        ''' 验证服务码 确认手术 '''
        query       = and_(
            ServiceCode.order_id==order_id,
            ServiceCode.code==service_code,
            ServiceCode.status==SERVICE_STATUS.BOOKED
            )
        count       = ServiceCode.query.filter(query).update({'status':SERVICE_STATUS.VERIFYED})
        db.session.commit()
        if count:
            print '确认手术'
        else:
            print '服务码找不到'
        return count

    @staticmethod
    def cancel_surgery(order_id):
        ''' 取消手术 '''
        query       = and_(
            ServiceCode.order_id==order_id,
            ServiceCode.status==SERVICE_STATUS.VERIFYED
            )
        count       = ServiceCode.query.filter(query).update({'status':SERVICE_STATUS.BOOKED})
        db.session.commit()
        if count:
            print '已取消手术'
        else:
            print '服务码找不到'
        return count

    @staticmethod
    def get_user_repayment(repayment_id, user_id):
        query   = and_(
            Repayment.id==repayment_id,
            Repayment.user_id==user_id
            )
        repayment   = Repayment.query.filter(query).first()
        return repayment

    @staticmethod
    def get_repayment_by_orderno(order_no):
        query   = and_(
            Repayment.order_no==order_no
            )
        repayment   = Repayment.query.filter(query).first()
        return repayment

    @staticmethod
    def count_order(where=None):
        return count_items(Order, where=where)

    @staticmethod
    def get_order_by_id(order_id):
        order   = Order.query.filter(Order.id==order_id).first()
        return order

    @staticmethod
    def get_service_codes_by_order_ids(order_ids):
        ''' '''
        rows = ServiceCode.query.filter(ServiceCode.order_id.in_(order_ids)).all()
        return {i.order_id:i.status for i in rows}

    @staticmethod
    def get_servicecodes_by_order_ids(order_ids, **kw):
        rows = ServiceCode.query.filter(ServiceCode.order_id.in_(order_ids)).all()
        return [i.as_dict() for i in rows]

    @staticmethod
    def get_orders_by_ids(order_ids):
        ''' 返回 '''
        return get_items(Order, order_ids)

    @staticmethod
    def add_repayment_log(period_pay_log_id, price, total, order_no):
        try:
            log     = PayLogOrderNo(period_pay_log_id=period_pay_log_id, price=price, total=total, order_no=order_no)
            db.session.add(log)
            db.session.commit()
            return log.id
        except Exception as e:
            import traceback
            traceback.print_exc()
            db.session.rollback()
            if SQL_DUPLICATE.search(str(e)):
                assert 0, '分期{}已还{}'.format(period_pay_log_id, price)

    @staticmethod
    def gen_repayment_log(repayment):
        ''' 还款ID '''
        log_list     = json.loads(repayment.data)
        print log_list, 'log_list'
        for data in log_list:
            print data,'...'
            period_pay_log_id = data['id']
            amount            = data['amount']
            fee               = data['fee']
            punish            = data['punish']
            #total             = format_price(float(amount)+float(fee or 0)+float(punish or 0))
            price             = format_price(float(amount)+float(fee or 0))
            OrderService.add_repayment_log(period_pay_log_id, price, repayment.price, repayment.order_no)

    @staticmethod
    def order_repayment_logs_amount(order_id):
        ''' 已还的总额 '''
        subquery    = db.session.query(PeriodPayLog.id).filter(PeriodPayLog.order_id==order_id).subquery()
        logs        = PayLogOrderNo.query.filter(PayLogOrderNo.period_pay_log_id.in_(subquery)).all()
        return sum(log.price for log in logs)

    @staticmethod
    def get_order_repayment_logs_amount(order_id):
        ''' 所有已还的总额按订单划分 '''
        subquery     = db.session.query(PeriodPayLog.id).filter(PeriodPayLog.order_id==order_id).subquery()
        logs         = PayLogOrderNo.query.filter(PayLogOrderNo.period_pay_log_id.in_(subquery)).all()

        order_no_map = defaultdict(lambda:0)
        order_no_total_map  = {}
        for log in logs:
            order_no_total_map[log.order_no]     = format_price(log.total)
            order_no_map[log.order_no] += format_price(log.price)

        data         = {}
        for order_no, price in order_no_map.items():
            repayment      = Repayment.query.filter(Repayment.order_no==order_no).first()
            assert repayment, '还款不存在'
            data[order_no] = {
                'price': format_price(price),
                'pay_method': repayment.pay_method,           
                'total': order_no_total_map[order_no],
                'transaction_id': repayment.transaction_id
                }
        return data

    @staticmethod
    def get_order_by_coupon_id(coupon_id):
        ''' '''
        return Order.query.filter(Order.coupon_id==coupon_id).first()

def set_order_status(order, comment=None, servicecode=None):
    ''' 根据服务码状态 是否已评论重新订单状态 '''
    if order['user_finished']:
        order['status'] = ORDER_STATUS.FINISH
    elif order['status']==ORDER_STATUS.FINISH:
        order['status'] = ORDER_STATUS.PAY_SUCCESS
    if order['credit_verified']==0 and order['status'] in [ORDER_STATUS.PAY_SUCCESS]:
        order['status'] = ORDER_STATUS.VERIFYING
    elif order['credit_verified']==2:
        order['status'] = ORDER_STATUS.REJECTED
    elif order['status']==ORDER_STATUS.PAY_SUCCESS:
        if servicecode['status'] == 1:
            order['status']     = ORDER_STATUS.BOOKED
        elif servicecode['status'] == 2:
            order['status']     = ORDER_STATUS.CONFIRMED
    elif order['status'] == ORDER_STATUS.FINISH and not comment:
        order['status'] = ORDER_STATUS.TO_COMMENT
