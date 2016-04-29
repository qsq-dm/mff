# -*- coding: utf-8 -*-

from sqlalchemy  import and_
from models      import db
from models      import Order
from ops.user    import UserService
from ops.order   import OrderService
from ops.credit  import CreditService
from ops.activity import ActivityService
from ops.room_design import RoomDesignService
from ops.item    import ItemService
from constants   import ORDER_STATUS
from thirdparty.sms import send_sms_new_order



def pay_success_action(order, send_verified=False, need_pay=True, **kw):
    ''' 支付成功 处理函数
        send_verified #需要额外微信或支付宝付钱并且额度待审核订单 审核前已支付成功现金部分 没发送短信就return了 审核通过后不管count多少 需要发送短信 
    '''
    new_status      = ORDER_STATUS.PAY_SUCCESS
    where           = and_(
        Order.id==order.id,
        Order.status.in_([ORDER_STATUS.TO_PAY, ORDER_STATUS.NEW_ORDER])
        )
    kw['status']    = new_status
    count           = OrderService.update_order(where, **kw)
    if not order.credit_verified: return
    user            = UserService.get_user_by_id(order.user_id)
    phone           = user.phone
    hospital        = ItemService.get_hospital_dict_by_id(order.hospital_id)
    hospital_name   = hospital['name']
    hospital_addr   = hospital['addr']
    hospital_phone  = hospital['phone']
    item            = ItemService.get_item_dict_by_id(order.item_id)
    item_name       = item['title']
    desc            = '{},{},{}'.format(hospital_name, hospital_addr, hospital_phone)
    print 'desc', desc
    if count or send_verified or not need_pay:
        service_code= OrderService.create_servicecode(order.id)
        if order.credit_amount:
            CreditService.gen_order_period_logs(order.id)
        #给用户发送通知，确认购买成功
        send_sms_new_order.delay(phone, item_name, desc, service_code)


def get_item_activity_price(item):
    activity        = ActivityService.get_current_activity()
    if activity:
        activity_item     = ItemService.get_item_activity(item['id'], activity['id'])
        if activity_item:
            item['price'] = activity_item['price']
