# -*- coding: utf-8 -*-
import time

from sqlalchemy import and_
from models         import db
from models         import PayNotifyLog
from models         import AlipayOrderUser
from models         import UserDevice
from models         import UserDeviceLog

from util.utils     import dt_obj


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

    @staticmethod
    def exist_device(device_id):
        return bool(UserDevice.query.filter(UserDevice.device_id==device_id).first())

    @staticmethod
    def log_device(device_id, **kw):
        exist   = LogService.exist_device(device_id)
        if exist:
            kw['update_time'] = dt_obj.now()
            UserDevice.query.filter(UserDevice.device_id==device_id).update(kw)
            db.session.commit()
        else:
            device  = UserDevice(device_id=device_id, **kw)
            db.session.add(device)
            db.session.commit()

    @staticmethod
    def exist_user_device(device_id, user_id):
        ''' '''
        query   = and_(
            UserDeviceLog.device_id==device_id,
            UserDeviceLog.user_id==user_id)
        return bool(UserDeviceLog.query.filter(query).first())

    @staticmethod
    def update_device_user(device_id, user_id):
        count   = UserDevice.query.filter(UserDevice.device_id==device_id).update({'user_id':user_id, 'update_time':dt_obj.now()})
        db.session.commit()
        return count
 
    @staticmethod
    def log_user_device(device_id, user_id):
        count       = LogService.update_device_user(device_id, user_id)
        if not LogService.exist_user_device(device_id, user_id):
            log     = UserDeviceLog(user_id=user_id, device_id=device_id)
            db.session.add(log)
            db.session.commit()
            return log.id


