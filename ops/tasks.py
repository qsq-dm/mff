# -*- coding: utf-8 -*-
from settings import celery

from thirdparty.wx_pay import send_redpack
from thirdparty.wx_pay import send_draw_cash
from thirdparty.sms import send_sms

from ops.redpack    import RedpackService
from ops.cache      import cache

@celery.task
def send_redpack_after_pay(open_id, price, name):
    ''' 用户查看问题支付后发红包给收红包用户 '''
    result      = send_redpack(open_id, price, name)
    total       = RedpackService.total_money()
    thousands_count = int(total) / 1000
    total_key   = 'total_redpack_send_money'
    if result['result_code'] == 'FAIL':
        send_sms('18801794295', '{}失败{}'.format(total, result['err_code']))
    if thousands_count: #每超过1000发短信给所有运营
        if cache.sadd(total_key, thousands_count):
            print 'send sms '
            send_sms('18801794295', '已使用{}元'.format(total))
            send_sms('18621955395', '已使用{}元'.format(total))
            send_sms('18750552673', '已使用{}元'.format(total))



@celery.task
def send_user_draw_cash(open_id, price):
    ''' '''
    return send_draw_cash(open_id, price)