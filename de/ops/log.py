# -*- coding: utf-8 -*-
import time

from models         import db
from models         import PayNotifyLog
from models         import AlipayOrderUser


class LogService(object):
    ''' '''
    @staticmethod
    def log_pay_callback(pay_type, content):
        log         = PayNotifyLog(pay_type=pay_type, content=content)
        db.session.add(log)
        db.session.commit()

    @staticmethod
    def log_alipay_buyer_email(order_no, buyer_email):
        try:
            ref     = AlipayOrderUser(order_no=order_no, buyer_email=buyer_email)
            db.session.add(ref)
            db.session.commit()
            return ref.id
        except Exception as e:
            import traceback
            traceback.print_exc()
            db.session.rollback()

