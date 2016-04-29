# -*- coding: utf-8 -*-
from decimal import Decimal
from sqlalchemy import and_

from models     import db
from models     import CreditUseLog
from models     import Order
from models     import UserCredit
from models     import PeriodPayLog
from models     import PeriodPayChoice
from models     import CreditApply
from util.sqlerr import SQL_DUPLICATE
from util.utils     import get_due_time
from util.utils     import dt_obj
from ops.utils      import count_items
from ops.utils      import get_page
from settings       import DEFAULT_CREDIT
from constants      import CREDIT_STATUS


class CreditService(object):
    ''' '''

    @staticmethod
    def create_default_credit(user_id, total=DEFAULT_CREDIT, status=0):
        ''' 创建额度 '''
        try:
            credit      = UserCredit(user_id=user_id, total=total, status=status)
            db.session.add(credit)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            if SQL_DUPLICATE.search(str(e)):
                return False
            else:
                raise(e)

    @staticmethod
    def get_user_credit(user_id):
        credit = UserCredit.query.filter(UserCredit.user_id==user_id).first()
        return credit

    @staticmethod
    def set_user_credit_total(user_id, total):
        ''' 审核通过设置用户额度 '''
        credit  = CreditService.get_user_credit(user_id)
        if not credit:
            CreditService.create_default_credit(user_id, total, status=1)
        else:
            UserCredit.query.filter(UserCredit.user_id==user_id).update({'total':total, 'status':CREDIT_STATUS.VERIFIED})
            db.session.commit()

    @staticmethod
    def update_user_credit_status(user_id, status):
        count   = UserCredit.query.filter(UserCredit.user_id==user_id).update({'status':status})
        db.session.commit()
        return count

    @staticmethod
    def init_credit(user_id):
        credit  = CreditService.get_user_credit(user_id)
        if not credit:
            CreditService.create_default_credit(user_id)
            credit  = CreditService.get_user_credit(user_id)
        return credit

    @staticmethod
    def modify_credit(user_id, amount):
        '''
        变更信用额度
        1变更成功
        2变更成功 但额度是虚假的 未通过审核
        0额度不足
        '''
        amount              = Decimal(str(amount))
        verified_query      = and_(
            UserCredit.user_id==user_id,
            UserCredit.status==2,
            UserCredit.used+amount<=UserCredit.total,
            UserCredit.used+amount>=0,
            )
        unverified_query    = and_(
            UserCredit.user_id==user_id,
            UserCredit.status==1,
            UserCredit.used+amount<=UserCredit.total,
            UserCredit.used+amount>=0,
            )
        update_data         = {
            'used':UserCredit.used+amount
            }
        count       = UserCredit.query.filter(verified_query).update(update_data)
        if count:
            log     = CreditUseLog(user_id=user_id, amount=amount, status=1)
            db.session.add(log)
            db.session.commit()
            return 1
        count       = UserCredit.query.filter(unverified_query).update(update_data)
        if count:
            log     = CreditUseLog(user_id=user_id, amount=amount, status=2)
            db.session.add(log)
            db.session.commit()
            return 2

        db.session.commit()
        return 0
            
    @staticmethod
    def get_period_choices():
        return PeriodPayChoice.query.all()

    @staticmethod
    def get_period_choice(choice_id):
        choice  = PeriodPayChoice.query.filter(PeriodPayChoice.id==choice_id).first()
        return choice

    @staticmethod
    def gen_order_period_logs(order_id):
        order       = Order.query.filter(Order.id==order_id).first()
        assert order, '订单不存在'
        choice      = PeriodPayChoice.query.filter(PeriodPayChoice.id==order.credit_choice_id).first()
        total_amount= order.credit_amount - order.total_fee
        period_amount   = total_amount/choice.period_count
        period_fee      = float(period_amount)*choice.period_fee
        for i in range(1, 1+choice.period_count):
            due_time    = get_due_time(i)
            log         = PeriodPayLog(
                order_id                =   order_id,
                period_count            =   choice.period_count, 
                user_id                 =   order.user_id,
                period_pay_index        =   i,
                amount                  =   period_amount,
                fee                     =   period_fee,
                deadline                =   due_time
                )
            db.session.add(log)
        db.session.commit()

    @staticmethod
    def get_period_pay_logs(user_id, where=None):
        query       = and_()
        query.append(PeriodPayLog.user_id==user_id)
        if where is not None: query.append(where)
        logs        = PeriodPayLog.query.filter(query).all()
        return logs

    @staticmethod
    def get_paged_pay_logs(**kw):
        return get_page(PeriodPayLog, {}, **kw)

    @staticmethod
    def add_apply(user_id, **kw):
        ''' 提交第一步申请资料 '''
        try:
            kw['create_time'] = dt_obj.now()
            apply   = CreditApply(user_id=user_id, **kw)
            db.session.add(apply)
            db.session.commit()
            return apply.id
        except Exception as e:
            db.session.rollback()
            if SQL_DUPLICATE.search(str(e)):
                pass
            else:
                raise(e)

    @staticmethod
    def update_apply(where, **kw):
        ''' 更新申请 '''
        kw.setdefault('update_time', dt_obj.now())
        count   = CreditApply.query.filter(where).update(kw)
        db.session.commit()
        return count

    @staticmethod
    def create_period_choice(**kw):
        try:
            choice = PeriodPayChoice(**kw)
            db.session.add(choice)
            db.session.commit()
            return choice.id
        except Exception as e:
            db.session.rollback()

    @staticmethod
    def get_paged_apply_list(**kw):
        return get_page(CreditApply, {}, **kw)

    @staticmethod
    def count_apply(where=None):
        return count_items(CreditApply, where=where)

    @staticmethod
    def get_apply_dict_by_id(apply_id):
        apply   = CreditApply.query.filter(CreditApply.id==apply_id).first()
        if apply: return apply.as_dict()

    @staticmethod
    def get_apply_dict_by_userid(user_id):
        apply   = CreditApply.query.filter(CreditApply.user_id==user_id).first()
        if apply: return apply.as_dict()

    @staticmethod
    def update_pay_log(log_ids):
        ''' 还款 '''
        query   = and_(
            PeriodPayLog.id.in_(log_ids),
            PeriodPayLog.status==0
            )
        repayment_time  = dt_obj.now()
        count   = PeriodPayLog.query.filter(query).update({'status':1, 'repayment_time':repayment_time}, synchronize_session=False)
        db.session.commit()
        if count==len(log_ids):
            return True
        else:
            db.session.rollback()
            return False

    @staticmethod
    def cancel_pay_logs(order_id):
        query   = and_(
            PeriodPayLog.order_id==order_id,
            PeriodPayLog.status==0
            )
        count   = PeriodPayLog.query.filter(query).update({'status':2})
        db.session.commit()
        return count

    @staticmethod
    def get_paged_period_choices(**kw):
        return get_page(PeriodPayChoice, {}, **kw)

    @staticmethod
    def get_paged_period_pay_logs(**kw):
        return get_page(PeriodPayLog, {}, **kw)

    @staticmethod
    def count_logs(where=None):
        return count_items(PeriodPayLog, where=where)







