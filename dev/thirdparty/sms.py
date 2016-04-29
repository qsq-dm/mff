# -*- coding: utf-8 -*-
import time
import hashlib
from datetime import datetime
import random
from functools import wraps

from flask import request
from flask import url_for

from thirdparty.SendTemplateSMS import sendTemplateSMS
import settings


def today_remain_seconds():
    now = datetime.now()
    year, month, day = now.year, now.month, now.day
    now_second = time.mktime(now.timetuple())
    cut_now = datetime(year, month, day)
    cut_now_second = time.mktime(cut_now.timetuple())
    return 86400 - int(now_second-cut_now_second)

def gen_vcode():
    code = random.randrange(100000,999999)
    return str(code)

def gen_complex_vcode():
    code = random.randrange(10000000,99999999)
    return str(code)


def _send_sms(phone, data, tpl_id):
    try:
        #请求包格式无法解析错误  把unicode转为str
        phone  = str(phone)
        for i in range(len(data)):
            data[i] = str(data[i])
            print 
        print phone, data, tpl_id, '发送短信'
        result = sendTemplateSMS(phone, data, tpl_id)
        return result
    except:
        import traceback
        traceback.print_exc()


@settings.celery.task
def send_sms(phone, vcode):
    print '发送注册短信', phone, vcode
    return _send_sms(phone, [vcode,5], 44515)


@settings.celery.task
def send_sms_apply_success(phone, amount):
    print '发送审核通过短信'
    return _send_sms(phone, [amount], 44988)


@settings.celery.task
def send_sms_apply_reject(phone):
    print '发送审核被拒短信'
    return _send_sms(phone, [], 44990)


@settings.celery.task
def send_sms_new_order(phone, name, desc, service_code):
    print '下单短信'
    return _send_sms(phone, [name, desc, service_code], 44994)


@settings.celery.task
def send_sms_refund(phone, name, price, period):
    print '退款短信'
    return _send_sms(phone, [name, price, period], 52093)


@settings.celery.task
def send_room_one(phone):
    ''' 老用户 '''
    return _send_sms(phone, [], 71623)


@settings.celery.task
def send_room_two(phone):
    ''' 拉票 '''
    return _send_sms(phone, [], 71638)





