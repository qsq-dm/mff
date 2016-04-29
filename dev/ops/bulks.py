# -*- coding: utf-8 -*-
import time
import urllib
from collections    import defaultdict

from models         import User
from ops.user       import UserService
from ops.item       import ItemService
from ops.activity   import ActivityService
from ops.credit     import CreditService
from ops.order      import OrderService
from ops.promote    import PromoteService
from ops.trial      import TrialService
from ops.coupon     import CouponService
from ops.notification import NotificationService
from ops.redpack      import RedpackService
from ops.data       import DataService
from settings       import ANONY_IMAGE


now = lambda :int(time.time())



def fetch_refs(items, id_, func=None, keep_id=False, **kw):
    refs = defaultdict(dict)
    dest_key  = kw.pop('dest_key', None) or id_.replace('_id', '')
    ref_key   = kw.pop('ref_key', None) or 'id'
    for item in items:
        ref_id         = item.get(id_)
        item[dest_key] = refs[ref_id]

    ref_list = func(refs.keys(), **kw)
    for item in ref_list:
        refs[item[ref_key]].update(item)
    if not keep_id:
        #重复的关联怎么优化处理 只保留一个引用
        for item in items:
            item.pop(id_, None)
    print items


ANONYMOUS_USER  = {
    'name': '匿名用户',
    'id': 0,
    'avatar': ANONY_IMAGE
    }
def fetch_user_refs(items, func=UserService.get_users_by_ids, **kw):
    id_     = 'user_id'
    fetch_refs(items, id_, func, **kw)
    for item in items:
        if item.get('is_anonymous'):
            item['user'] = ANONYMOUS_USER


def fetch_item_refs(items, id_='item_id', func=ItemService.get_items_by_ids, **kw):
    fetch_refs(items, id_, func, **kw)


def fetch_item_cat_refs(items, id_='cat_id', func=ItemService.get_cats_by_ids, **kw):
    fetch_refs(items, id_, func, **kw)


def fetch_item_subcat_refs(items, id_='sub_cat_id', func=ItemService.get_subcats_by_ids, **kw):
    fetch_refs(items, id_, func, **kw)


def fetch_credit_refs(items, id_='user_id', func=UserService.get_credit_applies_by_ids, **kw):
    fetch_refs(items, id_, func, ref_key='user_id', **kw)

def fetch_activity_refs(items, id_='activity_id', func=ActivityService.get_activitys_by_ids, **kw): 
    fetch_refs(items, id_, func, **kw)


def fetch_hospital_refs(items, id_='hospital_id', func=ItemService.get_hospitals_by_ids, **kw): 
    fetch_refs(items, id_, func, **kw)


def fetch_servicecode_refrence(items, id_='order_id', func=OrderService.get_servicecodes_by_order_ids, **kw):
    fetch_refs(items, id_, func, ref_key='order_id', **kw)


def fetch_order_refs(items, id_='order_id', func=OrderService.get_orders_by_ids, **kw):
    fetch_refs(items, id_, func, **kw)


def fetch_wechatinfo_refs(items, id_='user_id', func=PromoteService.get_user_qrcodes_by_user_ids, **kw):
    fetch_refs(items, id_, func, ref_key='user_id', **kw)


def fetch_apply_refs(items, id_='user_id', func=TrialService.get_trial_apply_by_user_ids, **kw):
    fetch_refs(items, id_, func, ref_key='user_id', **kw)


def fetch_coupon_refs(items, id_='coupon_id', func=CouponService.get_coupon_by_ids, **kw):
    fetch_refs(items, id_, func, **kw)


def fetch_article_refs(items, id_='article_id', func=NotificationService.get_articles_by_ids, **kw):
    fetch_refs(items, id_, func, **kw)

def fetch_question_refs(items, id_='question_id', func=RedpackService.get_questions_by_ids, **kw):
    fetch_refs(items, id_, func, **kw)

def fetch_qrcodeuser_refs(items, id_='qr_user_id', func=RedpackService.get_qr_user_by_ids, **kw):
    fetch_refs(items, id_, func, **kw)

def fetch_school_refs(items, id_='school_id', func=DataService.get_schools_dict_by_ids, **kw):
    fetch_refs(items, id_, func, **kw)


def fetch_min_period_info(items):
    ''' 商品列表 获取最低分期价格期数 '''
    _, period_pay_choices   = CreditService.get_paged_period_choices()
    choice_map              = {i['id']:i for i in period_pay_choices}
    period_id_count_map     = {i['id']:i['period_count'] for i in period_pay_choices}
    min_choice_id_func      = lambda choices: max(choices, key=lambda i:period_id_count_map[i])
    for item in items:
        choices             = item.pop('support_choice_list')
        min_choice          = choice_map[min_choice_id_func(choices)] if choices else None
        if min_choice:
            period_count        = min_choice['period_count']
            period_fee          = min_choice['period_fee']
            price               = item['price']
            period_amount       = price/period_count
            item['period_count']= period_count
            item['period_money']= int(period_amount*(1+period_fee))
        else:
            item['period_count']= 1
            item['period_money']= item['price']








