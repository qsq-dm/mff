# -*- coding: utf-8 -*-
from settings import celery

from thirdparty.wx_pay import send_redpack

from thirdparty.sms import send_sms



@celery.task
def send_redpack_after_pay(open_id, price):
    ''' 用户查看问题支付后发红包给收红包用户 '''
    send_redpack(open_id, price)