# -*- coding: utf-8 -*-
import math
from collections import defaultdict
from sqlalchemy import and_
from sqlalchemy import or_

from flask import request
from flask import redirect
from flask import Blueprint
from flask import render_template
from flask import make_response

from util.utils      import jsonify_response
from util.utils      import template_response
from util.utils      import abbreviated_pages
from util.sign       import gen_hospital_token
from util.sign       import del_cookie
from util.sign       import set_cookie
from util.decorators import hospital_dec
from util.validators import Optional
from util.validators import Inputs
from util.validators import MobileField
from util.validators import TextField
from util.validators import IdField
from util.validators import IntChoiceField
from util.validators import MobileField
from models          import db
from models          import Order
from models          import User
from models          import ItemCat
from models          import Item
from models          import ItemSubCat
from models          import ServiceCode
from ops.hospital    import HospitalService
from ops.cache       import HospitalInvalidUserPasswdCache
from ops.data        import DataService
from ops.item        import ItemService
from ops.comment     import CommentService
from ops.user        import UserService
from ops.order       import OrderService
from ops.room_design import RoomDesignService
from ops.promote     import PromoteService
from ops.bulks       import fetch_credit_refs
from ops.bulks       import fetch_user_refs
from ops.bulks       import fetch_item_refs
from ops.bulks       import fetch_servicecode_refrence
from ops.bulks       import fetch_apply_refs
from constants       import ResponseCode
from constants       import ORDER_STATUS
from constants       import SERVICE_STATUS
from settings        import CONTACT




def set_order_status(order, comment=None, servicecode=None):
    ''' 根据服务码状态 是否已评论重新订单状态'''
    if not order['credit_verified']:
        order['status'] = ORDER_STATUS.VERIFYING
    elif order['status']==ORDER_STATUS.PAY_SUCCESS:
        if servicecode['status'] == 1:
            order['status']     = ORDER_STATUS.BOOKED
        elif servicecode['status'] == 2:
            order['status']     = ORDER_STATUS.CONFIRMED
    elif order['status'] == ORDER_STATUS.FINISH and not comment:
        order['status'] = ORDER_STATUS.TO_COMMENT



index_validator = Inputs(
    {
     'offset'         : Optional(TextField(min_length=0, max_length=100, msg='分页')),
     'cat'            : Optional(IntChoiceField(choices=[1,2,3,4], msg='订单类型')),
     'phone'          : Optional(MobileField(msg='客户手机号')),
    }
    )
@hospital_dec(required=True, validator=index_validator)
def index():
    ''' 订单列表 '''
    offset      = request.valid_data.get('offset')
    cat         = request.valid_data.get('cat') or 1
    phone       = request.valid_data.get('phone')
    if not phone: assert cat, '订单类型'
    if not cat: assert phone, '客户手机号'

    user                = HospitalService.get_user_by_name(request.name)
    hospital_id         = user.hospital_id

    conditions          = []
    query_one           = and_(
        Order.hospital_id==hospital_id,
        Order.credit_verified==1,
        Order.status.in_([ORDER_STATUS.PAY_SUCCESS, ORDER_STATUS.FINISH, ORDER_STATUS.CANCELED])
        )
    sub_query       = db.session.query(ServiceCode.order_id).filter(ServiceCode.status==SERVICE_STATUS.STANDBY).subquery()
    query_two           = and_(
            Order.hospital_id==hospital_id,
            Order.credit_verified==1,
            Order.status==ORDER_STATUS.PAY_SUCCESS,
            Order.id.in_(sub_query)
            )
    sub_query       = db.session.query(ServiceCode.order_id).filter(ServiceCode.status==SERVICE_STATUS.BOOKED).subquery()
    conditions      = [
        Order.hospital_id==hospital_id,
        Order.status==ORDER_STATUS.PAY_SUCCESS,
        Order.credit_verified==1,
        Order.id.in_(sub_query)
        ]
    query_three     = and_(*conditions)
    sub_query       = db.session.query(ServiceCode.order_id).filter(ServiceCode.status==SERVICE_STATUS.VERIFYED).subquery()
    conditions[:]   = [
        Order.hospital_id==hospital_id,
        Order.status==ORDER_STATUS.PAY_SUCCESS,
        Order.credit_verified==1,
        Order.id.in_(sub_query)
        ]
    query_four      = and_(*conditions)

    counters            = {}

    condition_query     = {
        1: query_one,
        2: query_two,
        3: query_three,
        4: query_four
        }
    for i in [1,2,3,4]:
        counters[i]     = OrderService.count_order(condition_query[i])
    where               = condition_query[cat]
    if phone:
        subquery        = db.session.query(User.id).filter(User.phone==phone).subquery()
        where           = and_(
            Order.hospital_id==hospital_id,
            Order.user_id.in_(subquery),
            Order.credit_verified==1,
            Order.status.in_([
                ORDER_STATUS.FINISH, ORDER_STATUS.PAY_SUCCESS
                , ORDER_STATUS.CANCELED
                ]
                )
            )
    has_more, orders    = OrderService.get_paged_orders(where=where, offset=offset)

    order_ids           = [i['id'] for i in orders]

    order_id_service_code_map   = OrderService.get_service_codes_by_order_ids(order_ids)
    for order in orders:
        if order['status']==ORDER_STATUS.PAY_SUCCESS:
            order['label'] = '待预约'
        elif order['status']==ORDER_STATUS.BOOKED and not order_id_service_code_map.get(order['id']):
            order['label'] = '待验证'
        elif order['status']==ORDER_STATUS.BOOKED and order_id_service_code_map.get(order['id']):
            order['label'] = '待完成'
        else:
            order['label'] = '全部'

    offset              = str(orders[-1]['id']) if orders else ''

    data                = defaultdict(list)
    data[cat]           = orders

    fields  = ['name','id_no', 'user_id']
    fetch_credit_refs(orders, dest_key='credit', fields=fields, keep_id=True)
    fetch_user_refs(orders, keep_id=True)
    fields  = ['id', 'title', 'price', 'orig_price', 'image', 'hospital_id']
    fetch_item_refs(orders, fields=fields, keep_id=True)
    fetch_servicecode_refrence(orders, 'id', dest_key='service_code_dict', keep_id=True)

    fetch_apply_refs(orders, dest_key='trial_apply', keep_id=True)

    order_item_map      = {order['id']:order['item_id'] for order in orders}
    comments            = CommentService.get_comments_by_item_ids(order_item_map.values())
    item_comment_map    = {i['item_id']:i['id'] for i in comments}
    for order in orders:
        set_order_status(order, comment=item_comment_map.get(order['item_id']), servicecode=order['service_code_dict'])
    
    top_nav             = {
        cat: 'mui-active'
        }
    result              = {
        'code'              : ResponseCode.SUCCESS,
        'offset'            : offset,
        'counters'          : counters,
        'phone'             : phone,
        'data'              : data,
        'msg'               : '',
        'has_more'          : has_more,
        'infos'             : orders,
        'top_nav'           : top_nav,
        }

    template_name       = 'hospital/index.html'
    if phone:
        template_name   = 'hospital/index.html'
    if request.args.get('json'):
        return jsonify_response(result)
    return render_template(template_name, **result)


paged_orders_validator = Inputs(
    {
     'offset'         : Optional(TextField(min_length=0, max_length=100, msg='分页')),
     'cat'            : Optional(IntChoiceField(choices=[1,2,3,4], msg='订单类型')),
     'phone'          : Optional(MobileField(msg='客户手机号')),
    }
    )
@hospital_dec(required=True, validator=paged_orders_validator)
def get_paged_orders():
    ''' 分页订单列表 '''
    offset      = request.valid_data.get('offset')
    cat         = request.valid_data.get('cat') or 1
    phone       = request.valid_data.get('phone')
    if not phone: assert cat, '订单类型'
    if not cat: assert phone, '客户手机号'

    user                = HospitalService.get_user_by_name(request.name)
    hospital_id         = user.hospital_id

    conditions          = []
    query_one           = and_(
        Order.hospital_id==hospital_id,
        Order.credit_verified==1,
        Order.status.in_([ORDER_STATUS.PAY_SUCCESS, ORDER_STATUS.FINISH, ORDER_STATUS.CANCELED])
        )
    sub_query       = db.session.query(ServiceCode.order_id).filter(ServiceCode.status==SERVICE_STATUS.STANDBY).subquery()
    query_two           = and_(
            Order.hospital_id==hospital_id,
            Order.credit_verified==1,
            Order.status==ORDER_STATUS.PAY_SUCCESS,
            Order.id.in_(sub_query)
            )
    sub_query       = db.session.query(ServiceCode.order_id).filter(ServiceCode.status==SERVICE_STATUS.BOOKED).subquery()
    conditions      = [
        Order.hospital_id==hospital_id,
        Order.status==ORDER_STATUS.PAY_SUCCESS,
        Order.credit_verified==1,
        Order.id.in_(sub_query)
        ]
    query_three     = and_(*conditions)
    sub_query       = db.session.query(ServiceCode.order_id).filter(ServiceCode.status==SERVICE_STATUS.VERIFYED).subquery()
    conditions[:]   = [
        Order.hospital_id==hospital_id,
        Order.status==ORDER_STATUS.PAY_SUCCESS,
        Order.credit_verified==1,
        Order.id.in_(sub_query)
        ]
    query_four      = and_(*conditions)

    counters            = {}

    condition_query     = {
        1: query_one,
        2: query_two,
        3: query_three,
        4: query_four
        }
    for i in [1,2,3,4]:
        counters[i]     = OrderService.count_order(condition_query[i])
    where               = condition_query[cat]
    if phone:
        subquery        = db.session.query(User.id).filter(User.phone==phone).subquery()
        where           = and_(
            Order.hospital_id==hospital_id,
            Order.user_id.in_(subquery),
            Order.credit_verified==1,
            Order.status.in_([
                ORDER_STATUS.FINISH, ORDER_STATUS.PAY_SUCCESS
                , ORDER_STATUS.CANCELED
                ]
                )
            )
    has_more, orders    = OrderService.get_paged_orders(where=where, offset=offset)

    order_ids           = [i['id'] for i in orders]

    order_id_service_code_map   = OrderService.get_service_codes_by_order_ids(order_ids)
    for order in orders:
        if order['status']==ORDER_STATUS.PAY_SUCCESS:
            order['label'] = '待预约'
        elif order['status']==ORDER_STATUS.BOOKED and not order_id_service_code_map.get(order['id']):
            order['label'] = '待验证'
        elif order['status']==ORDER_STATUS.BOOKED and order_id_service_code_map.get(order['id']):
            order['label'] = '待完成'
        else:
            order['label'] = '全部'

    offset              = str(orders[-1]['id']) if orders else ''

    data                = defaultdict(list)
    data[cat]           = orders

    fields  = ['name','id_no', 'user_id']
    fetch_credit_refs(orders, dest_key='credit', fields=fields, keep_id=True)
    fetch_user_refs(orders)
    fields  = ['id', 'title', 'price', 'orig_price', 'image', 'hospital_id']
    fetch_item_refs(orders, fields=fields, keep_id=True)
    fetch_servicecode_refrence(orders, 'id', dest_key='service_code_dict', keep_id=True)

    order_item_map      = {order['id']:order['item_id'] for order in orders}
    comments            = CommentService.get_comments_by_item_ids(order_item_map.values())
    item_comment_map    = {i['item_id']:i['id'] for i in comments}
    for order in orders:
        set_order_status(order, comment=item_comment_map.get(order['item_id']), servicecode=order['service_code_dict'])
   
    template = ''
    for order in orders:
        template += render_template('hospital/entry.html', info=order)

    result   = {
        'code': ResponseCode.SUCCESS,
        'msg' : '',
        'has_more': has_more,
        'infos': template,
        'offset': offset
        }
    return jsonify_response(result)


def login():
    ''' 医院端登录 '''
    return render_template('hospital/hospital_login.html')


login_post_validator  = Inputs(
    {
     'name'         : TextField(min_length=1, max_length=100, msg='请输入账号'),
     'passwd'       : TextField(min_length=1, max_length=100, msg='请输入密码')
    }
    )
@hospital_dec(required=False, validator=login_post_validator)
def login_post():
    name   = request.valid_data.get('name')
    passwd = request.valid_data.get('passwd')
    count  = HospitalInvalidUserPasswdCache.incr(name)
    assert count<10, '今日密码错误次数超限，如需帮助，请联系美分分客服{}'.format(CONTACT)
    if HospitalService.check_user(name, passwd):
        response    = jsonify_response({'code':ResponseCode.SUCCESS}, with_response=True)
        token       = gen_hospital_token(name)
        set_cookie(response, 'hospital_name', name, 86400*30)
        set_cookie(response, 'sign', token, 86400*30)
        HospitalInvalidUserPasswdCache.incr(name, -1)
        return response
    assert 0, '用户名或密码错误'


def logout():
    try:
        response = redirect('/hospital/')
        del_cookie(response, 'sign')
        return response
    except:
        import traceback
        traceback.print_exc()
        return 'server error'



book_surgery_validator = Inputs(
    {
     'order_id'         : IdField(msg='订单id'),
     'book_time'        : TextField(min_length=1, max_length=100, msg='预约时间')
    }
    )
@hospital_dec(required=True, validator=book_surgery_validator)
def book_surgery():
    ''' 接受用户预约 '''
    order_id            = request.valid_data.get('order_id')
    book_time           = request.valid_data.get('book_time')

    count               = OrderService.book_surgery(order_id, book_time)

    msg                 = '预约成功' if count else '预约失败'
    result              = {
        'msg'           : msg,
        'code'          : ResponseCode.SUCCESS
        }
    return jsonify_response(result)


confirm_surgery_validator = Inputs(
    {
     'order_id'         : IdField(msg='订单id'),
     'service_code'     : TextField(min_length=1, max_length=100, msg='服务码'),
    }
    )
@hospital_dec(required=True, validator=confirm_surgery_validator)
def confirm_surgery():
    ''' 验证服务码 确认手术 '''
    service_code        = request.valid_data.get('service_code')
    order_id            = request.valid_data.get('order_id')
    count               = OrderService.verify_servicecode(order_id, service_code)
    assert count, '确认手术失败'
    msg                 = '确认手术成功' if count else '确认手术失败'
    result              = {
        'msg'           : msg,
        'code'          : ResponseCode.SUCCESS
        }
    return jsonify_response(result)


cancel_book_validator = Inputs(
    {
     'order_id'         : IdField(msg='订单id'),
    }
    )
@hospital_dec(required=True, validator=cancel_book_validator)
def cancel_book():
    ''' 取消预约 '''
    order_id            = request.valid_data.get('order_id')
    count               = OrderService.cancel_book(order_id)
    msg                 = '取消预约成功' if count else '没有找到预约记录或已取消预约'

    result              = {
        'msg'           : msg,
        'code'          : ResponseCode.SUCCESS
        }
    return jsonify_response(result)



cancel_surgery_validator = Inputs(
    {
     'order_id'         : IdField(msg='订单id'),
    }
    )
@hospital_dec(required=True, validator=cancel_surgery_validator)
def cancel_surgery():
    ''' 取消手术 '''
    order_id            = request.valid_data.get('order_id')
    count               = OrderService.cancel_surgery(order_id)
    msg                 = '取消手术成功' if count else '订单不存在或已取消'

    result              = {
        'msg'           : msg,
        'code'          : ResponseCode.SUCCESS
        }
    return jsonify_response(result)


finish_order_validator = Inputs(
    {
     'order_id'         : IdField(msg='订单id'),
    }
    )
@hospital_dec(required=True, validator=finish_order_validator)
def finish_order():
    order_id            = request.valid_data.get('order_id')
    order               = OrderService.get_order_by_id(order_id)
    where               = Order.status==ORDER_STATUS.PAY_SUCCESS
    count               = OrderService.update_order_status(order_id, ORDER_STATUS.FINISH, where=where)
    if count and order.credit_choice_id:
        RoomDesignService.add_user_vote_privilege(order.user_id, 2)
        #PromoteService.add_rd_draw_count(order.user_id, 3)
    result              = {
        'code'          : ResponseCode.SUCCESS,
        'msg'           : '手术已完成'
        }
    return jsonify_response(result)


@hospital_dec(required=True)
def get_hospital_cats():
    ''' 获取医院分类 '''
    user                = HospitalService.get_user_by_name(request.name)
    hospital_id         = user.hospital_id

    sub_cat_ids_count   = HospitalService.get_hospital_sub_cat_ids_and_count(hospital_id)

    sub_cat_ids         = sub_cat_ids_count.keys()

    sub_cat_count_map   = {i:len(v) for i,v in sub_cat_ids_count.items()}

    sub_cat_list        = ItemService.get_subcats_by_ids(sub_cat_ids)

    cat_ids             = []
    for i in sub_cat_list:
        cat_ids.extend((i['cat_id_list']))

    for i in sub_cat_list:
        i['count']      = sub_cat_count_map.get(i['id'], 0)

    print sub_cat_ids, 'sub_cat_ids', sub_cat_count_map
    cat_list            = ItemService.get_cats_by_ids(cat_ids)

    for cat in cat_list:
        sub_cats        = [i for i in sub_cat_list if cat['id'] in i['cat_id_list']]
        cat['sub_cats'] = sub_cats
        cat['count']    = sum(i['count'] for i in sub_cats)

    total               = sum(i['count'] for i in cat_list)
    result              = {
        'code'              : ResponseCode.SUCCESS,
        'msg'               : '',
        'cat_list'          : cat_list,
        'total'             : total
        }
    return jsonify_response(result)



order_list_validator = Inputs(
    {
     'offset'         : Optional(TextField(min_length=0, max_length=100, msg='分页')),
     'cat'            : Optional(IntChoiceField(choices=[1,2,3,4], msg='订单类型')),
     'phone'          : Optional(MobileField(msg='客户手机号')),
    }
    )
@hospital_dec(required=True, validator=order_list_validator)
def get_orders():
    ''' 订单列表 '''
    offset      = request.valid_data.get('offset')
    cat         = request.valid_data.get('cat')
    phone       = request.valid_data.get('phone')
    if not phone: assert cat, '订单类型'
    if not cat: assert phone, '客户手机号'

    user                = HospitalService.get_user_by_name(request.name)
    hospital_id         = user.hospital_id

    conditions  = []
    if   cat==2: #待预约
        conditions.append(
            Order.status==ORDER_STATUS.PAY_SUCCESS,
            )
    elif cat==3: #待验证
        sub_query       = db.session.query(ServiceCode.order_id).filter(ServiceCode.status==SERVICE_STATUS.STANDBY).subquery()
        conditions[:]   = [
            Order.status==ORDER_STATUS.BOOKED,
            Order.id.in_(sub_query)
            ]
    elif cat==4: #待完成
        sub_query       = db.session.query(ServiceCode.order_id).filter(ServiceCode.status==SERVICE_STATUS.VERIFYED).subquery()
        conditions[:]   = [
            Order.status==ORDER_STATUS.BOOKED,
            Order.id.in_(sub_query)
            ]
    if phone: #按客户手机号搜索订单
        sub_query       = db.session.query(User.id).filter(User.phone==phone).subquery()
        conditions[:]   = [ Order.user_id.in_(sub_query) ]

    conditions.append(Order.hospital_id==hospital_id)
    where               = and_(*conditions)
    has_more, orders    = OrderService.get_paged_orders(where=where, offset=offset)
    offset              = str(orders[-1]['id']) if orders else ''

    fetch_credit_refs(orders, dest_key='credit', keep_id=True)
    fetch_user_refs(orders)

    result              = {
        'code'              : ResponseCode.SUCCESS,
        'offset'            : offset,
        'msg'               : '',
        'has_more'          : has_more,
        'infos'             : orders,
        }
    return jsonify_response(result)


def change_passwd():
    return render_template('hospital/change_passwd.html')


change_passwd_validator = Inputs(
    {
     'passwd'         : TextField(min_length=0, max_length=100, msg='原密码'),
     'new_passwd'     : TextField(min_length=0, max_length=100, msg='新密码')
    }
    )
@hospital_dec(validator=change_passwd_validator)
def change_passwd_post():
    ''' 修改密码 '''
    passwd      = request.valid_data.get('passwd')
    new_passwd  = request.valid_data.get('new_passwd')
    user        = HospitalService.get_user_by_name(request.name)
    assert user and user.passwd==passwd, '原密码不正确'
    count       = HospitalService.change_passwd(request.name, new_passwd)

    msg         = '修改成功'

    result      = {
        'code'     : ResponseCode.SUCCESS,
        'msg'      : msg
        }
    return jsonify_response(result)






search_order_validator = Inputs(
    {
     'offset'         : Optional(TextField(min_length=0, max_length=100, msg='分页')),
     'phone'          : Optional(MobileField(msg='客户手机号')),
    }
    )
@hospital_dec(required=True, validator=search_order_validator)
def search_order_list():
    ''' 订单列表 '''
    offset      = request.valid_data.get('offset')
    phone       = request.valid_data.get('phone')
    if not phone: assert phone, '客户手机号'

    user                = HospitalService.get_user_by_name(request.name)
    hospital_id         = user.hospital_id

    conditions          = []
    if phone: #按客户手机号搜索订单
        sub_query       = db.session.query(User.id).filter(User.phone==phone).subquery()
        conditions.append(Order.user_id.in_(sub_query))
    conditions.append(Order.hospital_id==hospital_id)
    conditions.append(Order.credit_verified==1)
    where               = and_(*conditions)
    has_more, orders    = OrderService.get_paged_orders(where=where, offset=offset)

    order_ids           = [i['id'] for i in orders]

    order_id_service_code_map   = OrderService.get_service_codes_by_order_ids(order_ids)
    for order in orders:
        if order['status']==ORDER_STATUS.PAY_SUCCESS:
            order['label'] = '待预约'
        elif order['status']==ORDER_STATUS.BOOKED and not order_id_service_code_map.get(order['id']):
            order['label'] = '待验证'
        elif order['status']==ORDER_STATUS.BOOKED and order_id_service_code_map.get(order['id']):
            order['label'] = '待完成'
        else:
            order['label'] = '全部'

    offset              = str(orders[-1]['id']) if orders else ''

    data                = defaultdict(list)
    fetch_credit_refs(orders, dest_key='credit', keep_id=True)
    fetch_user_refs(orders)
    fetch_item_refs(orders)

    result              = {
        'code'              : ResponseCode.SUCCESS,
        'offset'            : offset,
        'phone'             : phone,
        'data'              : data,
        'msg'               : '',
        'has_more'          : has_more,
        'infos'             : orders,
        }

    template_name   = 'hospital/order_search.html'
    #return jsonify_response(result)
    return render_template(template_name, **result)

@hospital_dec()
def home():
    user  = HospitalService.get_user_by_name(request.name)
    hospital = ItemService.get_hospital_dict_by_id(user.hospital_id)
    return render_template('hospital/home.html',
        user=user,
        hospital=hospital
        )

@hospital_dec()
def cat():
    ''' 获取医院分类 '''
    user                = HospitalService.get_user_by_name(request.name)
    hospital_id         = user.hospital_id
    sub_cat_ids_count   = HospitalService.get_hospital_sub_cat_ids_and_count(hospital_id)

    sub_cat_ids         = sub_cat_ids_count.keys()

    sub_cat_count_map   = {i:len(v) for i,v in sub_cat_ids_count.items()}

    sub_cat_list        = ItemService.get_subcats_by_ids(sub_cat_ids)
    cat_ids             = []
    for i in sub_cat_list:
        cat_ids.extend((i['cat_id_list']))

    for i in sub_cat_list:
        i['count']      = sub_cat_count_map.get(i['id'], 0)

    print sub_cat_ids, 'sub_cat_ids', sub_cat_count_map
    cat_list            = ItemService.get_cats_by_ids(cat_ids)

    for cat in cat_list:
        sub_cats        = [i for i in sub_cat_list if cat['id'] in i['cat_id_list']]
        cat['sub_cats'] = sub_cats
        cat_sub_cat_item_ids = set()
        for i in sub_cats:
            cat_sub_cat_item_ids = cat_sub_cat_item_ids.union(sub_cat_ids_count[i['id']])
        cat['count']    = len(cat_sub_cat_item_ids)

    total               = sum(i['count'] for i in cat_list)
    result              = {
        'code'              : ResponseCode.SUCCESS,
        'msg'               : '',
        'cat_list'          : cat_list,
        'total'             : total
        }
    return render_template('hospital/cat.html',
        **result
        )


def reset_passwd():
    ''' 重置密码 '''
    return render_template('hospital/reset_passwd.html')


reset_passwd_post_validator = Inputs(
    {
     'passwd'         : TextField(min_length=0, max_length=100, msg='密码'),
     'new_passwd'     : TextField(min_length=0, max_length=100, msg='新密码'),
    }
    )
@hospital_dec(validator=reset_passwd_post_validator)
def reset_passwd_post():
    ''' 重置密码 '''
    passwd          = request.valid_data.get('passwd')
    new_passwd      = request.valid_data.get('new_passwd')

    print passwd
    print new_passwd
    user            = HospitalService.get_user_by_name(request.name)

    assert user and user.passwd == passwd, '原密码错误'
    HospitalService.change_passwd(request.name, new_passwd)

    result          = {
        'code'          : ResponseCode.SUCCESS,
        'msg'           : '修改成功'
    }
    return jsonify_response(result)



@hospital_dec()
def cat_items():
    ''' 分类商品列表 '''
    cat_id      = request.args.get('cat_id')
    sub_cat_id  = request.args.get('sub_cat_id')
    keyword     = request.args.get('keyword') or ''

    user        = HospitalService.get_user_by_name(request.name)
    conditions  = []
    where       = None
    cat         = None
    subcat      = None
    if cat_id:
        cat     = ItemService.get_cat_dict_by_id(cat_id)
    if sub_cat_id:
        subcat  = ItemService.get_subcat_dict_by_id(sub_cat_id)
        cat     = ItemService.get_cat_dict_by_id(subcat['cat_id'])
    if cat_id:
        query     = or_(
            ItemSubCat.cat_ids==cat_id,
            ItemSubCat.cat_ids.like('%,{}'.format(cat_id)),
            ItemSubCat.cat_ids.like('%,{},%'.format(cat_id)),
            ItemSubCat.cat_ids.like('{},%'.format(cat_id))
            )
        result    = db.session.query(ItemSubCat).filter(query).all()
        print result
        sub_cat_ids = [i.id for i in result]
        where       = or_()
        for the_sub_cat_id in sub_cat_ids:
            the_query     = or_(
            Item.sub_cat_ids==the_sub_cat_id,
            Item.sub_cat_ids.like('%,{}'.format(the_sub_cat_id)),
            Item.sub_cat_ids.like('%,{},%'.format(the_sub_cat_id)),
            Item.sub_cat_ids.like('{},%'.format(the_sub_cat_id))
            )
            where.append(the_query)
    elif sub_cat_id:
        query     = or_(
            Item.sub_cat_ids==sub_cat_id,
            Item.sub_cat_ids.like('%,{}'.format(sub_cat_id)),
            Item.sub_cat_ids.like('%,{},%'.format(sub_cat_id)),
            Item.sub_cat_ids.like('{},%'.format(sub_cat_id))
            )
        where       = query
    if keyword:
        where       = or_(
            Item.id==keyword,
            and_(
                Item.title.like('%{}%'.format(keyword)),
                Item.hospital_id==user.hospital_id
                )
            )
    if where is not None:
        where           = and_(
            where,
            Item.hospital_id==user.hospital_id
            )
    else:
        where       = Item.hospital_id==user.hospital_id
    has_more, items = ItemService.get_paged_items(where=where)

    item_ids        = [i['id'] for i in items]
    activity_items  = ItemService.get_activity_items_by_item_ids(item_ids)
    item_price_map  = {i.item_id:i.price for i in activity_items}
    for item in items:#活动价
        if item_price_map.get(item['id']):
            item['price'] = item_price_map.get(item['id'])
    result          = {
        'code'          : ResponseCode.SUCCESS,
        'keyword'       : keyword,
        'infos'         : items,
        'has_more'      : has_more,
        'cat'           : cat,
        'subcat'        : subcat,
        'msg'           : ''
    }
    #return jsonify_response(result)
    return render_template('hospital/cat_items.html', **result)



