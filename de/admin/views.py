# -*- coding: utf-8 -*-
import json
import time
import math
import pickle
from base64 import b64decode
from sqlalchemy import and_
from sqlalchemy import or_
from sqlalchemy import not_
from flask import request
from flask import redirect
from flask import Blueprint
from flask import render_template
from flask import make_response

from util.utils      import date_to_datetime
from util.utils      import jsonify_response
from util.utils      import template_response
from util.utils      import prefix_img_domain
from util.utils      import abbreviated_pages
from util.utils      import get_due_time
from util.utils      import format_price
from util.utils      import get_current_period
from util.utils      import cacl_punish_fee
from util.utils      import gen_item_no
from util.utils      import trans_list
from util.utils      import dt_obj
from util.sign       import gen_token
from util.sign       import del_cookie
from util.sign       import set_cookie
from util.sign       import get_cookie
from util.decorators import admin_json_dec
from util.validators import Optional
from util.validators import Inputs
from util.validators import MobileField
from util.validators import TextField
from util.validators import IdField
from util.validators import IntChoiceField
from util.validators import FloatField
from util.validators import IntChoicesField
from util.validators import BoolChoiceField
from util.validators import BoolIntChoiceField
from util.validators import IntField
from util.validators import REGField
from util.utils      import set_coupon_use_time

from models          import db
from models          import Item
from models          import School
from models          import Order
from models          import User
from models          import Promoter
from models          import Trial
from models          import DailyUser
from models          import ItemSubCat
from models          import ActivityItem
from models          import CreditApply
from models          import RecommendItem
from models          import Hospital
from models          import RecommendSubcat
from models          import PeriodPayLog
from models          import TrialApply
from models          import RecommendHospital
from ops.cache       import ChsiCache
from ops.cache       import AdminInvalidUserPasswdCache
from ops.common      import pay_success_action
from ops.beauty_tutorial   import TutorialService
from ops.admin       import AdminService
from ops.data        import DataService
from ops.promote     import PromoteService
from ops.item        import ItemService
from ops.user        import UserService
from ops.comment     import CommentService
from ops.credit      import CreditService
from ops.trial       import TrialService
from ops.coupon      import CouponService
from ops.bulks       import fetch_item_cat_refs
from ops.bulks       import fetch_user_refs
from ops.bulks       import fetch_item_refs
from ops.bulks       import fetch_order_refs
from ops.bulks       import fetch_item_subcat_refs
from ops.bulks       import fetch_hospital_refs
from ops.bulks       import fetch_wechatinfo_refs
from ops.bulks       import fetch_servicecode_refrence
from ops.bulks       import fetch_coupon_refs
from ops.order       import OrderService
from ops.order       import set_order_status
from ops.hospital    import HospitalService
from ops.activity    import ActivityService
from thirdparty.qn   import gen_qn_token
from thirdparty.qn   import upload_img
from thirdparty.sms  import send_sms_apply_success
from thirdparty.sms  import send_sms_apply_reject
from thirdparty.sms  import send_sms_refund
from thirdparty.chsi import login_xuexin
from thirdparty.chsi import refresh_chsi_captcha
from thirdparty.chsi import get_chsi_info
from thirdparty.wx_pay import refund_order
from thirdparty.wx_pay import refund_repayment
from thirdparty.wx_app_pay import refund_order as refund_app_order
from thirdparty.wx_app_pay import refund_repayment as wxapp_refund_repayment
from constants       import ResponseCode
from constants       import APPLY_STATUS
from constants       import ORDER_ADMIN_STATUS
from constants       import ORDER_STATUS
from constants       import ORDER_STATUS_LABEL
from constants       import ADMIN_ORDER_STATUS_CHOICES
from constants       import ORDER_ADMIN_STATUS_MAP
from constants       import CREDIT_STATUS
from constants       import PAY_METHOD


def index():
    ''' http://flask.pocoo.org/docs/0.10/blueprints/#templates '''
    return render_template('admin/index.html')


login_validator  = Inputs(
    {
     'name'         : TextField(min_length=1, max_length=100, msg='用户名'),
     'passwd'       : TextField(min_length=1, max_length=100, msg='密码')
    }
    )
@admin_json_dec(required=False, validator=login_validator)
def login():
    name   = request.valid_data.get('name')
    passwd = request.valid_data.get('passwd')
    admin  = AdminService.get_admin(name)
    count  = AdminInvalidUserPasswdCache.incr(name)
    assert count<10, '今日密码错误次数超限'
    if admin and admin.passwd==passwd:
        response    = jsonify_response({'code':ResponseCode.SUCCESS}, with_response=True)
        token       = gen_token(name)
        set_cookie(response, 'name', name, 86400*30)
        set_cookie(response, 'token', token, 86400*30)
        set_cookie(response, 'cat', str(admin.cat or 0), 86400*30)
        AdminInvalidUserPasswdCache.incr(name, -1)
        return response
    assert 0, '用户名或密码错误'


@admin_json_dec()
def logout():
    response = make_response(redirect('/admin'))
    del_cookie(response, 'name')
    del_cookie(response, 'token')
    return response


@admin_json_dec(roles=[0, 1, 2, 5])
def get_city_list(required=True, validator=None):
    has_more, cities     = DataService.get_paged_cities()

    result               = {
        'infos':cities
        }
    return jsonify_response(result)


new_city_validator  = Inputs(
    {
     'name'         : TextField(min_length=1, max_length=100, msg='城市名'),
    }
    )
@admin_json_dec(required=True, validator=new_city_validator)
def new_city():
    name            = request.valid_data.get('name')
    print name
    city_id         = DataService.create_city(name)

    result          = {
        'code'         : ResponseCode.SUCCESS,
        'msg'          : ''}
    return jsonify_response(result)


item_list_validator  = Inputs(
    {
     'keyword'         : Optional(TextField(min_length=1, max_length=100, msg='搜索关键字')),
     'sub_cat_id'      : Optional(IdField(msg='子分类id')),
     'sub_cat_id'      : Optional(IdField(msg='子分类id')),
     'hospital_id'     : Optional(IdField(msg='医院id')),
     'activity_id'     : Optional(IdField(msg='活动id')),
     'page'            : Optional(IdField(msg='页数')),
     'is_recommend'    : Optional(IntChoiceField(choices=[0,1], msg='是否推荐'))
    }
    )
@admin_json_dec(required=True, validator=item_list_validator)
def get_item_list():

    keyword       = request.valid_data.get('keyword')
    sub_cat_id    = request.valid_data.get('sub_cat_id')
    activity_id   = request.valid_data.get('activity_id')
    hospital_id   = request.valid_data.get('hospital_id')
    page          = request.valid_data.get('page') or 1
    is_recommend  = request.valid_data.get('is_recommend') or None

    limit         = 10
    start         = (page-1)*limit
    filters       = []
    order_by      = None
    join          = None
    if keyword: filters.append(Item.title.like('%{}%'.format(keyword)))
    if sub_cat_id:
        query     = or_(
            Item.sub_cat_ids==sub_cat_id,
            Item.sub_cat_ids.like('%,{}'.format(sub_cat_id)),
            Item.sub_cat_ids.like('%,{},%'.format(sub_cat_id)),
            Item.sub_cat_ids.like('{},%'.format(sub_cat_id))
            )
        filters.append(query)
    if hospital_id: filters.append(Item.hospital_id==hospital_id)
    if activity_id:
        subquery  = db.session.query(ActivityItem.item_id).filter(ActivityItem.activity_id==activity_id).subquery()
        filters.append(Item.id.in_(subquery))
    if is_recommend:
        subquery  = db.session.query(RecommendItem.item_id).subquery()
        filters.append(Item.id.in_(subquery))
        order_by  = RecommendItem.sort_order.asc()
        join      = RecommendItem
    where         = None
    if filters:
        where     = and_(*filters)
    total         = ItemService.count_items(where)
    page_info     = abbreviated_pages(int(math.ceil(total/(limit*1.0))), page)
    has_more, item_list = ItemService.get_the_paged_items(
        limit=limit, start=start, where=where, join=join, order_by=order_by)

    item_ids            = [ i['id'] for i in item_list]
    exists_recommend    = ItemService.exists_recommend_item_ids(item_ids)
    for i in item_list:
        i['is_recommend'] = i['id'] in exists_recommend
        i['sort_order']   = exists_recommend.get(i['id'], 0)

    fetch_item_subcat_refs(item_list)
    sub_cats            = [i['sub_cat'] for i in item_list]
    print sub_cats
    fetch_item_cat_refs(sub_cats)
    result              = {
        'infos'             : item_list,
        'page_info'         : page_info
        }

    return jsonify_response(result)


item_edit_validator  = Inputs(
    {
     'title'         : TextField(min_length=1, max_length=100, msg='商品名'),
     'item_no'       : Optional(TextField(min_length=0, max_length=100, msg='项目编号')),
     'image'         : TextField(min_length=1, max_length=1000, msg='商品小图'),
     'photos'        : Optional(TextField(min_length=0, max_length=1000, msg='图片列表')),
     'surgery_desc'  : TextField(min_length=1, max_length=1000000, msg='项目介绍'),
     'doctor_desc'   : TextField(min_length=1, max_length=1000000, msg='医生介绍'),
     'note'          : TextField(min_length=1, max_length=10000, msg='特别提醒'),
     'use_time'      : TextField(min_length=1, max_length=10000, msg='使用时间'),
     'has_fee'       : BoolIntChoiceField(msg='是否免息'),
     'direct_buy'    : BoolIntChoiceField(msg='是否直购'),
     #'sub_cat_id'    : Optional(IdField(msg='子分类id')),
     'sub_cat_ids'   : TextField(min_length=1, max_length=1000, msg='请选择分类'),
     'hospital_id'   : IdField(msg='医院id'),
     'price'         : FloatField(msg='价格'),
     'orig_price'    : FloatField(msg='原价'),
     'support_choice_list': IntChoicesField(choices=[1,2,3,4,5,6], msg='支持哪些分期选项'),
    }
    )
@admin_json_dec(required=True, validator=item_edit_validator, roles=[0,1,5])
def item_edit(item_id=None):
    title           = request.valid_data.get('title')
    sub_cat_id      = request.valid_data.get('sub_cat_id')
    sub_cat_ids     = request.valid_data.get('sub_cat_ids')
    price           = request.valid_data.get('price')
    orig_price      = request.valid_data.get('orig_price')
    hospital_id     = request.valid_data.get('hospital_id')
    item_no         = request.valid_data.get('item_no')
    image           = request.valid_data.get('image')
    has_fee         = request.valid_data.get('has_fee')
    direct_buy      = request.valid_data.get('direct_buy')
    photos          = request.valid_data.get('photos') or ''
    doctor_desc     = request.valid_data.get('doctor_desc')
    use_time        = request.valid_data.get('use_time')
    note            = request.valid_data.get('note')
    surgery_desc    = request.valid_data.get('surgery_desc')
    support_choice_list         = request.valid_data.get('support_choice_list')
    support_choices             = ','.join(map(str, support_choice_list))
    sub_cat_id = 1
    if item_id:
        assert item_no, '请输入商品编号'
        ItemService.update_item(item_id,
            title=title,
            sub_cat_id=sub_cat_id,
            sub_cat_ids=sub_cat_ids,
            price=price,
            orig_price=orig_price,
            support_choices=support_choices,
            hospital_id=hospital_id, item_no=item_no,
            photos=photos, surgery_desc=surgery_desc,
            doctor_desc=doctor_desc, image=image, direct_buy=direct_buy,
            has_fee=has_fee, use_time=use_time, note=note
            )
    else:
        item_no     = item_no or gen_item_no()
        item_id     = ItemService.create_item(
            title, hospital_id, sub_cat_id, sub_cat_ids, price, orig_price, item_no, support_choices, photos, surgery_desc, doctor_desc, image,
            has_fee, direct_buy, use_time, note)


    return jsonify_response({'item_id': item_id})


edit_itemcat_validator  = Inputs(
    {
     'name'         : TextField(min_length=1, max_length=100, msg='分类名'),
    }
    )
@admin_json_dec(required=True, validator=edit_itemcat_validator)
def edit_itemcat(cat_id=None):
    name            = request.valid_data.get('name')
    if cat_id:
        msg         = '修改成功'
        ItemService.update_cat(cat_id, **request.valid_data)
    else:
        msg         = '添加成功'
        ItemService.create_cat(name)
    result = {
        'code'  : ResponseCode.SUCCESS,
        'msg'   : msg
        }
    return jsonify_response(result)


edit_itemsubcat_validator  = Inputs(
    {
     'name'         : TextField(min_length=1, max_length=100, msg='小类名'),
     'icon'         : TextField(min_length=1, max_length=1000, msg='图标'),
     'cat_ids'      : TextField(min_length=1, max_length=1000, msg='逗号分隔的父分类id'),
     'cat_id'       : Optional(IdField(msg='分类id')),
    }
    )
@admin_json_dec(required=True, validator=edit_itemsubcat_validator)
def edit_itemsubcat(sub_cat_id=None):
    ''' 编辑／添加小类 '''
    name            = request.valid_data.get('name')
    icon            = request.valid_data.get('icon')
    cat_id          = request.valid_data.get('cat_id')
    cat_ids         = request.valid_data.get('cat_ids')
    if sub_cat_id:
        msg         = '修改成功'
        ItemService.update_subcat(sub_cat_id=sub_cat_id, **request.valid_data)
    else:
        msg         = '添加成功'
        desc        = ''
        ItemService.create_sub_cat(cat_id, name, icon, desc, cat_ids)
    result = {
        'code'  : ResponseCode.SUCCESS,
        'msg'   : msg
        }
    return jsonify_response(result)


new_period_pay_choice_validator  = Inputs(
    {
     'period_count'  : IntField(msg='分期数'),
     'period_fee'    : FloatField(msg='分期费率')
    }
    )
@admin_json_dec(validator=new_period_pay_choice_validator)
def new_period_pay_choice():
    period_count    = request.valid_data.get('period_count')
    period_fee      = request.valid_data.get('period_fee')

    pay_id          = CreditService.create_period_choice(period_count=period_count, period_fee=period_fee)
    result          = {
        'pay_id': pay_id
        }
    return jsonify_response(result)


@admin_json_dec(required=True)
def get_item():
    item_id         = request.args.get('item_id')
    item            = ItemService.get_item_dict_by_id(item_id)

    item['has_fee']     = 1 if item['has_fee'] else 0
    item['direct_buy']  = 1 if item['direct_buy'] else 0
    result          = {
        'data'  : item
        }
    response        = jsonify_response(result)
    return response


@admin_json_dec(required=True)
def get_cat():
    item_id         = request.args.get('cat_id')
    item            = ItemService.get_cat_dict_by_id(item_id)

    result          = {
        'data'         : item
        }
    return jsonify_response(result)


@admin_json_dec(required=True)
def get_subcat():
    item_id         = request.args.get('sub_cat_id')
    item            = ItemService.get_subcat_dict_by_id(item_id)

    result          = {
        'data'         : item
        }
    return jsonify_response(result)


@admin_json_dec(required=True)
def get_school_list():

    limit         = 100
    page          = int(request.args.get('page', 1))
    city_name     = request.args.get('city_name')
    start         = (page-1)*limit
    where         = None
    if city_name: where = School.city_name==city_name
    total         = DataService.count_schools(where=where)
    page_info     = abbreviated_pages(int(math.ceil(total/(limit*1.0))), page)
    has_more, item_list = DataService.get_paged_schools(limit=limit, start=start, where=where, _sort='city_name')

    result               = {
        'infos'             : item_list,
        'page_info'         : page_info,
        'total'             : total,
        }

    return jsonify_response(result)


@admin_json_dec(required=True)
def get_cat_list():
    has_more, cat_list  = ItemService.get_paged_cats(limit=1000, _sort='sort_order', _sort_dir='ASC')
    result               = {
        'infos'             : cat_list,
        'page_info'         : None,
        }

    return jsonify_response(result)


cat_list_validator  = Inputs(
    {
     'cat_id'       : Optional(IdField(msg='分类id')),
     'is_recommend' : Optional(IntChoiceField(choices=[0,1], msg='是否推荐'))
    }
    )
@admin_json_dec(required=True, validator=cat_list_validator)
def get_subcat_list():
    cat_id                 = request.valid_data.get('cat_id')
    is_recommend           = request.valid_data.get('is_recommend')

    filters       = []
    order_by      = None
    join          = None
    where         = None
    if is_recommend:
        subquery  = db.session.query(RecommendSubcat.sub_cat_id).subquery()
        filters.append(ItemSubCat.id.in_(subquery))
        order_by  = RecommendSubcat.sort_order.asc()
        join      = RecommendSubcat
    if cat_id:
        or_query= or_(
            ItemSubCat.cat_ids==cat_id,
            ItemSubCat.cat_ids.like('%,{}'.format(cat_id)),
            ItemSubCat.cat_ids.like('%,{},%'.format(cat_id)),
            ItemSubCat.cat_ids.like('{},%'.format(cat_id))
            )
        filters.append(or_query)

    if filters: where = and_(*filters)
    has_more, subcat_list  = ItemService.get_paged_sub_cats(where=where, order_by=order_by, join=join, limit=100)
    fetch_item_cat_refs(subcat_list)

    all_cats              = ItemService.get_item_cats()
    cat_id_obj            = {i.id:i.as_dict() for i in all_cats}
    sub_cat_ids           = [i['id'] for i in subcat_list]
    exists_recommend      = ItemService.exists_recommend_subcat_map(sub_cat_ids)
    for i in subcat_list:
        i['is_recommend'] = i['id'] in exists_recommend
        i['sort_order']   = exists_recommend.get(i['id'], 0)
        i['cat_list']     = [cat_id_obj.get(k) for k in i['cat_id_list']]
    result               = {
        'infos'             : subcat_list,
        'page_info'         : None,
        }

    return jsonify_response(result)


hospital_list_validator  = Inputs(
    {
     'keyword'         : Optional(TextField(min_length=1, max_length=100, msg='搜索关键字')),
     'is_recommend'    : Optional(IntChoiceField(choices=[0,1], msg='是否推荐')),
     'page'            : Optional(IdField(msg='页数')),
    }
    )
@admin_json_dec(required=True, validator=hospital_list_validator)
def get_hospital_list():
    is_recommend  = request.valid_data.get('is_recommend')
    keyword       = request.valid_data.get('keyword')
    page          = request.valid_data.get('page') or 1


    limit         = 10
    start         = (page-1)*limit
    filters       = []
    where         = None
    join          = None
    order_by      = None
    if is_recommend:
        subquery  = db.session.query(RecommendHospital.hospital_id).subquery()
        filters.append(Hospital.id.in_(subquery))
        order_by  = RecommendHospital.sort_order.asc()
        join      = RecommendHospital
    if keyword: filters.append(Hospital.name.like('%{}%'.format(keyword)))
    if filters: where = and_(*filters)
    total         = ItemService.count_hospitals(where)
    page_info     = abbreviated_pages(int(math.ceil(total/(limit*1.0))), page)
    has_more, hospital_list     = ItemService.get_paged_hospitals(
        join=join, order_by=order_by, where=where, start=start)

    item_ids            = [ i['id'] for i in hospital_list]
    exists_recommend    = ItemService.exists_recommend_hospital_ids(item_ids)
    for i in hospital_list:
        i['is_recommend'] = i['id'] in exists_recommend
        i['sort_order']   = exists_recommend.get(i['id'], 0)

    result                      = {
        'infos'             : hospital_list,
        'page_info'         : page_info,
        }

    return jsonify_response(result)



subcat_status_validator  = Inputs(
    {
     'subcat_id'    : IdField(msg='子分类id'),
     'status'       : IntChoiceField(choices=[0,1], msg='状态')
    }
    )
@admin_json_dec(required=True, validator=subcat_status_validator)
def set_subcat_status():
    subcat_id       = request.valid_data.get('subcat_id')
    status          = request.valid_data.get('status')

    ItemService.set_subcat_status(subcat_id, status)
    if status==0:
        ItemService.offline_subcat(subcat_id)
    result          = {}
    return jsonify_response(result)


@admin_json_dec(required=True)
def get_period_choice_list():
    _sort         = 'period_count'
    _sort_dir     = 'ASC'
    _, choice_list= CreditService.get_paged_period_choices(_sort=_sort, _sort_dir=_sort_dir)

    result        = {
        'infos'             : choice_list,
        'page_info'         : None,
        }

    return jsonify_response(result)


@admin_json_dec(required=True)
def refresh_qntoken():
    response    = jsonify_response({}, with_response=True)
    if 1:#not get_cookie('qntoken'):
        qntoken         = gen_qn_token()
        set_cookie(response, 'qntoken', qntoken, 86400*30)#cookie存token一小时

    return response


@admin_json_dec()
def get_apply_list():
    ''' 额度申请列表 '''
    limit         = 10
    page          = int(request.args.get('page', 1))
    apply_status  = int(request.args.get('apply_status') or 0)
    where         = None
    if apply_status==1:
        where     = CreditApply.status==APPLY_STATUS.VERIFIED
    elif apply_status==2:
        where     = CreditApply.status==APPLY_STATUS.REJECTED
    elif apply_status==3:
        where     = CreditApply.status==APPLY_STATUS.FIRST_STEP
    elif apply_status==4:
        where     = CreditApply.status==APPLY_STATUS.SECOND_STEP
    start         = (page-1)*limit
    total         = CreditService.count_apply(where=where)
    page_info     = abbreviated_pages(int(math.ceil(total/(limit*1.0))), page)
    has_more, item_list = CreditService.get_paged_apply_list(limit=limit, start=start, where=where, _sort='update_time')

    fetch_user_refs(item_list)
    result               = {
        'infos'             : item_list,
        'page_info'         : page_info,
        'total'             : total,
        }

    return jsonify_response(result)


@admin_json_dec()
def get_apply_detail():
    ''' 额度申请详情 '''
    apply_id        = request.args.get('apply_id')
    apply           = CreditService.get_apply_dict_by_id(apply_id)
    credit          = CreditService.get_user_credit(apply['user_id'])
    if credit: credit = credit.as_dict()
    fetch_user_refs((apply,))
    result          = {
        'apply'        : apply,
        'credit'       : credit
        }
    return jsonify_response(result)


apply_approve_validator  = Inputs(
    {
     'apply_id'       : IdField(msg='申请id'),
     'total'          : IntField(msg='额度'),
    }
    )
@admin_json_dec(validator=apply_approve_validator, roles=[0,1,5])
def apply_approve():
    ''' 申请通过 '''
    apply_id        = request.valid_data.get('apply_id')
    total           = request.valid_data.get('total')
    where       = and_(
        CreditApply.id==apply_id,
        )
    data        = {
        'status':APPLY_STATUS.VERIFIED
        }
    CreditService.update_apply(where, **data)
    apply       = CreditService.get_apply_dict_by_id(apply_id)
    credit      = CreditService.get_user_credit(apply['user_id'])
    if not credit:
        CreditService.init_credit(apply['user_id'])
        credit  = CreditService.get_user_credit(apply['user_id'])
    used        = credit.used
    err_msg     = '审批额度不能低于当前已使用额度{}'.format(used)
    assert total>=used, err_msg

    CreditService.set_user_credit_total(apply['user_id'], total)
    count       = CreditService.update_user_credit_status(apply['user_id'], CREDIT_STATUS.VERIFIED)
    if count:
        where       = and_(
            Order.user_id==apply['user_id'],
            Order.credit_verified!=1
            )
        orders      = OrderService.get_orders(where=where)
        for order in orders:
            where       = and_(
                Order.id==order.id,
                Order.credit_verified!=1,
                )
            count   = OrderService.update_order(where, credit_verified=1)
            if count and order.status==ORDER_STATUS.PAY_SUCCESS:
                pay_success_action(order, send_verified=True)
        where       = and_(
            Order.credit_verified!=1,
            Order.user_id==apply['user_id']
            )
        OrderService.update_order(where, credit_verified=1)
        user    = UserService.get_user_by_id(apply['user_id'])
        send_sms_apply_success.delay(user.phone, total)
    result      = {
        'code'     : ResponseCode.SUCCESS,
        'msg'      : ''
        }
    return jsonify_response(result)


@admin_json_dec()
def get_hospital():
    ''' 医院详情 '''
    hospital_id       = request.args.get('item_id')
    hospital          = ItemService.get_hospital_dict_by_id(hospital_id)

    result            = {
        'data'           : hospital
        }
    return jsonify_response(result)


apply_reject_validator  = Inputs(
    {
     'reason'         : TextField(min_length=1, max_length=1000, msg='被拒原因'),
     'apply_id'       : IdField(msg='申请id'),
    }
    )
@admin_json_dec(validator=apply_reject_validator, roles=[0,1,5])
def apply_reject():
    ''' 申请拒绝 '''
    apply_id    = request.valid_data.get('apply_id')
    reason      = request.valid_data.get('reason')

    apply       = CreditService.get_apply_dict_by_id(apply_id)
    assert apply, '申请不存在'
    where       = and_(
        CreditApply.id==apply_id
        )
    data        = {
        'status':APPLY_STATUS.REJECTED,
        'reason':reason,
        }
    CreditService.update_apply(where, **data)
    CreditService.update_user_credit_status(apply['user_id'], CREDIT_STATUS.REJECTED)
    user    = UserService.get_user_by_id(apply['user_id'])
    where       = and_(
            Order.user_id==apply['user_id'],
            Order.credit_verified==0
            )
    orders      = OrderService.get_orders(where=where)
    for order in orders:
        where       = and_(
                Order.id==order.id,
                Order.credit_verified==0,
                )
        count   = OrderService.update_order(where, credit_verified=2)
    send_sms_apply_reject.delay(user.phone)
    result      = {
        'code'     : ResponseCode.SUCCESS,
        'msg'      : ''
    }
    return jsonify_response(result)



hospital_edit_validator  = Inputs(
    {
     'name'           : TextField(min_length=1, max_length=100, msg='医院名'),
     'tags'           : TextField(min_length=1, max_length=100, msg='标签'),
     'addr'           : TextField(min_length=1, max_length=100, msg='地址'),
     'phone'          : TextField(min_length=1, max_length=100, msg='电话'),
     'photos'         : Optional(TextField(min_length=0, max_length=1000, msg='图片列表')),
     'image'          : TextField(min_length=1, max_length=100, msg='医院头像'),
     'desc'           : TextField(min_length=1, max_length=10000, msg='描述'),
     'working_time'   : TextField(min_length=1, max_length=100, msg='工作时间'),
     'city_id'        : IdField(msg='城市id'),
     'lng'            : FloatField(msg='经度'),
     'lat'            : FloatField(msg='纬度'),
    }
    )
@admin_json_dec(required=True, validator=hospital_edit_validator)
def hospital_edit(item_id=None):
    name        = request.valid_data.get('name')
    phone       = request.valid_data.get('phone')
    image       = request.valid_data.get('image')
    tags        = request.valid_data.get('tags')
    city_id     = request.valid_data.get('city_id')
    lng         = request.valid_data.pop('lng')
    lat         = request.valid_data.pop('lat')
    desc        = request.valid_data.get('desc')
    working_time= request.valid_data.get('working_time')
    long_lat    = '{},{}'.format(lng, lat)
    request.valid_data['long_lat']  = long_lat
    if item_id:
        print name
        ItemService.update_hospital(item_id, **request.valid_data)
    else:
        item_id = ItemService.create_hospital(**request.valid_data)

    return jsonify_response({'item_id': item_id})



recommend_item_validator  = Inputs(
    {
     'item_id'          : IdField(msg='商品id'),
     'recommend'        : BoolChoiceField(msg='是否推荐'),
    }
    )
@admin_json_dec(required=True, validator=recommend_item_validator)
def recommend_item():
    item_id         = request.valid_data.get('item_id')
    recommend       = request.valid_data.get('recommend')
    print item_id, recommend

    if recommend:
        ItemService.add_recommend_item(item_id)
    else:
        ItemService.rm_recommend_item(item_id)
    msg             = '推荐成功' if recommend else '取消推荐成功'
    result          = {
        'msg'          : msg
        }

    return jsonify_response(result)


recommend_hospital_validator  = Inputs(
    {
     'item_id'          : IdField(msg='医院id'),
     'recommend'        : BoolChoiceField(msg='是否推荐'),
    }
    )
@admin_json_dec(required=True, validator=recommend_hospital_validator)
def recommend_hospital():
    ''' 取消推荐医院 '''
    item_id         = request.valid_data.get('item_id')
    recommend       = request.valid_data.get('recommend')

    ItemService.rm_recommend_hospital(item_id)
    msg             = '取消推荐成功'
    result          = {
        'msg'           : msg,
        'code'          : ResponseCode.SUCCESS
        }

    return jsonify_response(result)



set_item_status_validator  = Inputs(
    {
     'item_id'          : IdField(msg='商品id'),
     'status'           : IntChoiceField(choices=[0,1], msg='商品状态'),
    }
    )
@admin_json_dec(required=True, validator=set_item_status_validator)
def set_item_status():
    item_id         = request.valid_data.get('item_id')
    status          = request.valid_data.get('status')
    print item_id, status
    data            = {
        'status': status
        }
    ItemService.update_item(item_id, **data)
    msg             = '上线成功' if status==1 else '下线成功'
    if status==0:
        ItemService.offline_item(item_id)
    result          = {
        'msg'           : msg
        }
    return jsonify_response(result)


user_list_validator  = Inputs(
    {
     'keyword'         : Optional(TextField(min_length=1, max_length=100, msg='搜索关键字')),
     'page'            : Optional(IdField(msg='页数')),
     'promoter_id'     : Optional(IdField(msg='推广员id')),
     'same_user_id'    : Optional(IdField(msg='相同用户注册id')),
    }
    )
@admin_json_dec(required=True, validator=user_list_validator, roles=[0,2,5])
def get_user_list():
    ''' 获取用户列表 '''
    keyword       = request.valid_data.get('keyword')
    promoter_id   = request.valid_data.get('promoter_id')
    page          = request.valid_data.get('page') or 1
    same_user_id  = request.valid_data.get('same_user_id')
    limit         = 10
    start         = (page-1)*limit
    where         = None
    filters       = []
    if keyword:
        filters.append(
            or_(
                User.name==keyword,
                User.phone==keyword
            )
        )
    if promoter_id:
        sub_q   = PromoteService.get_promoter_user_id_suq(promoter_id)
        filters.append(User.id.in_(sub_q))
    if filters: where = and_(*filters)
    if same_user_id:
        open_id = None
        qrcode_user = PromoteService.get_qrcode_user_by_user_id(same_user_id)
        if qrcode_user: open_id = qrcode_user.open_id
        suq     = PromoteService.open_id_user_ids_suq(open_id)
        where   = and_(
            User.id.in_(suq),
            User.id!=same_user_id
            )
    total         = UserService.count_user(where)
    page_info     = abbreviated_pages(int(math.ceil(total/(limit*1.0))), page)
    has_more, item_list = UserService.get_paged_user(limit=limit, start=start, where=where)
    fetch_wechatinfo_refs(item_list, id_='id', dest_key='wechat_info', keep_id=True)

    user_ids      = [i['id'] for i in item_list]
    open_ids      = PromoteService.get_open_ids_by_user_ids(user_ids)
    count_map            = PromoteService.count_open_id_user_count(open_ids)
    user_id_open_id_map  = PromoteService.get_user_id_open_id_map(open_ids)
    open_id_promoter_id_map= PromoteService.get_qrcodeusers_by_open_ids(open_ids)
    print user_id_open_id_map
    for info in item_list:
        open_id      = user_id_open_id_map.get(info['id'])
        if open_id:
            info['same_user_count'] = (count_map.get(open_id) or 1) -1
            info['open_id']         = open_id
            if open_id_promoter_id_map.get(open_id):
                info['promoter']        = open_id_promoter_id_map.get(open_id)['promoter']
            if open_id_promoter_id_map.get(open_id):
                info['parent']          = open_id_promoter_id_map.get(open_id)['parent']
        else:
            info['same_user_count'] = 0
    result               = {
        'infos'             : item_list,
        'page_info'         : page_info,
        'total'             : total,
        }

    return jsonify_response(result)


@admin_json_dec()
def get_user_detail():
    ''' 用户详情 '''
    item_id     = request.args.get('item_id')
    user        = UserService.get_user_by_id(item_id)
    assert user, '用户不存在'
    qruser      = PromoteService.get_qrcode_user_by_user_id(item_id)
    open_id     = None
    wechat_info = None
    location    = None
    if qruser:
        open_id = qruser.open_id
        if not qruser.nickname:
            try:
                PromoteService.set_user_sex(open_id)
                qruser = PromoteService.get_qrcode_user_by_user_id(item_id)
            except Exception as e:
                import traceback
                traceback.print_exc()
        if qruser and qruser.nickname:
            wechat_info = {}
            wechat_info['nickname']  = qruser.nickname
            wechat_info['sex']  = qruser.sex
            wechat_info['city']  = qruser.city
            wechat_info['headimgurl']  = qruser.headimgurl
    if open_id:
        try:
            from thirdparty.wechat import wechat
            location = PromoteService.get_first_location(open_id)
            from util.utils import translate_location
            if location:
                latlng = '{},{}'.format(location['lat'], location['lng'])
                result = translate_location(latlng)
                location = result.json()['result'][0]
        except Exception as e:
            import traceback
            traceback.print_exc()
    user        = user.as_dict()
    apply       = CreditService.get_apply_dict_by_userid(item_id)
    result      = {
        'data'     : user,
        'apply'    : apply,
        'location' : location,
        'wechat_info': wechat_info
        }
    return jsonify_response(result)



@admin_json_dec()
def get_school_city_list():
    ''' 学校省市列表 '''
    datas       = DataService.get_school_city_names()
    result      = {
        'infos': datas
        }
    return jsonify_response(result)


order_list_validator  = Inputs(
    {
     'hospital_id'          : Optional(IdField(msg='医院id')),
     'sub_cat_id'           : Optional(IdField(msg='子分类id')),
     'keyword'              : Optional(TextField(min_length=1, max_length=1000, msg='搜索订单号或用户手机号')),
     'order_status'         : Optional(IntChoiceField(choices=ORDER_ADMIN_STATUS_MAP.keys(), msg='订单筛选状态')),
    }
    )
@admin_json_dec(validator=order_list_validator)
def get_order_list():
    ''' 订单列表 '''
    page          = int(request.args.get('page', 1))
    hospital_id   = request.valid_data.get('hospital_id')
    sub_cat_id    = request.valid_data.get('sub_cat_id')
    keyword       = request.valid_data.get('keyword')
    order_status  = request.valid_data.get('order_status')
    limit         = 10
    start         = (page-1)*limit

    where         = None
    order_by      = None
    conditions    = []
    if hospital_id: conditions.append(Order.hospital_id==hospital_id)
    if keyword and len(keyword)==11:
        sub_query       = db.session.query(User.id).filter(User.phone==keyword).subquery()
        conditions.append(Order.user_id.in_(sub_query))
    elif keyword:
        conditions.append(Order.order_no==keyword)
    if order_status:
        if order_status==ORDER_ADMIN_STATUS.TO_PAY:
            conditions.append(Order.status.in_([ORDER_STATUS.NEW_ORDER, ORDER_STATUS.TO_PAY]))
        elif order_status==ORDER_ADMIN_STATUS.FINISH:
            conditions.append(Order.status==ORDER_STATUS.FINISH)
        elif order_status==ORDER_ADMIN_STATUS.TO_SERVE: #待服务
            conditions.append(and_(
                Order.status==ORDER_STATUS.PAY_SUCCESS,
                Order.credit_verified==1
                )
            )
        elif order_status==ORDER_ADMIN_STATUS.CREDIT_VERIFY: #额度待审核
            conditions.append(Order.credit_verified==0)
        elif order_status==ORDER_ADMIN_STATUS.CANCELD:
            conditions.append(Order.status.in_([ORDER_STATUS.CANCEL_BEFORE_PAY, ORDER_STATUS.CANCELED]))
        elif order_status==ORDER_ADMIN_STATUS.TO_REFUND:
            order_by    = [Order.refund.asc(), Order.id.desc()]
            sub_filter  = and_(
                PeriodPayLog.status==1
                )
            sub_q   = db.session.query(PeriodPayLog.order_id).filter(sub_filter).subquery()
            conditions.append(and_(
                Order.status==ORDER_STATUS.CANCELED,
                or_(
                    Order.price>0,
                    Order.id.in_(sub_q)
                ),
                #~(Order.refund==1), #分两部退款的可能某一次退款不成功
                )
            )
        else:
            conditions.append(Order.status==None)
    if sub_cat_id:
        sub_query       = db.session.query(Item.id).filter(Item.sub_cat_id==sub_cat_id).subquery()
        conditions.append(Order.item_id.in_(sub_query))
    if conditions:
        where           = and_(*conditions)

    total         = OrderService.count_order(where)
    page_info     = abbreviated_pages(int(math.ceil(total/(limit*1.0))), page)
    has_more, item_list = OrderService.get_paged_orders(
        order_by=order_by, limit=limit, start=start, where=where)

    fetch_servicecode_refrence(item_list, 'id', dest_key='service_code_dict', keep_id=True)

    for order in item_list:
        comment = None
        set_order_status(order, comment, order['service_code_dict'])
    trans_list(item_list, 'status', 'status_label', ORDER_STATUS_LABEL, pop=False)

    order_status_choices = ADMIN_ORDER_STATUS_CHOICES

    fetch_user_refs(item_list)
    fetch_item_refs(item_list)
    result              = {
        'infos'             : item_list,
        'page_info'         : page_info,
        'total'             : total,
        'order_status_choices': order_status_choices
        }

    return jsonify_response(result)


upload_image_validator  = Inputs(
    {
     'image'              : TextField(min_length=1, max_length=10000000, msg='图片')
    }
    )
@admin_json_dec(validator=upload_image_validator)
def upload_image():
    try:
        img_str = request.valid_data.pop('image')
        code    = 0
        msg     = '上传成功'
        print 'uploading...', len(img_str)
        content = b64decode(img_str.split(',')[1])
        key     = 'subcaticon/' + str(time.time())
        upload_img(key, content)
        return jsonify_response({'image': key, 'fullpath': prefix_img_domain(key)})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify_response({'msg':'服务器异常'})



@admin_json_dec()
def verify_chsi():
    ''' 验证chsi学信网 '''
    user_id         = request.args.get('user_id')
    apply           = CreditService.get_apply_dict_by_userid(user_id)
    chsi_name       = apply['chsi_name']
    chsi_passwd     = apply['chsi_passwd']
    data, success, return_captcha, session  = login_xuexin(chsi_name, chsi_passwd)

    ChsiCache.set(user_id, pickle.dumps(session))
    if return_captcha:
        data        = prefix_img_domain(data)
    msg             = '抓取成功' if success else '抓取失败'
    result          = {
        'code'          : ResponseCode.SUCCESS,
        'msg'           : msg,
        'success'       : success,
        'return_captcha': return_captcha,
        'data'          : data,
        }
    return jsonify_response(result)



set_chsi_captcha_validator  = Inputs(
    {
     'captcha'            : TextField(min_length=1, max_length=10000000, msg='验证码'),
     'apply_id'           : IdField(msg='申请id')
    }
    )
@admin_json_dec(validator=set_chsi_captcha_validator)
def set_chsi_captcha():
    ''' 输入验证码成功 '''
    captcha             = request.valid_data.get('captcha')
    apply_id            = request.valid_data.get('apply_id')

    apply               = CreditService.get_apply_dict_by_id(apply_id)
    chsi_name           = apply['chsi_name']
    chsi_passwd         = apply['chsi_passwd']
    user_id             = apply['user_id']

    session_pickle      = ChsiCache.get(user_id)
    session             = pickle.loads(session_pickle)

    msg                 = ''
    data                = get_chsi_info(chsi_name, chsi_passwd, captcha, session)
    result          = {
        'code'          : ResponseCode.SUCCESS,
        'msg'           : msg,
        'success'       : True,
        'data'          : data,
        }
    return jsonify_response(result)


@admin_json_dec(validator=None)
def refresh_captcha():
    ''' 刷新验证码 '''
    apply_id            = request.args.get('apply_id')
    apply               = CreditService.get_apply_dict_by_id(apply_id)
    session_pickle      = ChsiCache.get(apply['user_id'])
    session             = pickle.loads(session_pickle)

    print session
    print apply_id
    key                 = refresh_chsi_captcha(session)
    print key
    result          = {
        'code'          : ResponseCode.SUCCESS,
        'msg'           : '',
        'data'          : prefix_img_domain(key),
        }
    return jsonify_response(result)


@admin_json_dec()
def get_advice_list():
    ''' 反馈列表 '''
    limit         = 10
    page          = int(request.args.get('page', 1))
    start         = (page-1)*limit
    total         = UserService.count_advices()
    page_info     = abbreviated_pages(int(math.ceil(total/(limit*1.0))), page)
    has_more, item_list = UserService.get_paged_user_advices(limit=limit, start=start)

    fetch_user_refs(item_list)
    result               = {
        'infos'             : item_list,
        'page_info'         : page_info,
        'total'             : total,
        }

    return jsonify_response(result)


@admin_json_dec()
def get_advice_detail():
    ''' 反馈详情 '''
    advice_id   = request.args.get('advice_id')
    advice      = UserService.get_advice_dict_by_id(advice_id)
    fetch_user_refs((advice,))
    result      = {
        'data': advice
        }
    return jsonify_response(result)



refund_validator  = Inputs(
    {
     'order_id'           : IdField(msg='订单id')
    }
    )
@admin_json_dec(validator=refund_validator, roles=[0,1,5])
def admin_refund_order():
    ''' 退款 '''
    order_id        = request.valid_data.get('order_id')

    order           = OrderService.get_order_by_id(order_id)

    assert order and order.status==ORDER_STATUS.CANCELED, '订单不能退款'

    where           = and_(
        Order.id==order_id,
        Order.status==ORDER_STATUS.CANCELED
        )
    count           = OrderService.update_order(where, commit=True, refund=True)
    has_alipay      = False
    if order.pay_method==PAY_METHOD.ALIPAY:
        has_alipay  = True
        
    order_repayments= OrderService.get_order_repayment_logs_amount(order_id)
    repayment_amount= sum([format_price(i['price']) for i in order_repayments.values()] or [0])
    assert order.price or repayment_amount, '订单未曾支付过金额'
    sms_msg         = '首付金额{}'.format(format_price(order.price))
    if repayment_amount:
        sms_msg     = sms_msg + '和已还款金额{}'.format(repayment_amount)

    refund_data     = {}
    link            = ''
    for order_no in order_repayments:
        info        = order_repayments[order_no]
        if info['pay_method'] == PAY_METHOD.ALIPAY:
            has_alipay = True

    #微信支付 支付宝支付退款需要分两部进行
    if not has_alipay: assert count, '订单不能退款'

    msg             = ''
    if not has_alipay:
        for order_no in order_repayments:
            info        = order_repayments[order_no]
            pay_method  = info['pay_method']
            amount      = info['price']
            total_fee   = info['total']
            transaction_id  = info['transaction_id']
            if pay_method==PAY_METHOD.WECHAT_APP:
                result  = wxapp_refund_repayment(amount, total_fee, order_no, transaction_id)
            else:
                resullt = refund_repayment(amount, total_fee, order_no, transaction_id)
        if order.price:
            if order.pay_method==PAY_METHOD.WECHAT_APP:
                result          = refund_app_order(order)
            else:
                result          = refund_order(order)
        print result
        if result['result_code'] == 'SUCCESS':
            msg         = '退款成功'
            code        = ResponseCode.SUCCESS
            user        = UserService.get_user_by_id(order.user_id)
            send_sms_refund.delay(user.phone, order.order_no, sms_msg, '14个工作日')
        else:
            code        = ResponseCode.SERVER_ERROR
            msg         = '退款失败'
    else: #支付宝 微信混杂退款
        for order_no in order_repayments:
            info        = order_repayments[order_no]
            pay_method  = info['pay_method']
            amount      = info['price']
            total_fee   = info['total']
            transaction_id  = info['transaction_id']
            if pay_method==PAY_METHOD.ALIPAY:
                refund_data[transaction_id] = amount
            elif pay_method==PAY_METHOD.WECHAT_APP:
                wxapp_refund_repayment(amount, total_fee, order_no, transaction_id)
            else:
                refund_repayment(amount, total_fee, order_no, transaction_id)
        if order.pay_method==PAY_METHOD.WECHAT_WEB:
            result          = refund_order(order)
        elif order.pay_method==PAY_METHOD.WECHAT_APP:
            result          = refund_app_order(order)
        else:
            refund_data[order.transaction_id] = format_price(order.price)
        from thirdparty.alipay import alipay
        link            = alipay.refund_order(refund_data, '美分分订单退款')
        msg             = '跳转到支付宝商户后台退款'

    result          = {
        'code'  : ResponseCode.SUCCESS,
        'msg'   : msg,
        'refund_data': refund_data,
        'link'  : link,
        'has_alipay': has_alipay
        }
    return jsonify_response(result)



del_item_activity_validator  = Inputs(
    {
     'item_id'           : IdField(msg='商品id')
    }
    )
@admin_json_dec(validator=del_item_activity_validator)
def del_item_activity():
    item_id     = request.valid_data.get('item_id')
    ActivityService.del_item_activitys(item_id, None)
    result      = {
        'code'     : ResponseCode.SUCCESS,
        'msg'      : '从活动移除商品成功'
    }
    return jsonify_response(result)


@admin_json_dec()
def get_activity_list():
    ''' 活动列表 ''' 
    limit         = 10
    page          = int(request.args.get('page', 1))
    start         = (page-1)*limit
    total         = ActivityService.count_activitys()
    page_info     = abbreviated_pages(int(math.ceil(total/(limit*1.0))), page)

    has_more, item_list = ActivityService.get_paged_activitys(limit=limit, start=start)

    result               = {
        'infos'             : item_list,
        'page_info'         : page_info,
        'total'             : total,
        }

    return jsonify_response(result)


@admin_json_dec()
def get_activity_items():
    ''' 活动商品列表 '''
    limit                   = 1000
    activity_id             = int(request.args.get('activity_id', 1))
    where                   = ActivityItem.activity_id==activity_id
    has_more, infos         = ActivityService.get_paged_activity_items(where=where, limit=limit)

    fields                  = ['id', 'title']
    has_more,   items       = ItemService.get_paged_items(limit=limit, fields=fields)

    selected                = set(i['item_id'] for i in infos)
    for i in items:
        i['selected']       = i['id'] in selected
        i['label']          = i['title']

    result                  = {
        'infos'             : items,
        }

    return jsonify_response(result)


set_activity_items_validator  = Inputs(
    {
     'activity_id'          : IdField(msg='活动id'),
     'ids'                  : IntChoicesField(all=True, msg='商品id列表')
    }
    )
@admin_json_dec(validator=set_activity_items_validator)
def set_activity_items():
    ''' 设置活动商品列表 '''
    item_ids            = request.valid_data.get('ids')
    activity_id         = request.valid_data.get('activity_id')

    print item_ids, activity_id

    ActivityService.set_activity_items(activity_id, item_ids)

    result              = {
        'code'              : ResponseCode.SUCCESS,
        'msg'               : '编辑成功'
        }
    return jsonify_response(result)



activity_edit_validator  = Inputs(
    {
     'title'         : TextField(min_length=1, max_length=100, msg='活动标题'),
     'desc'          : TextField(min_length=1, max_length=10000, msg='活动描述'),
     'start_time'    : TextField(min_length=1, max_length=100, msg='开始时间'),
     'end_time'      : TextField(min_length=1, max_length=100, msg='结束时间'),
    }
    )
@admin_json_dec(required=True, validator=activity_edit_validator)
def activity_edit(item_id=None):
    title           = request.valid_data.get('title')
    desc            = request.valid_data.get('desc')
    start_time      = request.valid_data.get('start_time')
    end_time        = request.valid_data.get('end_time')
    if not item_id:
        assert not ActivityService.exists_activity_time(start_time, end_time), '时间范围已存在'
        item_id     = ActivityService.create_activity(title, desc, start_time, end_time)
        msg         = '添加成功'
    else:
        assert not ActivityService.exists_activity_time(start_time, end_time, item_id), '时间范围已存在'
        ActivityService.update_activity(item_id, **request.valid_data)
        msg         = '修改成功'
    result          = {
        'code'          : ResponseCode.SUCCESS,
        'item_id'       : item_id,
        'msg'           : msg
        }
    return jsonify_response(result)


def get_activity():
    item_id         = request.args.get('item_id')
    activity        = ActivityService.get_activity_dict_by_id(item_id)

    result          = {
        'data':activity
        }
    return jsonify_response(result)


top_recommend_item_validator  = Inputs(
    {
     'item_id'       : IdField(msg='商品id'),
    }
    )
@admin_json_dec(validator=top_recommend_item_validator)
def top_recommend_item():
    ''' 置顶推荐 '''
    item_id         = request.valid_data.get('item_id')
    ItemService.top_recommend_item(item_id)

    result          = {
        'code'  : ResponseCode.SUCCESS,
        'msg'   : '置顶成功'
        }
    return jsonify_response(result)



top_recommend_subcat_validator  = Inputs(
    {
     'sub_cat_id'       : IdField(msg='子分类id'),
    }
    )
@admin_json_dec(validator=top_recommend_subcat_validator)
def top_recommend_subcat():
    ''' 子分类 '''
    sub_cat_id         = request.valid_data.get('sub_cat_id')
    ItemService.top_recommend_subcat(sub_cat_id)

    result          = {
        'code'  : ResponseCode.SUCCESS,
        'msg'   : '置顶成功'
        }
    return jsonify_response(result)



recommend_subcat_validator  = Inputs(
    {
     'item_id'       : IdField(msg='子分类id'),
     'recommend'        : BoolChoiceField(msg='是否推荐'),
    }
    )
@admin_json_dec(required=True, validator=recommend_subcat_validator)
def recommend_subcat():
    sub_cat_id      = request.valid_data.get('item_id')
    recommend       = request.valid_data.get('recommend')
    print sub_cat_id, recommend

    if recommend:
        ItemService.add_recommend_subcat(sub_cat_id)
    else:
        ItemService.rm_recommend_subcat(sub_cat_id)
    msg             = '推荐成功' if recommend else '取消推荐成功'
    result          = {
        'msg'          : msg
        }


@admin_json_dec()
def get_item_recommend():
    item_id         = int(request.args.get('item_id'))

    data            = ItemService.get_item_recommend(item_id) or dict(item_id=item_id)

    if data: fetch_item_refs((data,))
    result          = {
        'data'         : data
        }
    return jsonify_response(result)


@admin_json_dec()
def get_hospital_recommend():
    hospital_id         = int(request.args.get('hospital_id'))

    data            = ItemService.get_hospital_recommend(hospital_id) or dict(hospital_id=hospital_id)

    if data: fetch_hospital_refs((data,))
    result          = {
        'data'         : data
        }
    return jsonify_response(result)


@admin_json_dec()
def get_item_activity():
    item_id         = int(request.args.get('item_id'))

    data            = ItemService.get_item_activity(item_id) or dict(item_id=item_id)

    if data: fetch_item_refs((data,))
    result          = {
        'data'         : data
        }
    return jsonify_response(result)


@admin_json_dec()
def get_subcat_recommend():
    sub_cat_id      = int(request.args.get('sub_cat_id'))
    data            = ItemService.get_subcat_recommend(sub_cat_id) or dict(sub_cat_id=sub_cat_id)
    if data: fetch_item_subcat_refs((data, ))
    result          = {
        'data'         : data
        }
    return jsonify_response(result)



item_activity_edit_validator  = Inputs(
    {
     'sort_order'       : IntField(msg='排序'),
     'activity_id'      : IdField(msg='活动id'),
     'image'            : TextField(min_length=1, max_length=1000, msg='图片'),
     'price'            : FloatField(msg='活动价格'),
    }
    )
@admin_json_dec(validator=item_activity_edit_validator)
def item_activity_edit(item_id=None):
    sort_order  = request.valid_data.get('sort_order')
    activity_id = request.valid_data.get('activity_id')
    price       = request.valid_data.get('price')
    image       = request.valid_data.get('image')

    item_activity = ItemService.get_item_activity(item_id)
    if not item_activity:
        ItemService.add_activity_item(item_id, sort_order, activity_id, price, image)
    else:
        ActivityService.del_item_activitys(item_id, item_activity['activity_id'])
        ItemService.update_activity_item(item_id, **request.valid_data)

    msg         = '编辑成功'
    result      = {
        'msg'      : msg
        }
    return jsonify_response(result)



item_recommend_edit_validator  = Inputs(
    {
     'sort_order'       : IntField(msg='排序'),
     'image'            : TextField(min_length=1, max_length=1000, msg='图片'),
     'desc'             : TextField(min_length=1, max_length=1000, msg='描述')
    }
    )
@admin_json_dec(validator=item_recommend_edit_validator)
def item_recommend_edit(item_id=None):
    image       = request.valid_data.get('image')
    desc        = request.valid_data.get('desc')
    sort_order  = request.valid_data.get('sort_order')

    recommend   = ItemService.get_item_recommend(item_id)
    DataService.set_img_size.delay(image)
    if not recommend:
        ItemService.add_recommend_item(item_id, sort_order, image, desc)
    else:
        ItemService.update_recommend_item(item_id, **request.valid_data)

    msg         = '编辑成功'
    result      = {
        'msg'      : msg
        }
    return jsonify_response(result)


subcat_recommend_edit_validator  = Inputs(
    {
     'sort_order'       : IntField(msg='排序'),
     'icon'             : TextField(min_length=1, max_length=1000, msg='图片'),
    }
    )
@admin_json_dec(validator=subcat_recommend_edit_validator)
def subcat_recommend_edit(item_id=None):
    icon        = request.valid_data.get('icon')
    sort_order  = request.valid_data.get('sort_order')

    recommend   = ItemService.get_subcat_recommend(item_id)
    if not recommend:
        ItemService.add_recommend_subcat(item_id, sort_order, icon)
    else:
        ItemService.update_recommend_subcat(item_id, **request.valid_data)

    msg         = '编辑成功'
    result      = {
        'msg'      : msg
        }
    return jsonify_response(result)


hospital_recommend_edit_validator  = Inputs(
    {
     'sort_order'       : IntField(msg='排序'),
     'color'            : TextField(min_length=1, max_length=1000, msg='颜色'),
     'tag'              : TextField(min_length=1, max_length=1000, msg='标签'),
    }
    )
@admin_json_dec(validator=hospital_recommend_edit_validator)
def hospital_recommend_edit(item_id=None):
    tag         = request.valid_data.get('tag')
    color       = request.valid_data.get('color')
    sort_order  = request.valid_data.get('sort_order')

    recommend   = ItemService.get_hospital_recommend(item_id)
    if not recommend:
        ItemService.add_recommend_hospital(item_id, sort_order, color, tag)
    else:
        ItemService.update_recommend_hospital(item_id, **request.valid_data)

    msg         = '编辑成功'
    result      = {
        'msg'      : msg
        }
    return jsonify_response(result)



set_recommend_order_validator  = Inputs(
    {
     'sort_order'       : IntField(msg='排序'),
     'item_id'          : IdField(msg='商品id'),
    }
    )
@admin_json_dec(validator=set_recommend_order_validator)
def set_recommend_order():
    item_id         = request.valid_data.get('item_id')
    sort_order      = request.valid_data.get('sort_order')

    exist           = ItemService.check_exist_order(sort_order)
    assert not exist, '排序值已存在'
    ItemService.update_recommend_item(item_id, sort_order=sort_order)

    result          = {
        'code'          : ResponseCode.SUCCESS,
        'msg'           : '修改成功'
    }
    return jsonify_response(result)


set_trial_order_validator  = Inputs(
    {
     'sort_order'       : IntField(msg='排序'),
     'item_id'          : IdField(msg='商品id'),
    }
    )
@admin_json_dec(validator=set_trial_order_validator)
def set_trial_order():
    item_id         = request.valid_data.get('item_id')
    sort_order      = request.valid_data.get('sort_order')

    exist           = TrialService.check_exist_order(sort_order)
    assert not exist, '排序值已存在'
    TrialService.update_trial(item_id, sort_order=sort_order)

    result          = {
        'code'          : ResponseCode.SUCCESS,
        'msg'           : '修改成功'
    }
    return jsonify_response(result)




set_recommend_subcat_order_validator  = Inputs(
    {
     'sort_order'       : IntField(msg='排序'),
     'item_id'          : IdField(msg='子分类id'),
    }
    )
@admin_json_dec(validator=set_recommend_subcat_order_validator)
def set_recommend_subcat_order():
    item_id         = request.valid_data.get('item_id')
    sort_order      = request.valid_data.get('sort_order')

    exist           = ItemService.check_exist_subcat_order(sort_order)
    assert not exist, '排序值已存在'
    ItemService.update_recommend_subcat(item_id, sort_order=sort_order)

    result          = {
        'code'          : ResponseCode.SUCCESS,
        'msg'           : '修改成功'
    }
    return jsonify_response(result)


set_recommend_hospital_order_validator  = Inputs(
    {
     'sort_order'       : IntField(msg='排序'),
     'item_id'          : IdField(msg='医院id'),
    }
    )
@admin_json_dec(validator=set_recommend_hospital_order_validator)
def set_recommend_hospital_order():
    item_id         = request.valid_data.get('item_id')
    sort_order      = request.valid_data.get('sort_order')

    exist           = ItemService.check_exist_hospital_order(sort_order)
    assert not exist, '排序值已存在'
    ItemService.update_recommend_hospital(item_id, sort_order=sort_order)

    result          = {
        'code'          : ResponseCode.SUCCESS,
        'msg'           : '修改成功'
    }
    return jsonify_response(result)


def get_period_pay_log_list():
    ''' 逾期分期帐单列表 '''
    limit                   = 10
    page                    = int(request.args.get('page') or 1)
    keyword                 = request.args.get('keyword', '')
    is_delayed              = request.args.get('is_delayed')=='true'
    start                   = (page-1)*limit

    deadline                = get_due_time(0)
    where                   = and_()
    if is_delayed:
        where.append(and_(#逾期为还的
            PeriodPayLog.repayment_time==None,
            PeriodPayLog.deadline<deadline,
            PeriodPayLog.status==0
            ))

    if keyword:
        user                = UserService.get_user_by_phone(keyword)
        user_id             = None
        if user: user_id    = user.id
        where.append(PeriodPayLog.user_id==user_id)
    has_more, infos         = CreditService.get_paged_period_pay_logs(where=where, limit=limit, start=start)
    fetch_order_refs(infos)
    for log in infos:
        log['item_id']      = log['order']['item_id']
    fetch_item_refs(infos, fields=['id', 'title'])
    fetch_user_refs(infos)
    for i in infos:
        cacl_punish_fee(i)

    total         = CreditService.count_logs(where)
    page_info     = abbreviated_pages(int(math.ceil(total/(limit*1.0))), page)

    result                  = {
        'msg'               : '',
        'code'              : ResponseCode.SUCCESS,
        'infos'             : infos,
        'total'             : total,
        'page_info'         : page_info
        }

    return jsonify_response(result)


@admin_json_dec(required=True)
def get_refund_detail():
    order_id        = request.args.get('order_id')

    order           = OrderService.get_order_by_id(order_id)

    assert order and order.status==ORDER_STATUS.CANCELED, '订单不能退款'

    order_repayments= OrderService.get_order_repayment_logs_amount(order_id)
    repayment_amount= sum([format_price(i['price']) for i in order_repayments.values()] or [0])

    refund_data     = {}
    wechat_web      = {}
    wechat_app      = {}
    link            = ''
    has_alipay      = False
    for order_no in order_repayments:
        info        = order_repayments[order_no]
        if info['pay_method'] == PAY_METHOD.ALIPAY:
            has_alipay = True
    if order.pay_method==PAY_METHOD.ALIPAY: has_alipay=True
    if has_alipay:
        for order_no in order_repayments:
            info        = order_repayments[order_no]
            pay_method  = info['pay_method']
            amount      = info['price']
            total_fee   = info['total']
            transaction_id  = info['transaction_id']
            if pay_method==PAY_METHOD.ALIPAY:
                refund_data[transaction_id] = amount
            elif pay_method==PAY_METHOD.WECHAT_APP:
                wechat_app[transaction_id]  = amount
            elif pay_method==PAY_METHOD.WECHAT_WEB:
                wechat_web[transaction_id]  = amount

    result          = {
        'code'         : ResponseCode.SUCCESS,
        'msg'          : '',
        'has_alipay'    : has_alipay,
        'order_repayments'          : order_repayments,
        'wechat_app'                : wechat_app,
        'wechat_web'                : wechat_web,
        'repayment_amount'          : repayment_amount,
        'price'                     : format_price(order.price)
        }
    return jsonify_response(result)



@admin_json_dec(required=True)
def get_coupon_list():
    ''' '''
    limit                   = 10
    page                    = int(request.args.get('page') or 1)
    start                   = (page-1)*limit

    has_more, infos         = CouponService.get_paged_coupons(start=start, limit=limit)
    total                   = CouponService.count(None)
    page_info               = abbreviated_pages(int(math.ceil(total/(limit*1.0))), page)

    fetch_item_subcat_refs(infos)
    fetch_item_refs(infos, fields=['id', 'title'])
    fetch_item_cat_refs(infos)

    result                  = {
        'msg'               : '',
        'code'              : ResponseCode.SUCCESS,
        'infos'             : infos,
        'total'             : total,
        'page_info'         : page_info
        }

    return jsonify_response(result)


coupon_edit_validator  = Inputs(
    {
     'title'         : TextField(min_length=1, max_length=100, msg='商品名'),
     'cat_id'        : Optional(IdField(msg='分类id')),
     'is_trial'      : IntChoiceField(choices=[0, 1], msg='是否试用'),
     'sub_cat_id'    : Optional(IdField(msg='子分类id')),
     'item_id'       : Optional(IdField(msg='商品id')),
     'coupon_cat'    : IdField(msg='优惠券类型'),
     'price'         : Optional(FloatField(msg='优惠金额')),
     'need'          : Optional(IntField(msg='满多少使用')),
     'effective'     : IntField(msg='有效期')
    }
    )
@admin_json_dec(required=True, validator=coupon_edit_validator, roles=[0,1])
def coupon_edit(item_id=None):
    title           = request.valid_data.get('title')
    cat_id          = request.valid_data.get('cat_id')
    sub_cat_id      = request.valid_data.get('sub_cat_id')
    mff_item_id     = request.valid_data.get('item_id')
    price           = request.valid_data.get('price') or 0
    need            = request.valid_data.get('need') or 0
    effective       = request.valid_data.get('effective')
    effective       = effective * 86400
    request.valid_data['effective'] = effective
    coupon_cat      = request.valid_data.get('coupon_cat')
    is_trial        = request.valid_data.get('is_trial')
    request.valid_data['price'] = price
    if not is_trial:
        assert price, '请输入优惠金额'

    if coupon_cat==1: assert cat_id, '请选择商品分类'
    if coupon_cat==2: assert sub_cat_id, '请选择商品子分类'
    if coupon_cat==3:
        assert mff_item_id, '请输入商品id'
        item            = ItemService.get_item_dict_by_id(mff_item_id)
        assert item, '商品不存在'
    if not item_id:
        coupon_id       = CouponService.create_coupon(
            coupon_cat, cat_id, title, price, effective,
            mff_item_id, sub_cat_id, is_trial, need=need)
    else:
        CouponService.update_coupon(item_id, **request.valid_data)
    result          = {
        'code'      : ResponseCode.SUCCESS,
        'msg'       : ''
    }
    return jsonify_response(result)



city_edit_validator  = Inputs(
    {
     'name'          : TextField(min_length=1, max_length=100, msg='城市名'),
     'city_code'          : TextField(min_length=1, max_length=100, msg='百度城市编码'),
     'amap_code'          : TextField(min_length=1, max_length=100, msg='高德城市编码'),
    }
    )
@admin_json_dec(required=True, validator=city_edit_validator, roles=[0,1])
def city_edit(item_id=None):
    name            = request.valid_data.get('name')
    city_code       = request.valid_data.get('city_code')
    amap_code       = request.valid_data.get('amap_code')

    if not item_id:
        DataService.create_city(name, city_code, amap_code)
    else:
        DataService.update_city(item_id, **request.valid_data)
    result          = {
        'code'      : ResponseCode.SUCCESS,
        'msg'       : ''
    }
    return jsonify_response(result)


def get_city():
    ''' 获取城市 '''
    city_id        = request.args.get('item_id')
    city           = DataService.get_city_dict_by_id(city_id)
    assert city, '城市不存在'
    result          = {
        'data':      city}
    return jsonify_response(result)


def get_coupon():
    ''' '''
    item_id         = request.args.get('item_id')
    coupon          = CouponService.get_coupon(item_id)
    result          = {
        'data':      coupon}
    return jsonify_response(result)




trial_edit_validator  = Inputs(
    {
     'title'         : TextField(min_length=1, max_length=100, msg='商品名'),
     'image'         : TextField(min_length=1, max_length=1000, msg='商品小图'),
     'rules'         : TextField(min_length=1, max_length=1000000, msg='攻略'),
     'process'       : TextField(min_length=1, max_length=1000000, msg='流程'),
     'start_time'    : TextField(min_length=1, max_length=10000, msg='开始时间'),
     'end_time'      : TextField(min_length=1, max_length=10000, msg='结束时间'),
     'cat'           : IntChoiceField(choices=[0,1], msg='是否免息'),
     'total'         : IntField(msg='总共'),
     'coupon_id'     : Optional(IdField(msg='子分类id')),
    }
    )
@admin_json_dec(required=True, validator=trial_edit_validator)
def trial_edit(item_id=None):
    title           = request.valid_data.get('title')
    image           = request.valid_data.get('image')
    rules           = request.valid_data.get('rules')
    cat             = request.valid_data.get('cat')
    need            = request.valid_data.get('need') or 0
    total           = request.valid_data.get('total')
    coupon_id       = request.valid_data.get('coupon_id')
    total           = request.valid_data.get('total')
    end_time        = request.valid_data.get('end_time')
    start_time      = request.valid_data.get('start_time')
    process         = request.valid_data.get('process')

    print start_time, end_time
    print start_time<end_time
    assert start_time[:16]<end_time[:16], '开始时间必须前于结束时间'
    if cat==1:
        assert coupon_id, '请选择优惠券'
        coupon      = CouponService.get_coupon(coupon_id)
        assert coupon, '优惠券不存在'
        assert coupon['item_id'], '优惠券类型必须为指定商品'

    if not item_id:
        trial_id    = TrialService.create_trial(
            title, image, cat, total, start_time,
            end_time, rules, process, coupon_id=coupon_id,
            need=need
            )
    else:
        trial       = TrialService.get_trial(item_id)
        assert trial, '申请不存在'
        assert total>trial['sent'], '不能低于已发放数'
        TrialService.update_trial(item_id, **request.valid_data)
    result          = {
        'code'          : ResponseCode.SUCCESS,
        'msg'           : ''
    }
    return jsonify_response(result)


@admin_json_dec(required=True)
def get_trial_list():
    ''' '''
    limit                   = 10
    page                    = int(request.args.get('page') or 1)
    start                   = (page-1)*limit

    _sort                   = 'end_time'
    _sort_dir               = 'DESC'
    has_more, infos         = TrialService.get_paged_trials(start=start, limit=limit, _sort=_sort, _sort_dir=_sort_dir)

    total                   = TrialService.count_trial(where=None)
    page_info               = abbreviated_pages(int(math.ceil(total/(limit*1.0))), page)
    current_time            = dt_obj.now()

    result                  = {
        'msg'               : '',
        'now'               : str(current_time),
        'code'              : ResponseCode.SUCCESS,
        'infos'             : infos,
        'total'             : total,
        'page_info'         : page_info
        }

    return jsonify_response(result)


@admin_json_dec(required=True)
def get_trial():
    ''' '''
    trial_id                = request.args.get('item_id')
    trial                   = TrialService.get_trial(trial_id)
    result                  = {
        'code'             : ResponseCode.SUCCESS,
        'data'             : trial,
        'msg'              : ''
    }
    return jsonify_response(result)



@admin_json_dec()
def trial_applyer_list():
    ''' 申请用户列表 '''
    limit               = 10
    page                = int(request.args.get('page') or 1)
    start                   = (page-1)*limit

    item_id             = request.args.get('item_id')
    trial               = TrialService.get_trial(item_id)

    where               = TrialApply.trial_id==item_id
    has_more, infos     = TrialService.get_paged_apply_user_list(where=where, start=start)
    user_ids            = [i['user_id'] for i in infos]
    apply_count_map     = TrialService.count_user_apply(user_ids)
    apply_received_count_map     = TrialService.count_user_apply(user_ids, 1)
    for info in infos:
        apply_count          = apply_count_map.get(info['user_id'], 0)
        apply_received_count = apply_received_count_map.get(info['user_id'], 0)
        info['apply_count']  = apply_count
        info['apply_received_count'] = apply_received_count
    total               = TrialService.count_apply(where)
    page_info           = abbreviated_pages(int(math.ceil(total/(limit*1.0))), page)
    result              = {
        'code'            : ResponseCode.SUCCESS,
        'item'            : trial,
        'infos'           : infos,
        'total'           : total,
        'page_info'       : page_info,
        'has_more'        : has_more,
        'msg'             : ''
    }
    return jsonify_response(result)



@admin_json_dec()
def daily_applyer_list():
    ''' 每日领取优惠券用户列表 '''
    limit               = 10
    page                = int(request.args.get('page') or 1)
    start                   = (page-1)*limit

    item_id             = request.args.get('item_id')
    item                = TutorialService.get_daily_coupon(item_id)

    where               = DailyUser.daily_id==item_id
    has_more, infos     = TutorialService.get_daily_user_ids(where=where, start=start)
    total               = TutorialService.count_daily_users(where)

    fetch_user_refs(infos)
    page_info           = abbreviated_pages(int(math.ceil(total/(limit*1.0))), page)
    result              = {
        'code'            : ResponseCode.SUCCESS,
        'item'            : item,
        'infos'           : infos,
        'total'           : total,
        'page_info'       : page_info,
        'has_more'        : has_more,
        'msg'             : ''
    }
    return jsonify_response(result)


send_trial_validator  = Inputs(
    {
     'apply_id'      : IdField(msg='申请id'),
     'item_id'       : IdField(msg='试用id'),
    }
    )
@admin_json_dec(validator=send_trial_validator, roles=[0,1,3])
def send_trial():
    ''' 赠送申请 '''
    apply_id        = request.valid_data.get('apply_id')
    item_id         = request.valid_data.get('item_id')

    trial           = TrialService.get_trial(item_id)
    assert trial, '试用不存在'
    apply           = TrialService.get_apply(apply_id)
    assert apply, '申请不存在'

    where           = and_(
        TrialApply.id==apply_id,
        TrialApply.status==0
        )
    to_status       = 1
    count           = TrialService.update_apply_status(where, to_status)
    if count:
        TrialService.incr_trial_sent_count(item_id)
        if trial['cat']==1:
            user_coupon_id  = CouponService.send_user_coupon(apply['user_id'], trial['coupon_id'])
            TrialService.update_apply(TrialApply.id==apply_id, coupon_id=user_coupon_id)
        msg         = '发放成功'
    else:
        apply       = TrialService.get_apply(apply_id)
        if apply['status'] in {1,2,3}:
            msg     = '已发放给该用户'
        else:
            msg     = '发放失败'

    result          = {
        'code'         : ResponseCode.SUCCESS,
        'msg'          : msg
        }
    return jsonify_response(result)


@admin_json_dec()
def get_promoter_list():
    ''' 推广管理员列表 '''
    limit               = 10
    page                = int(request.args.get('page') or 1)
    start               = (page-1)*limit

    where               = Promoter.status==1
    has_more, infos     = PromoteService.get_paged_promoters(where=where, start=start, limit=limit)
    promoter_ids        = [ i['id'] for i in infos ]
    count               = PromoteService.count_promoter_admin_reg(promoter_ids)
    follow_count_map    = {i[0]:int(i[1]) for i in count}
    reg_count_map       = {i[0]:int(i[2]) for i in count}
    for info in infos:
        info['follow_count_total'] = follow_count_map.get(info['id'])
        info['reg_count_total']    = reg_count_map.get(info['id'])
        if info['id']==1:
            promoter = PromoteService.get_promoter_by_phone('18801794295')
            if promoter:
                info['follow_count_total'] = promoter.follow_count
                info['reg_count_total'] = promoter.reg_count
    total               = PromoteService.count_promoters(where)
    page_info           = abbreviated_pages(int(math.ceil(total/(limit*1.0))), page)
    result              = {
        'code'            : ResponseCode.SUCCESS,
        'infos'           : infos,
        'total'           : total,
        'page_info'       : page_info,
        'has_more'        : has_more,
        'msg'             : ''
    }
    return jsonify_response(result)


add_promoter_validator  = Inputs(
    {
     'name'        : TextField(min_length=1, max_length=100, msg='请输入用户名'),
     'phone'       : MobileField(min_length=1, max_length=100, msg='请输入手机号'),
     'passwd'      : TextField(min_length=1, max_length=100, msg='请输入密码'),
    }
    )
@admin_json_dec(validator=add_promoter_validator)
def add_promoter():
    ''' 添加推广员 '''
    name            = request.valid_data.get('name')
    phone           = request.valid_data.get('phone')
    passwd          = request.valid_data.get('passwd')
    PromoteService.create_promoter(phone, passwd, name)

    result          = {
        'code'         : ResponseCode.SUCCESS,
        'msg'          : ''
    }
    return jsonify_response(result)



@admin_json_dec()
def get_hospital_user_list():
    ''' 医院管理员列表 '''
    limit               = 10
    page                = int(request.args.get('page') or 1)
    start               = (page-1)*limit

    where               = None
    has_more, infos     = HospitalService.get_paged_hospital_admin_users(where=where, start=start)

    fetch_hospital_refs(infos)
    total               = HospitalService.count_admin(where)
    page_info           = abbreviated_pages(int(math.ceil(total/(limit*1.0))), page)
    result              = {
        'code'            : ResponseCode.SUCCESS,
        'infos'           : infos,
        'total'           : total,
        'page_info'       : page_info,
        'has_more'        : has_more,
        'msg'             : ''
    }
    return jsonify_response(result)


add_hospital_admin_validator  = Inputs(
    {
     'name'        : TextField(min_length=1, max_length=100, msg='请输入用户名'),
     'hospital_id' : IdField(msg='医院id'),
     'passwd'      : TextField(min_length=1, max_length=100, msg='请输入密码'),
    }
    )
@admin_json_dec(validator=add_hospital_admin_validator, roles=[0,1])
def add_hospital_admin():
    ''' 添加医院管理员 '''
    name            = request.valid_data.get('name')
    passwd          = request.valid_data.get('passwd')
    hospital_id     = request.valid_data.get('hospital_id')

    HospitalService.create_user(name, passwd, hospital_id)

    result          = {
        'code'         : ResponseCode.SUCCESS,
        'msg'          : ''
    }
    return jsonify_response(result)



to_supply_validator  = Inputs(
    {
     'apply_id' : IdField(msg='申请id'),
    }
    )
@admin_json_dec(validator=to_supply_validator, roles=[0,1])
def to_supply():
    ''' 补充资料 '''
    apply_id     = request.valid_data.get('apply_id')

    where       = and_(
        CreditApply.id==apply_id,
        )
    data        = {
        'status':APPLY_STATUS.SECOND_STEP
        }
    CreditService.update_apply(where, **data)
    result          = {
        'code'         : ResponseCode.SUCCESS,
        'msg'          : ''
    }
    return jsonify_response(result)




supply_apply_validator  = Inputs(
    {
    'apply_id'           : IdField(msg='申请id'),
    'id_no'              : TextField(min_length=0, max_length=100, msg='身份证号'),
    'school'             : TextField(min_length=0, max_length=100, msg='学校'),
    'enrollment_time'    : TextField(min_length=0, max_length=100, msg='入学时间'),
    'graduate_time'      : TextField(min_length=0, max_length=100, msg='毕业时间'),
    'name'               : TextField(min_length=0, max_length=100, msg='真实姓名'),
    'major'              : TextField(min_length=0, max_length=100, msg='专业'),
    'stu_no'             : TextField(min_length=0, max_length=100, msg='学号'),
    'stu_years'          : FloatField(msg='学制请输入浮点数如：4'),
    'stu_education'      : TextField(min_length=0, max_length=100, msg='学历'),
    }
    )
@admin_json_dec(validator=supply_apply_validator)
def supply_apply():
    apply_id        = request.valid_data.pop('apply_id')
    try:
        request.valid_data['enrollment_time'] = '{} 00:00:00'.format(request.valid_data['enrollment_time'])
        request.valid_data['graduate_time']   = '{} 00:00:00'.format(request.valid_data['graduate_time'])
        format                                = '%Y-%m-%d %H:%M:%S'
        request.valid_data['graduate_time']   = date_to_datetime(request.valid_data['graduate_time'], format)
        request.valid_data['enrollment_time'] = date_to_datetime(request.valid_data['enrollment_time'], format)
    except Exception as e:
        assert 0, '入学时间，毕业时间输入有误，请按格式2015-09-01输入'
    assert len(request.valid_data['id_no'])==18, '身份证号码长度有误'
    where      = and_(
        CreditApply.id==apply_id,
        )
    request.valid_data['update_time'] = dt_obj.now()
    request.valid_data['has_supply']  = True
    count          = CreditService.update_apply(where, **request.valid_data)
    result         = {
        'code'        : ResponseCode.SUCCESS,
        'msg'         : '补充成功' if count else '申请不存在'
    }
    return jsonify_response(result)


set_hospital_status_validator  = Inputs(
    {
     'item_id'          : IdField(msg='医院id'),
     'status'           : IntChoiceField(choices=[0,1], msg='医院状态'),
    }
    )
@admin_json_dec(required=True, validator=set_hospital_status_validator)
def set_hospital_status():
    item_id         = request.valid_data.get('item_id')
    status          = request.valid_data.get('status')
    print item_id, status
    data            = {
        'status': status
        }
    msg             = '上线成功' if status==1 else '下线成功'
    count           = ItemService.set_hospital_status(item_id, status)
    assert count, '医院不存在'
    if status==1:
        where       = and_(
            Item.hospital_id==item_id,
            Item.status==2
            )
        ItemService.set_hospital_item_status(where, 1)
    else:
        where       = and_(
            Item.hospital_id==item_id,
            Item.status==1
            )
        ItemService.set_hospital_item_status(where, 2)
    result          = {
        'msg'           : msg,
        'code'          : ResponseCode.SUCCESS
        }
    return jsonify_response(result)


@admin_json_dec(required=True)
def get_daily_coupon_list():
    ''' 每日领取优惠券列表 '''
    limit                   = 10
    page                    = int(request.args.get('page') or 1)
    start                   = (page-1)*limit

    _sort                   = 'start_time'
    has_more, infos         = TutorialService.get_paged_daily_coupons(_sort=_sort, start=start, limit=limit)
    total                   = TutorialService.count_daily_coupons(None)
    page_info               = abbreviated_pages(int(math.ceil(total/(limit*1.0))), page)
    fetch_coupon_refs(infos)
    set_coupon_use_time(infos)
    result                  = {
        'msg'               : '',
        'code'              : ResponseCode.SUCCESS,
        'infos'             : infos,
        'total'             : total,
        'page_info'         : page_info
        }

    return jsonify_response(result)


@admin_json_dec(required=True)
def get_tutorial_list():
    ''' 美攻略列表 '''
    limit                   = 10
    page                    = int(request.args.get('page') or 1)
    start                   = (page-1)*limit

    has_more, infos         = TutorialService.get_paged_tutorial_entries(start=start, limit=limit)
    total                   = TutorialService.count_tutorials(None)
    page_info               = abbreviated_pages(int(math.ceil(total/(limit*1.0))), page)
    result                  = {
        'msg'               : '',
        'code'              : ResponseCode.SUCCESS,
        'infos'             : infos,
        'total'             : total,
        'page_info'         : page_info
        }

    return jsonify_response(result)


@admin_json_dec(required=True)
def get_tutorial():
    ''' '''
    item_id             = request.args.get('item_id')
    tutorial            = TutorialService.get_tutorial(item_id)
    assert tutorial, '攻略不存在'
    result              = {
        'code'          : ResponseCode.SUCCESS,
        'msg'           : '',
        'data'          : tutorial
        }
    return jsonify_response(result)


daily_coupon_edit_validator  = Inputs(
    {
     'start_time'    : TextField(min_length=1, max_length=100, msg='开始时间'),
     'end_time'      : TextField(min_length=1, max_length=100, msg='结束时间'),
     'use_condition' : TextField(min_length=0, max_length=100, msg='使用条件'),
     'total'         : IntField(msg='领取总数量'),
     'title'         : Optional(TextField(min_length=0, max_length=100, msg='每日优惠标题')),
     'coupon_id'     : IdField(msg='优惠券id')
    }
    )
@admin_json_dec(required=True, validator=daily_coupon_edit_validator, roles=[0,1])
def daily_coupon_edit(item_id=None):
    start_time      = request.valid_data.get('start_time')
    end_time        = request.valid_data.get('end_time')
    total           = request.valid_data.get('total')
    title           = request.valid_data.get('title')
    coupon_id       = request.valid_data.get('coupon_id')
    use_condition   = request.valid_data.get('use_condition')

    assert start_time<end_time, '开始时间不能晚于结束时间'
    if item_id:
        daily       = TutorialService.get_daily_coupon(item_id)
        assert daily, '领取不存在'
        assert total>=daily['sent'], '总数不能低于已领取数'
        count       = TutorialService.update_daily_coupon(item_id, **request.valid_data)
    else:
        use_time    = ''
        TutorialService.create_daily_coupon(title, coupon_id, start_time, end_time, total, use_time, use_condition)
    result          = {
        'code'      : ResponseCode.SUCCESS,
        'msg'       : ''
    }
    return jsonify_response(result)


@admin_json_dec(required=True)
def get_daily_coupon():
    ''' '''
    item_id     = request.args.get('item_id')
    daily       = TutorialService.get_daily_coupon(item_id)
    assert daily, '领取不存在'

    result      = {
        'data': daily,
        'code': ResponseCode.SUCCESS,
        'msg': ''           
        }
    return jsonify_response(result)


set_tutorial_status_validator  = Inputs(
    {
     'item_id'          : IdField(msg='攻略id'),
     'status'           : IntChoiceField(choices=[0,1], msg='攻略状态'),
    }
    )
@admin_json_dec(required=True, validator=set_tutorial_status_validator)
def set_tutorial_status():
    item_id         = request.valid_data.get('item_id')
    status          = request.valid_data.get('status')

    data            = {
        'status': status
        }
    TutorialService.set_tutorial_status(item_id, status)
    msg             = '上线成功' if status==1 else '下线成功'

    result          = {
        'code'          : ResponseCode.SUCCESS,
        'msg'           : msg
        }
    return jsonify_response(result)



reset_user_vcode_validator  = Inputs(
    {
     'phone': MobileField(msg='请输入手机号')
    }
    )
@admin_json_dec(validator=reset_user_vcode_validator, roles=[0,4])
def reset_user_vcode_sent():
    ''' 重置验证码次数 '''
    from ops.cache import InvalidUserPasswdCache
    from ops.cache import InvalidUserResetVcodeCache
    from ops.cache import InvalidUserSignupVcodeCache
    from ops.cache import SmsCache
    phone       = request.valid_data.get('phone')
    InvalidUserPasswdCache.clear_today_counter(phone)
    InvalidUserResetVcodeCache.clear_today_counter(phone)
    InvalidUserSignupVcodeCache.clear_today_counter(phone)
    SmsCache.clear_sent_count(phone)
    result  = {
        'code'      : ResponseCode.SUCCESS,
        'msg'       : '重置成功'
        }
    return jsonify_response(result)


get_user_vcode_validator  = Inputs(
    {
     'phone': MobileField(msg='请输入手机号'),
     'cat'  : IntChoiceField(choices=[1,2], msg='请选择类型')
    }
    )
@admin_json_dec(validator=get_user_vcode_validator, roles=[0,4])
def get_user_vcode():
    ''' 获取用户验证码 '''
    from ops.cache import SmsCache
    phone   = request.valid_data.get('phone')
    cat     = request.valid_data.get('cat')
    user    = UserService.get_user_by_phone(phone)
    if cat==1:
        assert not user, '用户已存在'
    else:
        assert user, '用户不存在'
    vcode   = SmsCache.get_vcode(phone)
    sent    = SmsCache.get_sent_count(phone)
    assert vcode, '验证码不存在, 请获取验证码'
    result  = {
        'code'      : ResponseCode.SUCCESS,
        'msg'       : '',
        'vcode'     : vcode,
        'count'     : sent
        }
    return jsonify_response(result)


tutorial_edit_validator  = Inputs(
    {
     'title'         : TextField(min_length=1, max_length=100, msg='攻略标题'),
     'image'         : TextField(min_length=1, max_length=100, msg='攻略首页推荐图'),
     'icon'          : TextField(min_length=1, max_length=100, msg='攻略列表icon'),
     'photo'         : TextField(min_length=1, max_length=100, msg='攻略详情大图'),
     'items'         : REGField(pattern='^(\d+,?)+$', msg='请输入项目id，逗号隔开')
    }
    )
@admin_json_dec(required=True, validator=tutorial_edit_validator, roles=[0,1])
def tutorial_edit(item_id=None):
    title           = request.valid_data.get('title')
    image           = request.valid_data.get('image')
    photo           = request.valid_data.get('photo')
    items           = request.valid_data.get('items')
    icon            = request.valid_data.get('icon')
    for the_item_id in items.split(','):
        item        = ItemService.get_item_dict_by_id(the_item_id)
        assert item, 'ID为{}的项目不存在'.format(the_item_id)
    if item_id:
        TutorialService.update_tutorial_entry(item_id, **request.valid_data)
    else:
        item_id     = TutorialService.create_tutorial_entry(title, icon, image, photo, items)
    return jsonify_response({'item_id': item_id})



send_user_coupon_validator  = Inputs(
    {
     'phone'         : MobileField(min_length=1, max_length=100, msg='请输入用户手机号码'),
     'coupon_id'     : IdField(msg='请选择优惠券')
    }
    )
@admin_json_dec(required=True, validator=send_user_coupon_validator, roles=[0,1,4])
def send_user_coupon():
    phone           = request.valid_data.get('phone')
    coupon_id       = request.valid_data.get('coupon_id')

    user            = UserService.get_user_by_phone(phone)
    assert user, '用户不存在'
    coupon          = CouponService.get_coupon(coupon_id)
    assert coupon, '优惠券不存在'
    CouponService.send_user_coupon(user.id, coupon_id)

    result          = {
        'code'      : ResponseCode.SUCCESS,
        'msg'       : '发放成功'
    }
    return jsonify_response(result)


@admin_json_dec(required=True, validator=None, roles=[0,1,4])
def set_cats_order():
    data    = json.loads(request.data)
    for index, i in enumerate(data):
        ItemService.set_item_cat_order(i, index)

    result  = {
        'code'  : ResponseCode.SUCCESS,
        'msg'   : '排序成功'
    }
    return jsonify_response(result)


