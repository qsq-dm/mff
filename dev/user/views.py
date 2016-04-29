# -*- coding: utf-8 -*-
import os
import time
import json
from itertools import chain

from flask import request
from flask import redirect
from flask import render_template
from flask import send_from_directory

from sqlalchemy      import case
from sqlalchemy      import and_
from sqlalchemy      import or_
from models          import db
from models          import ItemComment
from models          import Item
from models          import School
from models          import UserCoupon
from models          import Order
from models          import PeriodPayLog
from models          import ItemFav
from models          import Repayment
from models          import UserCoupon
from models          import HelpCat
from models          import ActivityItem
from models          import CreditApply
from models          import ItemSubCat
from models          import Hospital
from models          import DailyCoupon
from models          import BeautyEntry

from util.utils      import format_price
from util.utils      import deadline_zh
from util.utils      import jsonify_response
from util.utils      import template_response
from util.utils      import trans_list
from util.utils      import calc_expire_remain
from util.utils      import dt_obj
from util.utils      import day_delta
from util.utils      import get_current_period
from util.utils      import get_next_period
from util.utils      import get_due_time
from util.utils      import is_delayed
from util.utils      import date_to_datetime
from util.utils      import get_timestamp
from util.utils      import add_months
from util.utils      import js_response
from util.utils      import get_date_delta
from util.utils      import cacl_punish_fee
from util.utils      import get_time_str_from_dt
from util.utils      import prefix_img_domain
from util.utils      import get_delayed_info
from util.utils      import get_next_working_day
from util.utils      import get_img_key
from util.utils      import set_coupon_use_time
from util.utils      import format_dt
from util.utils      import format_rate
from util.utils      import str_to_int_list
from util.sign       import get_cookie
from util.sign       import set_cookie
from util.decorators import wechat_loggin_dec

from util.validators import Optional
from util.validators import REGField
from util.validators import Inputs
from util.validators import MobileField
from util.validators import TextField
from util.validators import IntChoiceField
from util.validators import IdField
from util.validators import JsonField
from util.validators import ChoiceField
from ops.common      import pay_success_action
from ops.common      import get_item_activity_price
from ops.bulks       import fetch_user_refs
from ops.bulks       import fetch_item_refs
from ops.bulks       import fetch_item_subcat_refs
from ops.bulks       import fetch_min_period_info
from ops.bulks       import fetch_hospital_refs
from ops.bulks       import fetch_order_refs
from ops.bulks       import fetch_coupon_refs
from ops.item        import ItemService
from ops.comment     import CommentService
from ops.promote     import PromoteService
from ops.user        import UserService
from ops.order       import OrderService
from ops.activity    import ActivityService
from ops.log         import LogService
from ops.data        import DataService
from ops.redpack     import RedpackService
from ops.credit      import CreditService
from ops.coupon      import CouponService
from ops.beauty_tutorial import TutorialService
from ops.bulks       import fetch_servicecode_refrence
from constants       import ResponseCode
from constants       import ORDER_STATUS
from constants       import ORDER_STATUS_LABEL
from constants       import PAY_METHOD
from constants       import REPAYMENT_STATUS
from constants       import APPLY_STATUS
from constants       import CREDIT_STATUS
from settings        import CONTACT
from settings        import DEFAULT_CREDIT
from settings        import WX_PAY_NOTIFY_URL
from settings        import WX_REPAYMENT_NOTIFY_URL
from thirdparty.wx_pay      import Notify_pub
from thirdparty.wx_pay      import WxPayConf_pub
from thirdparty.wx_pay      import UnifiedOrder_pub
from thirdparty.wx_pay      import JsApi_pub
from thirdparty.wx_pay      import get_wx_pay_params
from thirdparty.wechat      import wechat
from thirdparty.wechat      import get_jssdk_context
from thirdparty.qn          import gen_qn_token
from thirdparty.qn          import upload_img
from thirdparty.sms         import send_sms_new_order
from settings import SERVER_NAME
from settings import ITEM_ORDER_CHOICES
from settings import HOSPITAL_ORDER_CHOICES
from settings import CAT_ICONS
from settings import CAT_ICONS_ACTIVE

from ops.order import set_order_status


def set_coupon_cat_str(info, item_cats=None, item_subcats=None):
    ''' 优惠券品类信息 '''
    if info['coupon_cat']==0:
        info['cat_str'] = '全部适用'
    elif info['coupon_cat']==1:
        cat             = filter(lambda i:i['id']==info['cat_id'], item_cats)[0]
        info['cat_str'] = '仅限{}类项目'.format(cat['name'])
    elif info['coupon_cat']==2:
        print info['sub_cat_id'], [i['id'] for i in item_subcats]
        subcat          = filter(lambda i:i['id']==info['sub_cat_id'], item_subcats)[0]
        info['cat_str'] = '仅限{}项目'.format(subcat['name'])
    else:
        info['cat_str'] = '指定项目'



@wechat_loggin_dec(required=False, validator=None, app=True)
def user_index():
    ''' 用户首页 '''
    _,  recommend_sub_cats  = ItemService.get_paged_recommend_subcats(_sort='sort_order', _sort_dir='ASC')
    fetch_item_subcat_refs(recommend_sub_cats)

    current_activity        = ActivityService.get_current_activity() or {}
    where                   = ActivityItem.activity_id==current_activity.get('id')
    fields                  = ('id', 'item_id', 'price')
    _,  activity_items      = ItemService.get_paged_activity_items(fields=fields, where=where, _sort='sort_order', _sort_dir='ASC')
    fields                  = ('id', 'item_id', 'image', 'desc')
    where                   = None
    _,  recommend_items     = ItemService.get_paged_recommend_items(fields=fields, where=where, _sort='sort_order', _sort_dir='ASC')

    fields                  = ['id', 'title', 'price', 'orig_price', 'has_fee', 'support_choice_list']
    fetch_item_refs(chain(activity_items, recommend_items), fields=fields)

    item_dict_list          = [i['item'] for i in chain(activity_items, recommend_items)]
    item_list               = []
    for i in item_dict_list:
        if i not in item_list:
            item_list.append(i)
    fetch_min_period_info(item_list)
        
    banner                  = [
        {'image':'http://7xnpdb.com1.z0.glb.clouddn.com/o_1a32t99l213e55j47fp1v96u80111348368_1467882916861451_480196332_n.jpg', 'link':'/user/login'},
        {'image':'http://7xnpdb.com1.z0.glb.clouddn.com/o_1a32t99l213e55j47fp1v96u80111348368_1467882916861451_480196332_n.jpg', 'link':'/user/login'},
        {'image':'http://7xnpdb.com1.z0.glb.clouddn.com/o_1a32t99l213e55j47fp1v96u80111348368_1467882916861451_480196332_n.jpg', 'link':'/user/login'}
        ]
    context                 = {
        'code'                 : ResponseCode.SUCCESS,
        'msg'                  : '',
        'activity_items'       : activity_items,
        'recommend_items'      : recommend_items,
        'activity'             : current_activity,
        'banner'               : banner,
        }
    print dir(request)
    print request.headers

    return jsonify_response(context)
    js_sdk_context          = get_jssdk_context()
    return render_template('user/user_index.html', recommend_sub_cats=recommend_sub_cats, nav={1:'active'}, **js_sdk_context)


item_filters_validator  = Inputs(
    {
     'sub_cat_id'    : Optional(IdField(msg='分类id')),
     'hospital_id'   : Optional(IdField(msg='医院id')),
     'city_id'       : Optional(IdField(msg='城市id')),
     'offset'        : Optional(TextField(min_length=1, max_length=100, msg='分页参数')),
     'sort_type'     : Optional(IntChoiceField(choices=[1,2,3,4], msg='排序选项')),
    }
    )
@wechat_loggin_dec(required=False, validator=item_filters_validator, app=True)
def item_filters():
    ''' 筛选参数列表 '''
    sub_cat_id  = request.valid_data.get('sub_cat_id')
    sort_type   = request.valid_data.get('sort_type') or 1

    order_choices   = [
        {'id':1, 'name':'综合排序'},
        {'id':2, 'name':'销量优先'},
        {'id':3, 'name':'低价优先'},
        {'id':4, 'name':'高价优先'},
        ]
    has_more, citys = DataService.get_paged_cities()

    cat_id      = None
    subcat      = None
    if sub_cat_id:
        subcat  = ItemService.get_subcat_dict_by_id(sub_cat_id)

    sort_type_obj = None
    if sort_type:
        for i in order_choices:
            if i['id'] == sort_type:
                sort_type_obj = i
    
    all_cats        = ItemService.get_item_cats()
    all_sub_cats    = ItemService.get_item_subcats()
    _, all_recommend_subcats   = ItemService.get_paged_recommend_subcats(no_limit=True)

    id_order_map               = {i['sub_cat_id']:i['sort_order'] for i in all_recommend_subcats}
    recommend_subcat_ids       = set(i['sub_cat_id'] for i in all_recommend_subcats)
    recommend_subcats          = filter(lambda i:i['id'] in recommend_subcat_ids, all_sub_cats)
    recommend_subcats.sort(key=lambda i: id_order_map[i['id']])

    item_cat                   = [
        {
            'id': 0,
            'name':'推荐',
            'sub_cats':recommend_subcats,
            'icon'  : CAT_ICONS[0],
            'icon_active'  : CAT_ICONS_ACTIVE[0]
        }]
    for cat in all_cats:
        tmp             = {'name': cat.name, 'id': cat.id}
        tmp['sub_cats'] = [i for i in all_sub_cats if cat.id in i['cat_id_list']]
        tmp['icon']     = CAT_ICONS.get(cat.id) or ''
        tmp['icon_active'] = CAT_ICONS_ACTIVE.get(cat.id) or ''
        item_cat.append(tmp)
    sort_type_obj   = sort_type_obj or order_choices[0]
    subcat          = subcat or item_cat[0]['sub_cats'][0]

    city_id         = get_current_city_id()
    city            = None
    for the_city in citys:
        if the_city['id']==city_id: city = the_city
    for i in all_sub_cats:
        if i['id'] in recommend_subcat_ids:
            i['cat_id_list'].append(0)
    city            = city or citys[0]
    result          = {
        'order_choices': order_choices,
        'data': item_cat,
        'all_sub_cats':all_sub_cats,
        'citys': citys,
        'sort_type_obj':sort_type_obj,
        'city': city,
        'subcat': subcat
        }
    #return json.dumps(result).decode('unicode-escape').encode('utf8')
    return jsonify_response(result)



hospital_filters_validator  = Inputs(
    {
     'sub_cat_id'    : Optional(IdField(msg='分类id')),
     'city_id'       : Optional(IdField(msg='城市id')),
     'offset'        : Optional(TextField(min_length=1, max_length=100, msg='分页参数')),
     'sort_type'     : Optional(IntChoiceField(choices=[1,2,3,4], msg='排序选项')),
    }
    )
@wechat_loggin_dec(required=False, validator=hospital_filters_validator, app=True)
def hospital_filters():
    ''' 筛选参数列表 '''
    sub_cat_id  = request.valid_data.get('sub_cat_id')
    sort_type   = request.valid_data.get('sort_type') or 1

    order_choices   = HOSPITAL_ORDER_CHOICES

    has_more, citys = DataService.get_paged_cities()

    cat_id      = None
    subcat      = None
    if sub_cat_id:
        subcat  = ItemService.get_subcat_dict_by_id(sub_cat_id)

    sort_type_obj = None
    if sort_type:
        for i in order_choices:
            if i['id'] == sort_type:
                sort_type_obj = i
    
    all_cats        = ItemService.get_item_cats()
    all_sub_cats    = ItemService.get_item_subcats()
    _, all_recommend_subcats   = ItemService.get_paged_recommend_subcats(limit=1000)

    id_order_map               = {i['sub_cat_id']:i['sort_order'] for i in all_recommend_subcats}
    recommend_subcat_ids       = set(i['sub_cat_id'] for i in all_recommend_subcats)
    recommend_subcats          = filter(lambda i:i['id'] in recommend_subcat_ids, all_sub_cats)
    recommend_subcats.sort(key=lambda i: id_order_map[i['id']])

    item_cat                   = [
        {
            'id': 0,
            'name':'推荐',
            'sub_cats':recommend_subcats,
            'icon'  : CAT_ICONS[0],
            'icon_active'  : CAT_ICONS_ACTIVE[0]
        }]
    total_cat                  = {'id': 0, 'name':'全部', 'cat_id_list': [0]
        }
    all_sub_cats.insert(0, total_cat)
    recommend_subcats.insert(0, total_cat)

    for cat in all_cats:
        tmp             = {'name': cat.name, 'id': cat.id}
        tmp['sub_cats'] = [i for i in all_sub_cats if cat.id in i['cat_id_list']]
        tmp['icon']     = CAT_ICONS.get(cat.id) or ''
        tmp['icon_active'] = CAT_ICONS_ACTIVE.get(cat.id) or ''
        item_cat.append(tmp)
    sort_type_obj   = sort_type_obj or order_choices[0]
    subcat          = subcat or item_cat[0]['sub_cats'][0]

    city_id         = get_current_city_id()
    city            = None
    for the_city in citys:
        if the_city['id']==city_id: city = the_city
    for i in all_sub_cats:
        if i['id'] in recommend_subcat_ids:
            i['cat_id_list'].append(0)
    city            = city or citys[0]
    result          = {
        'order_choices': order_choices,
        'data': item_cat,
        'all_sub_cats':all_sub_cats,
        'citys': citys,
        'sort_type_obj':sort_type_obj,
        'city': city,
        'subcat': subcat
        }
    return jsonify_response(result)


item_list_validator  = Inputs(
    {
     'sub_cat_id'    : Optional(IdField(msg='分类id')),
     'hospital_id'   : Optional(IdField(msg='医院id')),
     'city_id'       : Optional(IdField(msg='城市id')),
     'offset'        : Optional(TextField(min_length=1, max_length=100, msg='分页参数')),
     'sort_type'     : Optional(IntChoiceField(choices=[1,2,3,4], msg='排序选项')),
    }
    )
@wechat_loggin_dec(required=False, validator=item_list_validator, app=True)
def item_list():
    ''' 商品列表 '''
    sub_cat_id  = request.valid_data.get('sub_cat_id')
    hospital_id = request.valid_data.get('hospital_id')
    city_id     = get_current_city_id()
    offset      = request.valid_data.get('offset') or ''
    sort_type   = request.valid_data.get('sort_type') or 1

    _sort       = 'id'
    _sort_dir   = 'ASC'
    where       = and_()
    where.append(Item.status==1)
    if city_id:
        subquery= db.session.query(Hospital.id).filter(Hospital.city_id==city_id).subquery()
        where.append(Item.hospital_id.in_(subquery))
    if sub_cat_id:
        or_query= or_(
            Item.sub_cat_ids==sub_cat_id,
            Item.sub_cat_ids.like('%,{}'.format(sub_cat_id)),
            Item.sub_cat_ids.like('%,{},%'.format(sub_cat_id)),
            Item.sub_cat_ids.like('{},%'.format(sub_cat_id))
            )
        where.append(or_query)

    order_by_case = None
    offset_id   = 0
    offset_field= ''
    _sort       = 'price'
    if hospital_id:
        _sort='id'
        _sort_dir='DESC'
    if offset:
        offset_id, offset_field = offset.split('_')
        offset_id = int(offset_id)
        offset_where    = Item.id<offset_id
    if sort_type==2:
        _sort='sold_count'; _sort_dir='DESC'
        offset_field    = int(offset_field or 10**10)
        offset_where    = or_(
            Item.sold_count<offset_field,
            and_(
                Item.sold_count<=offset_field,
                Item.id<offset_id 
                )
            )
    if sort_type==3:
        order_by_case   = case([(ActivityItem.price>0, ActivityItem.price)], else_=Item.price).asc()
        _sort='price'; _sort_dir='ASC'
        offset_field    = float(offset_field or 0)
        offset_where    = or_(
            Item.price>offset_field,
            and_(
                Item.price>=offset_field,
                Item.id<offset_id 
                )
            )
    if sort_type==4:
        order_by_case   = case([(ActivityItem.price>0, ActivityItem.price)], else_=Item.price).desc()
        _sort='price'; _sort_dir='DESC'
        offset_field    = float(offset_field or 10**10)
        offset_where    = or_(
            Item.price<offset_field,
            and_(
                Item.price<=offset_field,
                Item.id<offset_id 
                )
            )
    if offset: where.append(offset_where)

    if hospital_id:
        where.append(Item.hospital_id==hospital_id)
        if offset: where.append(Item.id<offset)

    offset      = offset
    fields      = ['id', 'hospital_id', 'title', 'sold_count', 'price', 'orig_price', 'support_choice_list', 'image', 'has_fee']
    has_more, items   = ItemService.get_paged_items(where=where, order_by_case=order_by_case, fields=fields, _sort=_sort, _sort_dir=_sort_dir)

    fetch_min_period_info(items)
    fetch_hospital_refs(items, fields=['id','name'])
    offset      = ''
    if items: offset  = str(items[-1]['id']) + '_' + (str(items[-1][_sort]) if sort_type !=1 else '')
    print offset, 'offset'
    result      = {
        'code'      : ResponseCode.SUCCESS,
        'msg'       : '',
        'has_more'  : has_more,
        'infos'     : items,
        'offset'    : offset
    }
    return jsonify_response(result)



hospital_list_validator  = Inputs(
    {
     'sub_cat_id'    : Optional(IdField(msg='分类id')),
     'city_id'       : Optional(IdField(msg='城市id')),
     'offset'        : Optional(TextField(min_length=1, max_length=100, msg='分页参数')),
     'sort_type'     : Optional(IntChoiceField(choices=[1,2,3], msg='排序选项')), #1综合 2销量 3好评优先
    }
    )
@wechat_loggin_dec(required=False, validator=hospital_list_validator, app=True)
def hospital_list():
    ''' 医院列表 '''
    sub_cat_id  = request.valid_data.get('sub_cat_id')
    city_id     = get_current_city_id()
    offset      = request.valid_data.get('offset') or ''
    sort_type   = request.valid_data.get('sort_type') or 1

    _sort       = 'id'
    _sort_dir   = 'DESC'
    where       = and_()
    where.append(Hospital.status==1)
    if city_id:
        where.append(Hospital.city_id==city_id)
    if sub_cat_id:
        query     = or_(
            Item.sub_cat_ids==sub_cat_id,
            Item.sub_cat_ids.like('%,{}'.format(sub_cat_id)),
            Item.sub_cat_ids.like('%,{},%'.format(sub_cat_id)),
            Item.sub_cat_ids.like('{},%'.format(sub_cat_id))
            )
        hospital_id_sub = db.session.query(Item.hospital_id).filter(query).subquery()
        where.append(Hospital.id.in_(hospital_id_sub))

    offset_id   = 0
    offset_field= ''
    _sort       = 'sold_count'
    if offset:
        offset_id, offset_field = offset.split('_')
        offset_id = int(offset_id)
        offset_where    = Hospital.id<offset_id
    if sort_type==2:
        _sort='sold_count'; _sort_dir='DESC'
        offset_field    = int(offset_field or 10**10)
        offset_where    = or_(
            Hospital.sold_count<offset_field,
            and_(
                Hospital.sold_count<=offset_field,
                Hospital.id<offset_id 
                )
            )
    if sort_type==3:
        _sort='rate'; _sort_dir='DESC'
        offset_field    = float(offset_field or 0)
        offset_where    = or_(
            Hospital.rate>offset_field,
            and_(
                Hospital.rate>=offset_field,
                Hospital.id<offset_id 
                )
            )
    if offset: where.append(offset_where)

    offset      = offset
    fields      = ['id', 'image', 'name', 'tag_list', 'rate', 'sold_count', 'addr']
    has_more, items   = ItemService.get_paged_hospitals(where=where, fields=fields, _sort=_sort, _sort_dir=_sort_dir)

    _, sub_cats       = ItemService.get_paged_sub_cats(limit=1000)
    _, cats           = ItemService.get_paged_cats(limit=1000)

    hospital_ids      = [i['id'] for i in items]
    hospital_item_count_map = ItemService.count_hospital_items(hospital_ids)
    hospital_item_subcat_map= ItemService.get_hospital_item_cats(hospital_ids)
    for i in items:
        i['rate']           = str(format_rate(i['rate']))
        i['item_count']     = hospital_item_count_map.get(i['id']) or 0
        subcat_ids          = hospital_item_subcat_map.get(i['id']) or []
        i['cats']           = ItemService.get_sub_cat_id_name(subcat_ids, sub_cats, cats)
    offset      = ''
    if items:
        offset  = str(items[-1]['id']) + '_' + (str(items[-1][_sort]) if sort_type !=1 else '')

    result      = {
        'code'      : ResponseCode.SUCCESS,
        'msg'       : '',
        'has_more'  : has_more,
        'infos'     : items,
        'offset'    : offset
    }
    return jsonify_response(result)


def cacl_need_pay(choice, price, credit, has_fee=True):
    if has_fee:
        total   = format_price((choice.period_fee+1) * price)
    else:
        total   = price
    need_pay    = 0
    if total>credit:
        credit_amount  = format_price(credit*1.0/(1.0+choice.period_fee))
        period_amount  = format_price(credit_amount*1.0/choice.period_count)
        period_money   = format_price(credit*1.0/choice.period_count)
        period_fee     = format_price(period_money-period_amount)
        credit_used    = credit
        need_pay       = format_price(price - period_amount*choice.period_count)
    else:
        period_money   = format_price(total/choice.period_count)
        period_fee     = format_price((choice.period_fee) * price*1.0/choice.period_count)
        period_amount  = format_price(period_money-period_fee)
        credit_used    = total

    result      = {
        'id'            : choice.id,
        'need_pay'      : need_pay,
        'period_money'  : period_money,
        'period_total'  : period_money,
        'period_fee'    : period_fee,
        'fee'           : choice.period_fee,
        'total'         : total,
        'credit_used'   : credit_used,
        'credit'        : credit,
        'period_amount' : period_amount,
        'period_count'  : choice.period_count
        }
    return result


item_detail_validator  = Inputs(
    {
     'item_id'    : IdField(msg='商品id'),
    }
    )
@wechat_loggin_dec(required=False, validator=item_detail_validator, app=True)
def item_detail():
    ''' 商品详情 '''
    result          = {
        'code'      : ResponseCode.SUCCESS,
        'msg'       : ''
    }
    item_id         = request.valid_data.get('item_id')
    fields          = [
        'id', 'title', 'note', 'use_time', 'support_choice_list', 'has_fee', 'direct_buy', 'photo_list', 'hospital_id', 'price', 'orig_price']
    item            = ItemService.get_item_dict_by_id(item_id, fields=fields)
    can_comment     = PromoteService.get_fakeuser_by_userid(request.user_id)
    has_fav         = False
    if request.user_id:
        has_fav     = bool(ItemService.has_fav(item_id, request.user_id))
    assert item, '商品不存在'
    get_item_activity_price(item)

    credit_amount   = DEFAULT_CREDIT #预计额度
    verified        = False #待审核
    if request.user_id:
        credit          = CreditService.init_credit(request.user_id)
        credit_amount   = format_price(credit.total-credit.used)
        verified        = bool(credit.status)
    apply           = CreditService.get_apply_dict_by_userid(request.user_id)
    need_pay        = 0
    if item['price']>credit_amount:
        need_pay            = format_price(item['price'] - credit_amount)
        total_period_amount = credit_amount
    else:
        total_period_amount = item['price']
    period_choices  = CreditService.get_period_choices()
    choices         = []
    now             = dt_obj.now()
    for period_choice in period_choices:
        if period_choice.id not in item['support_choice_list']: continue
        tmp             = cacl_need_pay(period_choice, item['price'], credit_amount, item['has_fee'])
        if apply and apply.get('graduate_time') and not apply['graduate_time']>add_months(now, period_choice.period_count+6):
            tmp['disabled'] = True
        else:
            tmp['disabled']  = False
        if not total_period_amount: continue
        choices.append(tmp)
    if True:#item['direct_buy']:
        tmp         = {
            'id'           : 0,
            'period_amount': 0,
            'period_fee'   : 0,
            'period_total' : item['price'],
            'period_count' : 0
            }
        choices.insert(0, tmp)
    choices.sort(key=lambda i:i['period_count'], reverse=False)
    where           = ItemComment.item_id==item_id
    comment_count   = CommentService.count_comments(where)
    fields          = ['id', 'user_id', 'is_anonymous', 'content', 'rate', 'create_time', 'photo_list', 'item_id']
    has_more, comment_list    = CommentService.get_paged_comments(where=where, limit=1, fields=fields)
    fetch_user_refs(comment_list, fields=['id','name','avatar'])

    fields          = ['id', 'name', 'photo_list', 'working_time', 'phone', 'long_lat', 'desc', 'tag_list', 'addr']
    hospital        = ItemService.get_hospital_dict_by_id(item['hospital_id'], fields=fields)
    result          = {
        'code'      : ResponseCode.SUCCESS,
        'msg'       : '',
        'can_comment': bool(can_comment),
        'has_fav'   : has_fav,
        'pay_choices': choices,
        'item'      : item,
        'hospital'  : hospital,
        'credit_amount': format_price(credit_amount),
        'need_pay'  : need_pay,
        'verified'  : verified,
        'total_period_amount': total_period_amount,
        'comments'  : {
            'total'    : comment_count,
            'infos'    : comment_list,
            }
    }
    return jsonify_response(result)


item_comment_list_validator  = Inputs(
    {
     'item_id'   : IdField(msg='商品id'),
     'offset'    : Optional(TextField(min_length=1, max_length=100, msg='分页参数'))
    }
    )
@wechat_loggin_dec(required=False, validator=item_comment_list_validator, app=True)
def item_comment_list():
    ''' 评论列表 '''
    item_id     = request.valid_data.get('item_id')
    item        = ItemService.get_item_dict_by_id(item_id, fields=['id', 'image', 'title', 'hospital_id', 'price', 'orig_price'])
    assert item, '商品不存在'
    get_item_activity_price(item)
    hospital    = ItemService.get_hospital_dict_by_id(item['hospital_id'], fields=['id', 'name'])
    offset      = request.valid_data.get('offset')
    where       = ItemComment.item_id==item_id
    fields      = ['id', 'is_anonymous', 'user_id', 'item_id', 'is_re_comment', 'photo_list', 'content', 'rate', 'create_time']
    has_more, comments    = CommentService.get_paged_comments(where=where, offset=offset, fields=fields)
    fetch_user_refs(comments, fields=['id','name','avatar'])
    offset      = str(comments[-1]['id']) if comments else ''
    result      = {
        'code'      : ResponseCode.SUCCESS,
        'msg'       : '',
        'item'      : item,
        'hospital'  : hospital,
        'has_more'  : has_more,
        'infos'     : comments,
        'offset'    : offset
    }
    return jsonify_response(result)



my_item_comment_list_validator  = Inputs(
    {
     'item_id'   : IdField(msg='商品id'),
     'offset'    : Optional(TextField(min_length=1, max_length=100, msg='分页参数'))
    }
    )
@wechat_loggin_dec(required=False, validator=my_item_comment_list_validator, app=True)
def my_item_comment_list():
    ''' 我的评论列表 '''
    item_id     = request.valid_data.get('item_id')
    item        = ItemService.get_item_dict_by_id(item_id, fields=['id', 'image', 'title', 'hospital_id', 'price', 'orig_price'])
    assert item, '商品不存在'
    get_item_activity_price(item)

    hospital    = ItemService.get_hospital_dict_by_id(item['hospital_id'], fields=['id', 'name'])
    offset      = request.valid_data.get('offset')
    where       = and_(
        ItemComment.item_id==item_id,
        ItemComment.user_id==request.user_id
        )
    fields      = ['id', 'is_anonymous', 'user_id', 'is_re_comment', 'item_id', 'photo_list', 'content', 'rate', 'create_time']
    has_more, comments    = CommentService.get_paged_comments(where=where, offset=offset, fields=fields)
    fetch_user_refs(comments, fields=['id','name','avatar'])
    offset      = str(comments[-1]['id']) if comments else ''
    result      = {
        'code'      : ResponseCode.SUCCESS,
        'msg'       : '',
        'item'      : item,
        'hospital'  : hospital,
        'has_more'  : has_more,
        'infos'     : comments,
        'offset'    : offset
    }
    return jsonify_response(result)



user_fav_item_validator  = Inputs(
    {
     'item_id'   : IdField(msg='商品id'),
     'status'    : IntChoiceField(choices=[0, 1], msg='是否收藏'),
    }
    )
@wechat_loggin_dec(required=True, validator=user_fav_item_validator, app=True)
def user_fav_item():
    ''' 添加心愿单 '''
    item_id     = request.valid_data.get('item_id')
    status      = request.valid_data.get('status')
    msg         = '添加成功' if status else '已从心愿单中移除'
    if status:
        ItemService.fav_item(request.user_id, item_id)
    else:
        ItemService.unfav_item(request.user_id, item_id) 
    result      = {
        'code'      : ResponseCode.SUCCESS,
        'msg'       : msg,
    }
    return jsonify_response(result)


user_advice_validator  = Inputs(
    {
     'content'   : TextField(min_length=1, max_length=10000, msg='反馈内容'),
     'contact'   : Optional(TextField(min_length=1, max_length=100, msg='手机号'))
    }
    )
@wechat_loggin_dec(required=False, validator=user_advice_validator, app=True)
def user_advice():
    ''' 用户反馈 '''
    content     = request.valid_data.get('content')
    contact     = request.valid_data.get('contact')
    msg         = '感谢您的反馈'
    UserService.advice(request.user_id, content, contact)
    result      = {
        'code'      : ResponseCode.SUCCESS,
        'msg'       : msg,
    }
    return jsonify_response(result)




user_order_list_validator  = Inputs(
    {
     'cat'       : IntChoiceField(choices=[0,1,2,3], msg='订单类型'),
     'offset'    : Optional(TextField(min_length=0, max_length=100, msg='分页'))
    }
    )
@wechat_loggin_dec(required=True, validator=user_order_list_validator, app=True)
def user_order_list():
    ''' 我的订单列表 '''
    cat         = request.valid_data.get('cat')
    offset      = request.valid_data.get('offset')
    where       = and_()
    where.append(Order.user_id==request.user_id)
    if cat==1:#待支付
        where.append(or_(
            Order.status.in_([ORDER_STATUS.NEW_ORDER, ORDER_STATUS.TO_PAY]),
            Order.credit_verified==False,
            )
            )
    elif cat==2:#待服务
        where.append(and_(
            Order.status.in_([ORDER_STATUS.PAY_SUCCESS]),
            Order.credit_verified==True
            ))
    elif cat==3:#待评价
        subquery  = db.session.query(ItemComment.order_id).filter(ItemComment.order_id>0).subquery()
        where.append(and_(
            Order.user_finished==True,
            Order.credit_verified==True,
            ~Order.id.in_(subquery)
            )
        )
    choices     = CreditService.get_period_choices()
    choice_fee_map        = { i.id:i.period_fee for i in choices}
    choice_count_map      = { i.id:i.period_count for i in choices}
    has_more, order_list  = OrderService.get_paged_orders(where=where, offset=offset)
    fetch_item_refs(order_list, fields=['id', 'title', 'image'], keep_id=True)
    for i in order_list:
        period_fee_amount   = 0
        period_count        = 1
        credit_choice_id    = i['credit_choice_id']
        i['period_fee']     = 0
        period_money        = i['credit_amount']/period_count
        if credit_choice_id:
            period_count    = choice_count_map[credit_choice_id]
            period_money    = i['credit_amount']/period_count
            period_fee_amount   = i['total_fee']/period_count
        i['period_amount']  = format_price(period_money - period_fee_amount)
        i['period_fee']     = format_price(period_fee_amount)
        i['period_count']   = period_count

    fetch_servicecode_refrence(order_list, 'id', dest_key='service_code_dict', keep_id=True)
    order_ids           = [order['id'] for order in order_list]
    comments            = CommentService.get_comments_by_order_ids(order_ids, user_id=request.user_id)
    order_comment_map   = {i['order_id']:i['id'] for i in comments}
    print order_comment_map, 'order_comment_map'
    for order in order_list:
        order['comment'] = order_comment_map.get(order['id'])
        set_order_status(order, comment=order_comment_map.get(order['id']), servicecode=order['service_code_dict'])

    trans_list(order_list, 'status', 'status_label', ORDER_STATUS_LABEL, pop=False)

    offset      = str(order_list[-1]['id']) if order_list else ''
    fetch_hospital_refs(order_list, fields=['id', 'name', 'phone'])
    result      = {
        'code'      : ResponseCode.SUCCESS,
        'msg'       : '',
        'has_more'  : has_more,
        'infos'     : order_list,
        'offset'    : offset
    }

    return jsonify_response(result)


def wx_pay_callback():
    xml             = request.data
    LogService.log_pay_callback(PAY_METHOD.WECHAT_WEB, xml)
    notify          = Notify_pub()
    rs              = notify.check_sign(xml)
    re              = {}
    if not rs:
        re['return_code']   = 'FAIL'
        re['return_msg']    = '签名失败'
        return notify.arrayToXml(re)

    data            = notify.get_data()
    result_code     = data['result_code']
    order_no        = str(data['out_trade_no'])
    total_fee       = data['total_fee']
    transaction_id  = data['transaction_id']

    order_info      = OrderService.get_order_by_orderno(order_no)
    if not order_info:
        re['return_code']   = 'FAIL'
        re['return_msg']    = '订单不存在:'+order_no
        return notify.arrayToXml(re)

    total_price     = float(total_fee)/100
    order_price     = float(order_info.price)
    if order_price != total_price and (os.environ.get('APP_ENV')=='production'):
        print order_price, total_price, '金额不匹配'
        re['return_code']   = 'FAIL'
        re['return_msg']    = '金额不匹配'
        return notify.arrayToXml(re)

    msg             = ''
    if (order_info.status==ORDER_STATUS.PAY_SUCCESS):
        re                  = {'return_code':'SUCCESS','return_msg':'ok'}
        return notify.arrayToXml(re)
    if result_code.upper()  == 'FAIL':
        re['return_code']   = 'FAIL'
        pay_error_action(order_info)
    elif result_code.upper()=='SUCCESS':
        re['return_code']   = 'SUCCESS'
        pay_success_action(order_info, transaction_id=transaction_id, pay_method=PAY_METHOD.WECHAT_WEB)
    else:
        print 'wxpay_notify:',result_code
        re['return_code']   = 'SUCCESS'
        msg                 = '未知返回码'

    re['return_msg']        = msg
    return notify.arrayToXml(re)


def wx_repayment_callback():
    ''' 微信还款回调 '''
    xml             = request.data
    LogService.log_pay_callback(PAY_METHOD.WECHAT_WEB, xml)
    notify          = Notify_pub()
    rs              = notify.check_sign(xml)
    re              = {}
    if not rs:
        re['return_code']   = 'FAIL'
        re['return_msg']    = '签名失败'
        return notify.arrayToXml(re)

    data            = notify.get_data()
    result_code     = data['result_code']
    order_no        = str(data['out_trade_no'])
    total_fee       = data['total_fee']
    transaction_id  = data['transaction_id']

    repayment      = OrderService.get_repayment_by_orderno(order_no)
    if not repayment:
        re['return_code']   = 'FAIL'
        re['return_msg']    = '订单不存在:'+order_no
        return notify.arrayToXml(re)

    total_price     = float(total_fee)/100
    order_price     = float(repayment.price)
    if order_price != total_price and (os.environ.get('APP_ENV')=='production'):
        print order_price, total_price, '金额不匹配'
        re['return_code']   = 'FAIL'
        re['return_msg']    = '金额不匹配'
        return notify.arrayToXml(re)

    msg             = ''
    if (repayment.status==REPAYMENT_STATUS.PAY_SUCCESS):
        re                  = {'return_code':'SUCCESS','return_msg':'ok'}
        return notify.arrayToXml(re)
    if result_code.upper()  == 'FAIL':
        re['return_code']   = 'FAIL'
        repayment_error_action(repayment)
    elif result_code.upper()=='SUCCESS':
        re['return_code']   = 'SUCCESS'
        repayment_success_action(repayment, transaction_id=transaction_id, pay_method=PAY_METHOD.WECHAT_WEB)
    else:
        print 'wxpay_notify:',result_code
        re['return_code']   = 'SUCCESS'
        msg                 = '未知返回码'

    re['return_msg']        = msg
    return notify.arrayToXml(re)




def repayment_error_action(repayment):
    ''' 还款失败 '''
    pass


def repayment_success_action(repayment, **kw):
    ''' 还款成功 '''
    new_status      = REPAYMENT_STATUS.PAY_SUCCESS
    kw['status']    = new_status
    where           = and_(
        Repayment.id==repayment.id,
        Repayment.status.in_([REPAYMENT_STATUS.TO_PAY, REPAYMENT_STATUS.NEW])
        )
    count           = OrderService.update_repayment(where, **kw)
    if count:
        print '还款成功'
        log_ids     = [i['id'] for i in json.loads(repayment.data)]
        OrderService.gen_repayment_log(repayment)
        result      = CreditService.update_pay_log(log_ids)
        if repayment.price:
            CreditService.modify_credit(repayment.user_id, -(repayment.price))


def pay_error_action(order):
    ''' 支付失败 处理函数 '''
    new_status      = ORDER_STATUS.PAY_ERROR
    where           = Order.status!=ORDER_STATUS.PAY_SUCCESS
    count           = OrderService.update_order_status(order.id, new_status, where=where)
    if count:
        print 'pay error'
        pass #通知后端以及管理员


order_preview_validator  = Inputs(
    {
     'item_id'              : IdField(msg='商品id'),
     'coupon_id'            : Optional(IdField(msg='优惠券id')),
     'period_choice_id'     : Optional(IdField(msg='分期类型id'))
    }
    )
@wechat_loggin_dec(required=True, validator=order_preview_validator, app=True)
def order_preview():
    item_id             = request.valid_data.get('item_id')
    coupon_id           = request.valid_data.get('coupon_id')
    period_choice_id    = request.valid_data.get('period_choice_id') or 0
    msg                 = ''

    fields              = [
        'id', 'has_fee', 'direct_buy',
        'image', 'title', 'price', 'sub_cat_id',
        'sub_cat_id_list', 'support_choice_list', 'hospital_id', 'orig_price'
        ]
    item                = ItemService.get_item_dict_by_id(item_id, fields=fields)
    assert item, '商品不存在'
    get_item_activity_price(item)

    if period_choice_id: assert period_choice_id in item['support_choice_list'], '商品不支持该分期选项'
    #if period_choice_id==0: assert item['direct_buy'], '商品不支持直接购买'

    sub_cat_id_list     = item['sub_cat_id_list']
    sub_cats            = ItemService.get_subcats_by_ids(sub_cat_id_list)
    cat_id_list         = []
    for i in sub_cats:
        cat_id_list.extend(i['cat_id_list'])
    user_coupon         = None
    if coupon_id:
        user_coupon         = CouponService.get_user_coupon(
            coupon_id, request.user_id, item_id=item_id, cat_id_list=cat_id_list, sub_cat_id_list=sub_cat_id_list,
            item_price=item['price']
            )
        if not(user_coupon):
            msg = '此优惠券不存在, 请选择其他优惠券'
        else:
            user_coupon     = user_coupon.as_dict()


    coupon_list         = []
    where               = and_()
    where.append(UserCoupon.status==0)
    where.append(UserCoupon.user_id==request.user_id)
    where.append(UserCoupon.price<=item['price'])
    where.append(UserCoupon.end_time>dt_obj.now())

    or_query            = or_(
        UserCoupon.coupon_cat==0,
        CouponService.cat_query(cat_id_list),
        CouponService.sub_cat_query(sub_cat_id_list),
        and_(
            UserCoupon.item_id==item_id,
            UserCoupon.coupon_cat==3
            )
        )
    where.append(or_query)
    final_where    = or_(
        and_(
            where,
            UserCoupon.need==0,
        ),
        and_(
            where,
            UserCoupon.need<=item['price']
        )
        )
    has_more, user_coupons    = CouponService.get_paged_user_coupons(where=final_where, limit=100)
    user_coupons.sort(key=lambda i:i['price'], reverse=False)
    if coupon_id==None and user_coupons and not user_coupon:
        for c in user_coupons[::-1]:
            if c['price']<=item['price']:
                user_coupon       = c
    if user_coupon:
        print user_coupon['price'], item['price']
        assert user_coupon['price']<=item['price'], '优惠券金额不能超过订单总额'
    coupon_amount       = 0
    if user_coupon:
        if user_coupon['is_trial']: #试用券 金额等于商品金额
            user_coupon['price']  = item['price']
        coupon_amount = format_price(user_coupon['price'])


    fields              = ['id', 'name']
    hospital            = ItemService.get_hospital_dict_by_id(item['hospital_id'], fields=fields)

    credit              = CreditService.get_user_credit(request.user_id)
    if not credit:
        CreditService.init_credit(request.user_id)
        credit          = CreditService.get_user_credit(request.user_id)
    verified            = bool(credit.status)
    #period_choice_id为0时 直购
    credit_amount_remain= format_price(credit.total-credit.used)
    if period_choice_id==0:
        credit_amount_remain = 0

    if period_choice_id:
        period_choice       = CreditService.get_period_choice(period_choice_id)
        assert period_choice, '分期选项不存在'
        period_count        = period_choice.period_count
        result              = cacl_need_pay(
            period_choice, item['price']-coupon_amount, credit_amount_remain, item['has_fee'])
        need_pay            = result['need_pay']
        period_money        = result['period_money']
        period_amount       = result['period_amount']
        period_fee          = result['period_fee']
        credit_used         = result['credit_used']
    else:
        period_count        = 1
        period_fee          = 0
        period_amount       = 0
        period_money        = 0
        credit_used         = 0
        need_pay            = item['price'] - coupon_amount

    _, item_cats        = ItemService.get_paged_cats(limit=1000)
    _, item_subcats     = ItemService.get_paged_sub_cats(limit=1000)
    for i in user_coupons:
        i['cat_str']    = '全部适用'
        i['remain_str'] = calc_expire_remain(i['end_time'])
        set_coupon_cat_str(i, item_cats, item_subcats)
    coupon_title        = ''
    if user_coupon: coupon_title = user_coupon['title']
    result              = {
        'code'              : ResponseCode.SUCCESS,
        'msg'               : msg,
        'item'              : item,
        'hospital'          : hospital,
        'coupon_amout'      : coupon_amount,
        'coupon_title'      : coupon_title,
        'coupon_id'         : user_coupon['id'] if user_coupon else 0,
        'credit_amount'     : credit_used, #使用了的额度
        'credit_amount_can_use': credit_amount_remain , #总分期金额
        'total'             : item['price'],
        'period_count'      : period_count,
        'period_amount'     : period_amount,
        'period_fee'        : period_fee,
        'period_total'      : period_money,
        'coupon_list'       : user_coupons,
        'need_pay'          : format_price(need_pay),
        'credit_status'     : credit.status
        }

    return jsonify_response(result)


confirm_order_validator  = Inputs(
    {
     'item_id'              : IdField(msg='商品id'),
     'period_choice_id'     : Optional(IdField(msg='分期类型id')),
     'coupon_id'       : Optional(IdField(msg='优惠券id'))
    }
    )
@wechat_loggin_dec(required=True, validator=confirm_order_validator, app=True)
def confirm_order():
    item_id                 = request.valid_data.get('item_id')
    user_coupon_id          = request.valid_data.get('coupon_id')
    period_choice_id        = request.valid_data.get('period_choice_id')

    item                    = ItemService.get_item_dict_by_id(item_id)
    assert item, '商品不存在'
    get_item_activity_price(item)

    sub_cat_id_list     = item['sub_cat_id_list']
    sub_cats            = ItemService.get_subcats_by_ids(sub_cat_id_list)
    cat_id_list         = []
    for i in sub_cats:
        cat_id_list.extend(i['cat_id_list'])

    hospital_id             = item['hospital_id']

    if period_choice_id: assert period_choice_id in item['support_choice_list'], '商品不支持该分期选项'

    user_coupon             = None

    if user_coupon_id:
        user_coupon         = CouponService.get_user_coupon(
            user_coupon_id, request.user_id, item_id=item_id, cat_id_list=cat_id_list, sub_cat_id_list=sub_cat_id_list,
            item_price=item['price']
            )
        assert user_coupon, '优惠券不存在'
        assert user_coupon.status==0, '优惠券已被使用'
        assert user_coupon.end_time>dt_obj.now(), '优惠券已过期'

    total                   = item['price']
    order_no                = OrderService.create_no()
    coupon_amount           = 0
    credit_amount           = 0
    if user_coupon_id:
        if user_coupon.is_trial: #试用券 金额等于商品金额
            user_coupon.price   = item['price']
        coupon_amount = format_price(user_coupon.price)
    credit                  = CreditService.get_user_credit(request.user_id)
    credit_amount_remain    = format_price(credit.total-credit.used)
    if period_choice_id:
        assert credit.status!=CREDIT_STATUS.DEFAULT, '请先申请额度'
        assert credit.status!=CREDIT_STATUS.REJECTED, '请重新申请额度'
    credit_verified         = 1 if (credit.status==CREDIT_STATUS.VERIFIED) else 0
    if period_choice_id==0: credit_verified=1

    if period_choice_id:
        period_choice       = CreditService.get_period_choice(period_choice_id)
        assert period_choice, '分期选项不存在'
        apply       = CreditService.get_apply_dict_by_userid(request.user_id)
        now         = dt_obj.now()
        if apply and apply.get('graduate_time'):
            assert apply['graduate_time']>add_months(now, period_choice.period_count+6), '选择分期期数需小于现在到毕业前六个月的月数'
        period_count        = period_choice.period_count
        result              = cacl_need_pay(
            period_choice, item['price']-coupon_amount, credit_amount_remain, item['has_fee'])
        need_pay            = result['need_pay']
        period_money        = result['period_money']
        period_amount       = result['period_amount']
        period_fee          = result['period_fee']
        credit_used         = result['credit_used']
    else:
        period_count        = 1
        period_fee          = 0
        period_amount       = 0
        period_money        = 0
        credit_used         = 0
        need_pay            = item['price'] - coupon_amount

    if user_coupon_id:
        query       = and_(
            UserCoupon.user_id==request.user_id,
            UserCoupon.id==user_coupon_id,
            UserCoupon.status==0,
            or_(
                UserCoupon.coupon_cat==0,
                CouponService.cat_query(cat_id_list),
                CouponService.sub_cat_query(sub_cat_id_list),
                and_(
                    UserCoupon.coupon_cat==3,
                    UserCoupon.item_id==item_id
                )
            )
        )
        or_query    = or_(
            and_(
                query,
                UserCoupon.need==0,
            ),
            and_(
                query,
                UserCoupon.need<=item['price']
            )
            )
        count       = CouponService.update_user_coupon_status(or_query, 1)
        assert count, '优惠券已被使用'
    total_fee               = format_price(period_fee*period_count)
    if credit_used:
        result = CreditService.modify_credit(request.user_id, credit_used)
        assert result in {1,2}, '额度不足'
    if need_pay:
        to_status           = ORDER_STATUS.NEW_ORDER
    else:
        to_status           = ORDER_STATUS.PAY_SUCCESS
    order_id                = OrderService.add_order(
        request.user_id, item_id, hospital_id, need_pay,
        credit_used, total_fee, coupon_amount, total, period_choice_id, user_coupon_id, order_no,
        credit_verified,
        status=to_status)
    if not(need_pay) and credit_verified:#额度已通过审核 并全部用额度购买成功
        order         = OrderService.get_user_order(order_id, request.user_id)
        pay_success_action(order, need_pay=False)
    result                  = {
        'code': ResponseCode.SUCCESS,
        'msg': '',
        'order_id': order_id}
    return jsonify_response(result)


order_prepay_validator  = Inputs(
    {
     'order_id'              : IdField(msg='订单id'),
    }
    )
@wechat_loggin_dec(required=True, validator=order_prepay_validator, app=False)
def order_pay():
    order_id                 = request.valid_data.get('order_id')
    order_info               = OrderService.get_user_order(order_id, request.user_id)

    assert order_info, '订单不存在'
    if order_info.status==ORDER_STATUS.PAY_SUCCESS:
        return redirect('/user/order_pay_success/?order_id='+str(order_id))
    if order_info.price==0:
        return render_template('user/pay_success_no_cash.html', order_id=order_id)

    assert order_info.status!=ORDER_STATUS.PAY_SUCCESS, '订单已支付成功'

    open_id                  = request.open_id or 'o56qvw-ThtwfthGGlZ-XbH-3fjRc'
    wx_pay_params, err  = get_wx_pay_params(
        open_id, order_info.price, order_info.order_no, WX_PAY_NOTIFY_URL, '美分分购买商品'
        )

    if err:
        return 'error'

    print wx_pay_params, 'wx_pay_params', type(wx_pay_params)
    return render_template('user/order_pay.html', order=order_info, wx_pay_params=wx_pay_params)


repayment_pay_validator  = Inputs(
    {
     'repayment_id'              : IdField(msg='还款id'),
    }
    )
@wechat_loggin_dec(required=True, validator=repayment_pay_validator, app=False)
def repayment_pay():
    ''' 还款 '''
    repayment_id             = request.valid_data.get('repayment_id')
    repayment                = OrderService.get_user_repayment(repayment_id, request.user_id)

    assert repayment, '还款不存在'

    open_id                  = request.open_id or 'o56qvw-ThtwfthGGlZ-XbH-3fjRc'
    wx_pay_params, err  = get_wx_pay_params(
        open_id, repayment.price, repayment.order_no, WX_REPAYMENT_NOTIFY_URL, '美分分分期账单还款'
        )

    if err: return ''

    print wx_pay_params, 'wx_pay_params', type(wx_pay_params)
    return render_template('user/repayment_pay.html', repayment=repayment, wx_pay_params=wx_pay_params)




@wechat_loggin_dec(required=False, app=True)
def uploads():
    ''' https://github.com/qiniu/js-sdk '''
    token       = gen_qn_token()
    return render_template('user/upload.html', token=token)


order_detail_validator  = Inputs(
    {
     'order_id'              : IdField(msg='订单id'),
    }
    )
@wechat_loggin_dec(required=True, validator=order_detail_validator, app=True)
def order_detail():
    order_id        = request.valid_data.get('order_id')
    order_info      = OrderService.get_user_order(order_id, request.user_id)

    assert order_info, '订单不存在'

    fields          = ['id', 'title', 'price', 'orig_price', 'image', 'hospital_id']
    item            = ItemService.get_item_dict_by_id(order_info.item_id, fields=fields)
    assert item, '商品不存在'
    get_item_activity_price(item)

    _, period_choices  = CreditService.get_paged_period_choices(limit=1000)
    period_amount   = 0
    period_count    = 0
    period_fee      = 0
    for choice in period_choices:
        if order_info.credit_choice_id==choice['id']:
            period_count  = choice['period_count']
            period_money  = format_price((order_info.credit_amount)/period_count)
            period_fee    = format_price(order_info.total_fee/period_count)
            period_amount = format_price(period_money - period_fee)
    fields          = ['id', 'addr', 'long_lat', 'tag_list', 'phone', 'name']
    hospital        = ItemService.get_hospital_dict_by_id(item['hospital_id'], fields=fields)

    service_code    = ''
    service_status  = 0
    service_code_dict = {}
    if order_info.credit_verified==1 and order_info.status in {ORDER_STATUS.PAY_SUCCESS, ORDER_STATUS.FINISH}:
        service         = OrderService.get_servicecode(order_id)
        assert service, '服务码不存在'
        service_code_dict = service.as_dict()
        service_code    = service.code
        service_status  = service.status
    order_info      = order_info.as_dict()
    cancel_msg      = '确认取消订单吗'
    if order_info['price'] and order_info['status']==ORDER_STATUS.PAY_SUCCESS:
        repayment_amount= OrderService.get_order_repayment_logs_amount(order_id)
        repayment_amount= sum([format_price(i['price']) for i in repayment_amount.values()]  or [0])
        refund_total    = order_info['price']+repayment_amount
        if repayment_amount:
            cancel_msg      = '取消订单将退还首付金额{}元和已还款金额{}元，是否取消订单？'.format(order_info['price'], repayment_amount)
        else:
            cancel_msg      = '取消订单将退还首付金额{}元，是否取消订单？'.format(order_info['price'])
    comment         = CommentService.get_comment(ItemComment.order_id==order_id)
    set_order_status(order_info, comment=comment, servicecode=service_code_dict)

    order_info.update({
        'period_fee'    : format_price(period_fee),
        'period_count'  : period_count,
        'period_amount' : format_price(period_amount)
        })
    order_info['status_labbel'] = ORDER_STATUS_LABEL.get(order_info['status'])
    result          = {
        'cancel_msg'    : cancel_msg,
        'item'          : item,
        'service_code'  : service_code,
        'service_status': service_status,
        'hospital'      : hospital,
        'order_info'    : order_info
        }
    return jsonify_response(result)


comment_post_validator  = Inputs(
    {
     'order_id'             : Optional(IdField(msg='订单id')),
     'item_id'              : Optional(IdField(msg='商品id')),
     'content'              : TextField(min_length=1, max_length=10000, msg='评价内容'),
     'photos'               : Optional(TextField(min_length=0, max_length=10000, msg='逗号分隔的图片列表')),
     'is_anonymous'         : IntChoiceField(choices=[0,1], msg='是否匿名'),
     'rate'                 : IntChoiceField(choices=range(1,6), msg='评星'),
    }
    )
@wechat_loggin_dec(required=True, validator=comment_post_validator, app=True)
def comment_post():
    order_id            = request.valid_data.get('order_id')
    item_id             = request.valid_data.get('item_id')
    content             = request.valid_data.get('content')
    photos              = request.valid_data.get('photos')
    is_anonymous        = request.valid_data.get('is_anonymous')
    rate                = request.valid_data.get('rate')
    order               = OrderService.get_user_order(order_id, request.user_id)
    can_comment         = PromoteService.get_fakeuser_by_userid(request.user_id)
    if not can_comment:
        assert order, '订单不存在'
    assert order_id or item_id, '请评论商品'
    if order:
        item_id         = order.item_id
    item                = ItemService.get_item_dict_by_id(item_id)
    assert item, '商品不存在'
    query               = and_()
    query.append(ItemComment.user_id==request.user_id)
    if order_id: query.append(ItemComment.order_id==order_id)
    if item_id: query.append(ItemComment.item_id==item_id)
    exists              = bool(CommentService.get_comment(query))
    comment_id          = CommentService.comment_item(
            item_id or order.item_id, request.user_id, content, photos, rate, is_anonymous,
            order_id,
            is_re_comment=exists
        )
    CommentService.rerate_hospital(item['hospital_id'])

    result              = {
        'code'             : ResponseCode.SUCCESS,
        'msg'              : '评论成功',
        'comment_id'       : comment_id,
        'item_id'          : item_id or order.item_id
        }
    return jsonify_response(result)



my_period_bill_validator  = Inputs(
    {
     'cat'                 : IntChoiceField(choices=range(1,3), msg='还款日期类型'),
    }
    )
@wechat_loggin_dec(required=True, validator=my_period_bill_validator, app=True)
def my_period_bill():
    cat             = request.valid_data.get('cat')
    deadline        = get_due_time(cat-1)
    start, end      = get_current_period()
    where           = or_()

    title, thedeadline = deadline_zh(deadline)
    where.append(PeriodPayLog.deadline==deadline)
    if cat==1: #本期包括逾期的
        where.append(
            and_(
                PeriodPayLog.deadline<deadline,
                PeriodPayLog.status==0,
            )
        )
        where.append(#已逾期但在本月还款了的
            and_(
                 PeriodPayLog.deadline<deadline,
                 PeriodPayLog.status==1,
                 PeriodPayLog.repayment_time>=start+day_delta,
                 PeriodPayLog.repayment_time<=dt_obj.now(),
            )
        )
    where           = and_(
        PeriodPayLog.status.in_([0,1]),
        where)
    logs            = CreditService.get_period_pay_logs(request.user_id, where)

    total           = 0
    repayed         = 0
    logs            = [i.as_dict() for i in logs]
    for log in logs:
        get_delayed_info(log)
        total       += log['fee'] + log['amount'] + log['punish']
        log['create_time_str'] = get_time_str_from_dt(log['create_time'], '%Y.%m.%d')
        if log['status']==1:
            repayed += log['fee'] + log['amount'] + log['punish']
        else:
            if log['deadline']!=str(deadline):
                cacl_punish_fee(log) #预期未还分期 动态计算滞纳金
                total   += log['punish']

    fetch_order_refs(logs)
    for log in logs:
        log['item_id']  = log['order']['item_id']
    fetch_item_refs(logs, fields=['id', 'title'])
    remain          = total - repayed
    result          = {
        'total'          : format_price(total),
        'remain'         : format_price(remain),
        'repayed'        : format_price(repayed),
        'infos'          : logs,
        'title'          : title,
        'deadline'       : thedeadline,
        }
    return jsonify_response(result)


import os
@wechat_loggin_dec(required=True, app=True)
def user_home():
    user            = UserService.get_user_by_id(request.user_id)

    user_credit     = CreditService.init_credit(request.user_id)
    where           = and_(
        UserCoupon.user_id==request.user_id,
        UserCoupon.status==0,
        UserCoupon.end_time>dt_obj.now()
        )
    coupon_count    = CouponService.count_coupon(where)

    verified        = bool(user_credit.status)
    total           = user_credit.total
    remain          = user_credit.total - user_credit.used
    apply_status    = user_credit.status #0未申请 1申请中 2已通过 3被拒绝
    period_to_pay   = 0

    deadline        = get_due_time(0)
    start, end      = get_current_period()
    where           = or_(
        )
    where.append(
        and_(
            PeriodPayLog.deadline<=deadline,
            PeriodPayLog.status==0,
        )
    )
    logs            = CreditService.get_period_pay_logs(request.user_id, where)
    logs            = [i.as_dict() for i in logs]
    has_delayed     = False
    for log in logs:
        if not has_delayed and log['status']==0:
            has_delayed = str(dt_obj.now())>log['deadline']
        if log['status']==1: continue
        period_to_pay +=  log['fee'] + log['amount']
        if not(log['repayment_time']) and str(dt_obj.now())>log['deadline']:
            cacl_punish_fee(log)
            period_to_pay     +=  log['punish']
    remain_days     = get_date_delta(str(dt_obj.now())[:19], str(deadline)[:19])
    can_edit_name   = not UserService.get_edit_name_log(request.user_id)
    if os.environ.get('APP_ENV')!='production': can_edit_name = True
    result          = {
        'has_delayed'   : has_delayed,
        'can_edit_name' : can_edit_name,
        'total'         : float(total),
        'remain'        : float(remain),
        'coupon_count'  : coupon_count,
        'apply_status'  : apply_status,
        'user'          : user.as_dict(),
        'period_to_pay' : format_price(period_to_pay), #本期应还
        'remain_days'   : remain_days,
        }

    return jsonify_response(result)


my_repayments_validator  = Inputs(
    {
     'offset'               : Optional(TextField(min_length=0, max_length=100, msg='分页参数'))
    }
)
@wechat_loggin_dec(required=True, validator=my_repayments_validator, app=True)
def my_repayments():
    ''' 还款历史 '''
    offset              = request.valid_data.get('offset')
    where               = and_()
    where.append(and_(
        PeriodPayLog.user_id==request.user_id,
        PeriodPayLog.status==1
        ))
    if offset:
        log_id, pay_time = offset.split('_')
        pay_datetime     = dt_obj.fromtimestamp(float(pay_time))
        where.append(or_(PeriodPayLog.repayment_time<pay_datetime, and_(PeriodPayLog.repayment_time==pay_datetime, PeriodPayLog.id<log_id)))
    has_more, logs      = CreditService.get_paged_pay_logs(where=where, _sort='repayment_time')
    offset              = ''
    if logs: offset     = str(logs[-1]['id']) + '_' + str(get_timestamp(logs[-1]['repayment_time']))

    fetch_order_refs(logs)
    for log in logs:
        log['item_id']  = log['order']['item_id']
    fetch_item_refs(logs, fields=['id', 'title'])
    result              = {
        'infos'             : logs,
        'has_more'          : has_more,
        'offset'            : offset
        }
    return jsonify_response(result)


@wechat_loggin_dec(required=False, app=True)
def item_cats():
    all_cats        = ItemService.get_item_cats()
    all_sub_cats    = ItemService.get_item_subcats()
    _, all_recommend_subcats   = ItemService.get_paged_recommend_subcats(no_limit=True)

    id_order_map               = {i['sub_cat_id']:i['sort_order'] for i in all_recommend_subcats}
    recommend_subcat_ids       = set(i['sub_cat_id'] for i in all_recommend_subcats)
    recommend_subcats          = filter(lambda i:i['id'] in recommend_subcat_ids, all_sub_cats)
    recommend_subcats.sort(key=lambda i: id_order_map[i['id']])

    data                        = [
        {
            'id': 0,
            'name':'推荐',
            'sub_cats':recommend_subcats,
            'icon'  : CAT_ICONS[0],
            'icon_active'  : CAT_ICONS_ACTIVE[0]
        }]
    for cat in all_cats:
        tmp             = {'name': cat.name, 'id': cat.id}
        tmp['sub_cats'] = [i for i in all_sub_cats if cat.id in i['cat_id_list']]
        tmp['icon']         = CAT_ICONS.get(cat.id)
        tmp['icon_active']  = CAT_ICONS_ACTIVE.get(cat.id)
        data.append(tmp)

    for i in all_sub_cats:
        if i['id'] in recommend_subcat_ids:
            i['cat_id_list'].append(0)

    result          = {
        'data':data,
        'all_sub_cats':all_sub_cats
        }
    return jsonify_response(result)
    #return render_template('user/item_cats.html', nav={2:'active'}, data=data)


my_favs_validator  = Inputs(
    {
     'offset'               : Optional(TextField(min_length=0, max_length=100, msg='分页参数'))
    }
)
@wechat_loggin_dec(required=True, validator=my_favs_validator, app=True)
def my_favs():
    ''' 我的心愿单 '''
    offset              = request.valid_data.get('offset')
    where               = ItemFav.user_id==request.user_id
    has_more, favs      = ItemService.get_paged_fav_items(where=where, offset=offset)

    period_choices      = CreditService.get_period_choices()

    fetch_item_refs(favs, fields=['id', 'image', 'title','support_choice_list','price','orig_price','hospital_id'])
    items               = [i['item'] for i in favs]
    print favs, 'favs'
    fetch_hospital_refs(items, fields=['id','name'])
    item_ids            = [i['item']['id'] for i in favs]
    activity            = ActivityService.get_current_activity()
    activity_id         = None
    if activity: activity_id = activity['id']
    price_map           = ItemService.get_activity_prices(item_ids, activity_id)
    for i in favs:
        activity_price  = price_map.get(i['item']['id'])
        if activity_price: i['item']['price'] = activity_price
    fetch_min_period_info(items)
    offset              = ''
    if favs: offset     = str(favs[-1]['id'])
    result              = {
        'has_more'      : has_more,
        'infos'         : favs,
        'offset'        : offset
        }

    return jsonify_response(result)


my_coupons_validator  = Inputs(
    {
     'cat'                  : IntChoiceField(choices=[1,2,3], msg='优惠券类型'), #1未使用 2已使用 3已过期
     'offset'               : Optional(TextField(min_length=0, max_length=100, msg='分页参数'))
    }
)
@wechat_loggin_dec(required=True, validator=my_coupons_validator, app=True)
def my_coupons():
    ''' 我的优惠券 '''
    offset                        = request.valid_data.get('offset')
    cat                           = request.valid_data.get('cat')

    where                         = None
    filters                       = [UserCoupon.user_id==request.user_id]
    if cat==1:
        filters.append(
            and_(
                UserCoupon.status==0,
                UserCoupon.end_time>dt_obj.now()
            )
        )
    elif cat==2:
        filters.append(
            and_(
                 UserCoupon.status==1
            )
        )
    elif cat==3:
        filters.append(
            and_(
                 UserCoupon.status==0,
                 UserCoupon.end_time<=dt_obj.now()
            )
        )
    where                         = and_(*filters)
    has_more, user_coupons        = CouponService.get_paged_user_coupons(where=where, offset=offset)

    fields                        = ['id','title']
    fetch_item_refs(user_coupons, fields=fields, keep_id=True)

    offset                        = ''
    if user_coupons: offset = str(user_coupons[-1]['id'])

    _, item_cats        = ItemService.get_paged_cats()
    _, item_subcats     = ItemService.get_paged_sub_cats()
    for coupon in user_coupons:
        coupon['remain_str'] = calc_expire_remain(coupon['end_time'], coupon['status'])
        set_coupon_cat_str(coupon, item_cats, item_subcats)
    result  = {
        'has_more': has_more,
        'infos'   : user_coupons,
        'offset'  : offset,
        }
    return jsonify_response(result)


@wechat_loggin_dec(required=True, app=True)
def my_apply():
    ''' 我的额度申请 '''
    apply       = CreditService.get_apply_dict_by_userid(request.user_id)
    result      = {
        'data': apply
        }
    return jsonify_response(result)


help_validator  = Inputs(
    {
     'cat_id'            : Optional(IdField(msg='分类id')),
    }
)
@wechat_loggin_dec(validator=help_validator, app=True)
def help():
    ''' 帮助 '''
    cat_id         = request.valid_data.get('cat_id')

    where          = None
    if cat_id: where = HelpCat.id==cat_id
    has_more, cats = DataService.get_paged_helpcats(where=where)

    has_more, entries     = DataService.get_paged_helpentries()

    for cat in cats:
        cat['entry_list'] = [ i for i in entries if i['cat_id']==cat['id'] ]
        if not cat_id:
            cat['entry_list'] = cat['entry_list'][:4]

    result         = {          
        'data'  : cats              
        }
    return jsonify_response(result)


help_html_validator  = Inputs(
    {
     'cat_id'            : Optional(IdField(msg='分类id')),
    }
)
@wechat_loggin_dec(required=False, validator=help_html_validator, app=True)
def help_html():
    ''' 帮助页面 '''
    cat_id         = request.valid_data.get('cat_id')

    where          = None
    if cat_id: where = HelpCat.id==cat_id
    has_more, cats = DataService.get_paged_helpcats(where=where)

    has_more, entries     = DataService.get_paged_helpentries()

    for cat in cats:
        cat['entry_list'] = [ i for i in entries if i['cat_id']==cat['id'] ]
        if not cat_id:
            cat['entry_list'] = cat['entry_list'][:4]

    result         = {          
        'data'  : cats              
        }
    return render_template('user/help-center.html', cats=cats, cat_id=cat_id)
    return jsonify_response(result)



help_entry_validator  = Inputs(
    {
     'entry_id'          : IdField(msg='条目id')
    }
)
@wechat_loggin_dec(required=False, validator=help_entry_validator, app=True)
def get_help_entry():
    ''' 帮助条目详情 '''
    entry_id        = request.valid_data.get('entry_id')

    entry           = DataService.get_helpentry_by_id(entry_id)
    result          = {
        'data'          : entry
        }
    contact         = CONTACT
    return render_template('user/help-center-detail.html', entry=entry, contact=contact)
    return jsonify_response(result)


@wechat_loggin_dec(app=True)
def apply_credit_page():
    ''' 额度申请 '''
    return render_template('user/apply_one.html')


project_doctor_description_validator  = Inputs(
    {
     'item_id'          : IdField(msg='商品id')
    }
)
@wechat_loggin_dec(required=False, validator=project_doctor_description_validator, app=True)
def project_doctor_description():
    ''' 项目医生图文介绍'''
    item_id         = request.args.get('item_id')
    item            = ItemService.get_item_dict_by_id(item_id)

    return render_template('user/doctor_hospital_desc.html', item=item)


def get_jssdk_js():
    print request
    print request.headers
    print type(request.headers)
    print dir(request.headers)

    sign_user   = get_cookie('sign_user') or ''
    if sign_user:
        sign_user = '&sign_user='+sign_user

    referer     = request.headers.get('Referer') or ''
    if '127.0.0.1' in referer:
        sign_user = '&sign_user=' + '2.2074eb5e01c2093a5f5f9586955d5414'
    browser     = request.headers.get('User-Agent')
    context     = get_jssdk_context(referer)
    text        = render_template('js_sdk.js', token=sign_user, **context)
    return js_response(text)


def get_school_list():
    ''' 学校选择列表 '''
    limit       = 3000
    fields      = ['id', 'name']
    where       = School.city_name=='上海'
    _, schools  = DataService.get_paged_schools(
        where=where, limit=limit, fields=fields)

    result      = {
        'code'      : ResponseCode.SUCCESS,
        'msg'       : '',
        'infos'     : schools
        }
    return jsonify_response(result)



repayment_validator  = Inputs(
    {
     'data'          : JsonField(msg='请选择还款数据')
    }
)
@wechat_loggin_dec(validator=repayment_validator, app=True)
def repayment():
    ''' 选择还款'''
    data            = request.valid_data.get('data')

    user_id         = request.user_id
    pay_method      = None
    price           = 0
    assert data, '请选择还款'
    for log in data:
        assert str(log.get['amount']).isdigit() and str(log.get['fee']).isdigit() and str(log.get['punish']).isdigit(), '数据格式错误'
        price += float(log['punish']) + float(log['fee']) + float(log['amount'])
    coupon_id       = None
    order_no        = OrderService.create_no()
    repayment_id    = OrderService.repayment(user_id, pay_method, coupon_id, price, json.dumps(data), order_no)

    msg             = ''
    result          = {
        'code'         : ResponseCode.SUCCESS,
        'msg'          : msg,
        'repayment_id'         : repayment_id
        }
    return jsonify_response(result)




hospital_detail_validator  = Inputs(
    {
     'hospital_id': IdField(msg='医院id')
    }
)
@wechat_loggin_dec(required=False, validator=hospital_detail_validator)
def hospital_detail():
    ''' 医院详情 '''
    hospital_id     = request.valid_data.get('hospital_id')
    fields          = ['id', 'name', 'photo_list', 'working_time', 'phone', 'long_lat', 'desc', 'tag_list', 'addr']
    hospital        = ItemService.get_hospital_dict_by_id(hospital_id, fields=fields)

    where       = Item.hospital_id==hospital_id
    fields      = ['id', 'photo_list', 'title', 'price', 'orig_price', 'support_choice_list', 'image', 'has_fee']
    has_more, items   = ItemService.get_paged_items(where=where, fields=fields, limit=5)

    fetch_min_period_info(items)
    result      = {
        'code': ResponseCode.SUCCESS,
        'msg': '',
        'hospital': hospital,
        'infos': items
        }
    return render_template('user/hospital_detail.html', **result)
    return jsonify_response(result)



@wechat_loggin_dec(required=None)
def get_city_list():
    ''' 城市列表 '''
    has_more, infos     = DataService.get_paged_city_list()

    result              = {
        'code'             : ResponseCode.SUCCESS,
        'msg'              : '',
        'infos'            : infos,
        }
    return jsonify_response(result)



upload_image_validator  = Inputs(
    {
     'image_cat'          : ChoiceField(choices=['avatar', 'comment', 'apply', 'room'], msg='图片类型')
    }
    )
@wechat_loggin_dec(validator=upload_image_validator)
def upload_image():
    try:
        file    = request.files['file']
        img_cat = request.valid_data.get('image_cat')
        code    = 0
        msg     = '上传成功'
        content = file.read()
        key     = img_cat+ '/' + str(time.time()) + '.jpg'
        upload_img(key, content)
        if img_cat=='avatar':
            UserService.update_user(request.user_id, avatar=key)
        return jsonify_response({
            'code' : ResponseCode.SUCCESS,
            'msg'  : '',
            'image': key,
            'fullpath': prefix_img_domain(key)
            })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify_response({'msg':'服务器异常','code': 10000})



apply_credit_post_validator  = Inputs(
    {
#      'name'               : Optional(TextField(min_length=0, max_length=100, msg='姓名')),
#      'id_no'              : TextField(min_length=0, max_length=100, msg='身份证号'),
#      'school'             : TextField(min_length=0, max_length=100, msg='学校'),
#      'enrollment_time'    : TextField(min_length=0, max_length=100, msg='入学时间'),
       'graduate_time'      : REGField(pattern='\d{4}-\d{1,2}', msg='请输入毕业时间格式如：2015-01'),
#      'major'              : TextField(min_length=0, max_length=100, msg='专业'),
#      'stu_no'             : TextField(min_length=0, max_length=100, msg='学号'),
#      'stu_education'      : TextField(min_length=0, max_length=100, msg='学历'),
#      'addr'               : TextField(min_length=0, max_length=100, msg='地址'),
     'parent_contact'     : TextField(min_length=0, max_length=100, msg='父母联系方式'),
     'chsi_name'          : TextField(min_length=0, max_length=100, msg='学信网账号'),
     'chsi_passwd'        : TextField(min_length=0, max_length=100, msg='学信网密码'),
     'body_choice_ids'        : Optional(TextField(min_length=0, max_length=100, msg='你满意的部位')),
     'body_choice_text'        : Optional(TextField(min_length=0, max_length=100, msg='其他内容')),
    }
    )
@wechat_loggin_dec(validator=apply_credit_post_validator)
def apply_credit_post():
#     request.valid_data['enrollment_time'] = '{}-01 00:00:00'.format(request.valid_data['enrollment_time'])
    request.valid_data['graduate_time']   = '{}-01 00:00:00'.format(request.valid_data['graduate_time'])
    body_choice_ids     = request.valid_data['body_choice_ids']
    body_choice_text    = request.valid_data['body_choice_text']
     
    apply_id       = CreditService.add_apply(request.user_id, **request.valid_data)
    if not apply_id:
        where      = and_(
            CreditApply.user_id==request.user_id,
            CreditApply.status!=APPLY_STATUS.VERIFIED
            )
        request.valid_data['create_time'] = dt_obj.now()
        request.valid_data['status']      = 1
        CreditService.update_apply(where, **request.valid_data)

    CreditService.update_user_credit_status(request.user_id, CREDIT_STATUS.VERIFYING)
    result         = {
        'code'        : ResponseCode.SUCCESS,
        'msg'         : ''
    }
    return jsonify_response(result)



apply_credit_photo_validator  = Inputs(
    {
     'id_card_photo'               : TextField(min_length=0, max_length=100, msg='身份证号码'),
     'stu_card_photo'              : TextField(min_length=0, max_length=100, msg='学生证号'),
    }
    )
@wechat_loggin_dec(validator=apply_credit_photo_validator)
def apply_credit_photo():
    ''' '''
    id_card_photo       = request.valid_data.get('id_card_photo')
    stu_card_photo      = request.valid_data.get('stu_card_photo')

    where               = CreditApply.user_id==request.user_id
    CreditService.update_apply(where, id_card_photo=id_card_photo, stu_card_photo=stu_card_photo, status=APPLY_STATUS.SECOND_STEP)
    CreditService.update_user_credit_status(request.user_id, CREDIT_STATUS.VERIFYING)

    result         = {
        'code'        : ResponseCode.SUCCESS,
        'msg'         : ''
    }
    return jsonify_response(result)


edit_name_validator  = Inputs(
    {
     'name'               : TextField(min_length=0, max_length=100, msg='修改名字'),
    }
    )
@wechat_loggin_dec(required=True, validator=edit_name_validator, app=True)
def edit_name():
    ''' 修改名字 '''
    name        = request.valid_data.get('name')
    print name
    count       = UserService.update_name(request.user_id, name)

    if count:
        UserService.add_edit_name_log(request.user_id)
    result      = {
        'code'     : ResponseCode.SUCCESS,
        'msg'       : '修改成功'
        }
    return jsonify_response(result)



def get_current_city_id():
    ''' 获取当期城市id '''
    city_id     = request.valid_data.get('city_id')
    city_code   = get_cookie('choose_city_code') or get_cookie('city_code')
    if city_id:
        return city_id
    elif city_code:
        city    = DataService.get_city_by_baidu_city_code(city_code)
        if city: return city.id

    return 1



item_list_html_validator  = Inputs(
    {
     'sub_cat_id'    : Optional(IdField(msg='分类id')),
     'hospital_id'   : Optional(IdField(msg='医院id')),
     'city_id'       : Optional(IdField(msg='城市id')),
     'offset'        : Optional(TextField(min_length=1, max_length=100, msg='分页参数')),
     'sort_type'     : Optional(IntChoiceField(choices=[1,2,3,4], msg='排序选项')),
    }
    )
@wechat_loggin_dec(required=False, validator=item_list_html_validator)
def item_list_html():
    ''' 商品列表 '''
    sub_cat_id  = request.valid_data.get('sub_cat_id')
    sort_type   = request.valid_data.get('sort_type') or 1

    order_choices   = [
        {'id':1, 'name':'综合排序'},
        {'id':2, 'name':'销量优先'},
        {'id':3, 'name':'低价优先'},
        {'id':4, 'name':'高价优先'},
        ]
    has_more, citys = DataService.get_paged_cities()


    cat_id      = None
    subcat      = None
    if sub_cat_id:
        subcat  = ItemService.get_subcat_dict_by_id(sub_cat_id)

    sort_type_obj = None
    if sort_type:
        for i in order_choices:
            if i['id'] == sort_type:
                sort_type_obj = i
    
    all_cats        = ItemService.get_item_cats()
    all_sub_cats    = ItemService.get_item_subcats()
    _, all_recommend_subcats   = ItemService.get_paged_recommend_subcats(limit=1000)

    id_order_map               = {i['sub_cat_id']:i['sort_order'] for i in all_recommend_subcats}
    recommend_subcat_ids       = set(i['sub_cat_id'] for i in all_recommend_subcats)
    recommend_subcats          = filter(lambda i:i['id'] in recommend_subcat_ids, all_sub_cats)
    recommend_subcats.sort(key=lambda i: id_order_map[i['id']])

    item_cat                   = [
        {
            'id': 0,
            'name':'推荐',
            'sub_cats':recommend_subcats,
            'icon'  : CAT_ICONS[0],
            'icon_active'  : CAT_ICONS_ACTIVE[0]
        }]
    for cat in all_cats:
        tmp             = {'name': cat.name, 'id': cat.id}
        tmp['sub_cats'] = [i for i in all_sub_cats if cat.id in i['cat_id_list']]
        tmp['icon']     = CAT_ICONS.get(cat.id) or ''
        tmp['icon_active'] = CAT_ICONS_ACTIVE.get(cat.id) or ''
        item_cat.append(tmp)
    sort_type_obj   = sort_type_obj or order_choices[0]
    subcat          = subcat or item_cat[0]['sub_cats'][0]

    city_id         = get_current_city_id()
    city            = None
    for the_city in citys:
        if the_city['id']==city_id: city = the_city

    for i in all_sub_cats:
        if i['id'] in recommend_subcat_ids:
            i['cat_id_list'].append(0)
    city            = city or citys[0]
    result          = {
        'order_choices': order_choices,
        'data': item_cat,
        'all_sub_cats':all_sub_cats,
        'citys': citys,
        'sort_type_obj':sort_type_obj,
        'city': city,
        'subcat': subcat
        }
    if request.args.get('json'):
        return jsonify_response(result)
    return render_template('user/item_list.html', **result)


hospital_list_html_validator  = Inputs(
    {
     'sub_cat_id'    : Optional(IdField(msg='分类id')),
     'hospital_id'   : Optional(IdField(msg='医院id')),
     'city_id'       : Optional(IdField(msg='城市id')),
     'offset'        : Optional(TextField(min_length=1, max_length=100, msg='分页参数')),
     'sort_type'     : Optional(IntChoiceField(choices=[1,2,3,4], msg='排序选项')),
    }
    )
@wechat_loggin_dec(required=False, validator=hospital_list_html_validator)
def hospital_list_html():
    ''' 医院列表 '''
    sub_cat_id  = request.valid_data.get('sub_cat_id')
    sort_type   = request.valid_data.get('sort_type') or 1

    order_choices   = HOSPITAL_ORDER_CHOICES
    has_more, citys = DataService.get_paged_cities()


    cat_id      = None
    subcat      = None
    if sub_cat_id:
        subcat  = ItemService.get_subcat_dict_by_id(sub_cat_id)

    sort_type_obj = None
    if sort_type:
        for i in order_choices:
            if i['id'] == sort_type:
                sort_type_obj = i
    
    all_cats        = ItemService.get_item_cats()
    all_sub_cats    = ItemService.get_item_subcats()
    _, all_recommend_subcats   = ItemService.get_paged_recommend_subcats(limit=1000)

    id_order_map               = {i['sub_cat_id']:i['sort_order'] for i in all_recommend_subcats}
    recommend_subcat_ids       = set(i['sub_cat_id'] for i in all_recommend_subcats)
    recommend_subcats          = filter(lambda i:i['id'] in recommend_subcat_ids, all_sub_cats)
    recommend_subcats.sort(key=lambda i: id_order_map[i['id']])
    total_cat                  = {'id': 0, 'name':'全部', 'cat_id_list': [0]
        }
    all_sub_cats.insert(0, total_cat)
    recommend_subcats.insert(0, total_cat)
    item_cat                   = [
        {
            'id': 0,
            'name':'推荐',
            'sub_cats':recommend_subcats,
            'icon'  : CAT_ICONS[0],
            'icon_active'  : CAT_ICONS_ACTIVE[0]
        }]
    for cat in all_cats:
        tmp             = {'name': cat.name, 'id': cat.id}
        tmp['sub_cats'] = [i for i in all_sub_cats if cat.id in i['cat_id_list']]
        tmp['icon']     = CAT_ICONS.get(cat.id) or ''
        tmp['icon_active'] = CAT_ICONS_ACTIVE.get(cat.id) or ''
        item_cat.append(tmp)
    sort_type_obj   = sort_type_obj or order_choices[0]
    subcat          = subcat or item_cat[0]['sub_cats'][0]

    city_id         = get_current_city_id()
    city            = None
    for the_city in citys:
        if the_city['id']==city_id: city = the_city

    for i in all_sub_cats:
        if i['id'] in recommend_subcat_ids:
            i['cat_id_list'].append(0)
    city            = city or citys[0]
    result          = {
        'order_choices': order_choices,
        'data': item_cat,
        'all_sub_cats':all_sub_cats,
        'citys': citys,
        'sort_type_obj':sort_type_obj,
        'city': city,
        'subcat': subcat
        }
    if request.args.get('json'):
        return jsonify_response(result)
    return render_template('user/hospital_list.html', **result)



@wechat_loggin_dec(required=False)
def menu_credit_apply():
    ''' 额度申请菜单入口 '''
    if not request.user_id:
        return redirect('/static/user/login.html?next=/user/menu_credit_apply/')
        #return send_from_directory('static/user/', 'login.html')
    apply   = CreditService.get_apply_dict_by_userid(request.user_id)
    if apply:
#         if apply['status']==1:
#             return redirect('static/user/applyer-pic.html')
        predict_time = str(get_next_working_day(str(apply['create_time'])))[:10]
        return render_template('user/apply_result.html', apply=apply, predict_time=predict_time)
    else:
        return redirect('static/user/applyer-infor.html')




my_order_bill_validator  = Inputs(
    {
     'order_id'                 : IdField(msg='订单id')
    }
    )
@wechat_loggin_dec(required=True, validator=my_order_bill_validator, app=True)
def my_order_bill():
    order_id        = request.valid_data.get('order_id')
    order           = OrderService.get_user_order(order_id, request.user_id)
    assert order, '订单不存在'

    where           = or_(
        )
    where.append(PeriodPayLog.order_id==order_id)

    order           = OrderService.get_order_by_id(order_id)
    item            = ItemService.get_item_dict_by_id(order.item_id)
    hospital        = ItemService.get_hospital_dict_by_id(item['hospital_id'], fields=['id','name'])
    logs            = CreditService.get_period_pay_logs(request.user_id, where)

    total           = 0
    repayed         = 0
    logs            = [i.as_dict() for i in logs]
    for log in logs:
        get_delayed_info(log)
        total       += log['fee'] + log['amount'] + log['punish']
        if log['status']==1:
            repayed += log['fee'] + log['amount'] + log['punish']
        else:
            if log['delayed']:
                cacl_punish_fee(log) #预期未还分期 动态计算滞纳金
                total   += log['punish']

    fetch_order_refs(logs)
    for log in logs:
        log['item_id']  = log['order']['item_id']
    fetch_item_refs(logs, fields=['id', 'title'])
    remain          = total - repayed
    item['price']   = format_price(order.total)

    result          = {
        'item'           : item,
        'total'          : format_price(total),
        'hospital'       : hospital,
        'repayed'        : format_price(repayed),
        'remain'         : format_price(remain),
        'infos'          : logs,
        }
    return jsonify_response(result)



hospital_item_list_validator  = Inputs(
    {
     'hospital_id'                 : IdField(msg='医院id')
    }
    )
@wechat_loggin_dec(required=False, validator=hospital_item_list_validator)
def hospital_item_list():
    hospital_id = request.valid_data.get('hospital_id')

    where       = and_()
    where.append(Item.status==1)

    if hospital_id:
        where.append(Item.hospital_id==hospital_id)

    fields      = ['id', 'hospital_id', 'title', 'price', 'orig_price', 'support_choice_list', 'image', 'has_fee']
    has_more, items   = ItemService.get_paged_items(where=where, fields=fields)

    fetch_min_period_info(items)
    fetch_hospital_refs(items, fields=['id','name'])
    offset      = ''
    if items: offset  = str(items[-1]['id']) + '_' + ''
    print offset, 'offset'
    result      = {
        'code'      : ResponseCode.SUCCESS,
        'msg'       : '',
        'has_more'  : has_more,
        'infos'     : items,
        'offset'    : offset
    }
    return render_template('user/hospital_item_list.html', **result)
    return jsonify_response(result)





order_pay_success_validator  = Inputs(
    {
     'order_id'                 : IdField(msg='订单id')
    }
    )
@wechat_loggin_dec(required=False, validator=order_pay_success_validator)
def order_pay_success():
    ''' 支付成功跳转页面 '''
    order_id            = request.valid_data.get('order_id')
    has_more, infos     = ItemService.get_paged_items(limit=2)
    fetch_hospital_refs(infos)
    fetch_min_period_info(infos)
    context             = {
        'order_id'         : order_id,
        'infos'            : infos
        }
    return render_template('user/order_pay_success.html', **context)



repayment_pay_success_validator  = Inputs(
    {
     'repayment_id'                 : IdField(msg='还款id')
    }
    )
@wechat_loggin_dec(required=False, validator=repayment_pay_success_validator)
def repayment_pay_success():
    ''' 还款成功跳转页面 '''

    return render_template('user/repayment_pay_success.html')



cancel_order_validator  = Inputs(
    {
     'order_id'                 : IdField(msg='订单id')
    }
    )
@wechat_loggin_dec(validator=cancel_order_validator)
def cancel_order():
    ''' 取消订单 '''
    order_id            = request.valid_data.get('order_id')
    order               = OrderService.get_user_order(order_id, request.user_id)
    assert order, '订单不存在'
    where               = Order.status==ORDER_STATUS.PAY_SUCCESS
    count               = OrderService.update_order_status(order_id, ORDER_STATUS.CANCELED, request.user_id, where)
    if count:
        if order.credit_amount:
            repayment_amount    = OrderService.order_repayment_logs_amount(order_id)
            remain_to_repayment = order.credit_amount - repayment_amount
            CreditService.modify_credit(request.user_id, -remain_to_repayment)
            CreditService.cancel_pay_logs(order_id)
        if order.coupon_id:
            CouponService.update_user_coupon_status(UserCoupon.id==order.coupon_id, 0)
    result              = {
        'code'             : ResponseCode.SUCCESS,
        'msg'              : '取消成功'
    }
    return jsonify_response(result)


cancel_pay_validator  = Inputs(
    {
     'order_id'                 : IdField(msg='订单id')
    }
    )
@wechat_loggin_dec(validator=cancel_pay_validator)
def cancel_pay():
    ''' 取消支付 '''
    order_id            = request.valid_data.get('order_id')
    order               = OrderService.get_user_order(order_id, request.user_id)
    assert order, '订单不存在'
    where               = Order.status.in_([ORDER_STATUS.NEW_ORDER, ORDER_STATUS.TO_PAY])
    count               = OrderService.update_order_status(order_id, ORDER_STATUS.CANCEL_BEFORE_PAY, request.user_id, where)
    if count:
        if order.credit_amount:
            CreditService.modify_credit(request.user_id, -(order.credit_amount))
        if order.coupon_id:
            CouponService.update_user_coupon_status(UserCoupon.id==order.coupon_id, 0)
    result              = {
        'code'             : ResponseCode.SUCCESS,
        'msg'              : '取消成功'
    }
    return jsonify_response(result)



finish_order_validator  = Inputs(
    {
     'order_id'                 : IdField(msg='订单id')
    }
    )
@wechat_loggin_dec(validator=finish_order_validator)
def finish_order():
    ''' 用户完成订单 '''
    order_id            = request.valid_data.get('order_id')
    order               = OrderService.get_user_order(order_id, request.user_id)
    assert order, '订单不存在'
    where               = and_(
        Order.id==order_id,
        Order.user_finished==False,
        Order.status.in_([ORDER_STATUS.PAY_SUCCESS, ORDER_STATUS.FINISH])
        )
    count               = OrderService.update_order(where, user_finished=True)
    if count:
        ItemService.incr_item_count(order.item_id)
    result              = {
        'code'             : ResponseCode.SUCCESS,
        'msg'              : '完成订单'
        }
    return jsonify_response(result)



hospital_location_validator  = Inputs(
    {
     'hospital_id'                 : IdField(msg='医院id')
    }
    )
@wechat_loggin_dec(required=False, validator=hospital_location_validator)
def hospital_location():
    hospital_id             = request.valid_data.get('hospital_id')
    hospital                = ItemService.get_hospital_dict_by_id(hospital_id)

    return render_template('user/hospital-location.html', hospital=hospital)


@wechat_loggin_dec(required=False)
def meifenfen_city():
    city_code       = get_cookie('city_code')
    city_name       = get_cookie('city_name')
    city            = None
    if city_code:
        city        = DataService.get_city_by_baidu_city_code(city_code)
    _, citys        = DataService.get_paged_city_list()
    cat             = 1 #1无法定位 2城市未开通 3城市已开通
    if city_code and not city:
        cat         = 2
    elif city:
        cat         = 3
    print city_name, city_code, type(city_name)
    context         = {
        'city'     : city,
        'citys'    :citys,
        'city_name': city_name,
        'city_code': city_code,
        'cat'      : cat 
        }
    if request.args.get('json'):
        response = jsonify_response(context)
    response     = template_response(render_template('user/meifenfen_city.html', **context))
    if city:
        set_cookie(response, 'city_id', str(city.id), 86400*365)
    return response


@wechat_loggin_dec(required=False, need_openid=True)
def meifenfen_index():
    banners         = [
        {'image': 'http://7xnpdb.com2.z0.glb.qiniucdn.com/o_1aco140fa18uljmo17f23cvvu111456800706495.jpg',
         'link':'http://{}/static/user/Activities/home.html'.format(SERVER_NAME),
        },
        {'image': 'http://7xnpdb.com2.z0.glb.qiniucdn.com/o_1a5cd7ihe2aokci1uqdpfk1ivq1banner_01.jpg',
         'link':'http://{}/static/user/banner1.html'.format(SERVER_NAME)},
        {'image': 'http://7xnpdb.com2.z0.glb.qiniucdn.com/o_1a53eou161cs8mku16tm1h91arh1banner_02.jpg',
         'link':'http://{}/static/user/banner2.html'.format(SERVER_NAME)},
        {'image': 'http://7xnpdb.com2.z0.glb.qiniucdn.com/o_1a5cd7ihe2aokci1uqdpfk1ivq1banner_03.jpg',
         'link':'http://{}/user/menu_credit_apply/'.format(SERVER_NAME)},
        ]
    city            = None
    city_name       = get_cookie('choose_city_name') or get_cookie('city_name')
    city_code       = get_cookie('choose_city_code') or get_cookie('city_code')
    if city_code:
        city        = DataService.get_city_by_baidu_city_code(city_code)
    _,  recommend_sub_cats  = ItemService.get_paged_recommend_subcats(_sort='sort_order', _sort_dir='ASC')
    fetch_item_subcat_refs(recommend_sub_cats)

    current_activity        = ActivityService.get_current_activity() or {}
    where                   = ActivityItem.activity_id==current_activity.get('id')
    fields                  = ('id', 'item_id', 'price', 'image')
    _,  activity_items      = ItemService.get_paged_activity_items(fields=fields, where=where, _sort='sort_order', _sort_dir='ASC')
    fields                  = ('id', 'item_id', 'image', 'desc')
    where                   = None
    _,  recommend_items     = ItemService.get_paged_recommend_items(fields=fields, where=where, _sort='sort_order', _sort_dir='ASC')

    img_keys                = [get_img_key(i['image']) for i in recommend_items]
    img_sizes               = DataService.get_imgs_size_by_keys(img_keys)
    img_key_size_map        = {i['key']:{'width':i['width'],'height':i['height']} for i in img_sizes}
    print img_key_size_map
    for rec in recommend_items:
        key                 = get_img_key(rec['image'])
        rec['width']        = img_key_size_map[key]['width']
        rec['height']       = img_key_size_map[key]['height']
    fields                  = ['id', 'hospital_id', 'title', 'price', 'orig_price', 'has_fee', 'support_choice_list']
    fetch_item_refs(chain(activity_items, recommend_items), fields=fields)

    recommend_sub_cats      = [
        {'image': 'http://www.meifenfen.com/static/user/img/home-btn1.png', 'id':5},
        {'image': 'http://www.meifenfen.com/static/user/img/home-btn2.png', 'id':8},
        {'image': 'http://www.meifenfen.com/static/user/img/home-btn3.png', 'id':3},
        ]
    first_activity_item     = None
    if activity_items:
        first_activity_item = activity_items[0]
        first_activity_item['hospital'] = ItemService.get_hospital_dict_by_id(first_activity_item['item']['hospital_id'])
    item_dict_list          = [i['item'] for i in chain(activity_items, recommend_items)]
    item_list               = []
    for i in item_dict_list:
        if i not in item_list:
            item_list.append(i)
    for item in activity_items:
        item['item']['price'] = item['price']
    fetch_min_period_info(item_list)
    context                 = {
        'code'                 : ResponseCode.SUCCESS,
        'msg'                  : '',
        'recommend_sub_cats'   : recommend_sub_cats,
        'activity_items'       : activity_items,
        'recommend_items'      : recommend_items,
        'activity'             : current_activity,
        'banners'              : banners,
        'city_code'            : city_code,
        'city_name'            : city_name,
        'city'                 : city.as_dict() if city else None
        }

    js_sdk_context          = get_jssdk_context()
    if request.args.get('json'):
        return jsonify_response(context)
    return render_template('user/meifenfen.html', **context)



@wechat_loggin_dec(required=False, need_openid=True)
def meifenfen_new_index():
    ''' 新首页 '''
    banners         = [
        {'image': 'http://7xnpdb.com2.z0.glb.qiniucdn.com/o_1aco140fa18uljmo17f23cvvu111456800706495.jpg',
         'link':'http://{}/static/user/Activities/home.html'.format(SERVER_NAME),
        },
        {'image': 'http://7xnpdb.com2.z0.glb.qiniucdn.com/redpack_banner.jpg',
         'link': 'http://www.meifenfen.com/user/redpack_index/'
        },
        {'image': 'http://7xnpdb.com2.z0.glb.qiniucdn.com/o_1a5cd7ihe2aokci1uqdpfk1ivq1banner_01.jpg',
         'link':'http://{}/static/user/banner1.html'.format(SERVER_NAME)},
        {'image': 'http://7xnpdb.com2.z0.glb.qiniucdn.com/o_1a53eou161cs8mku16tm1h91arh1banner_02.jpg',
         'link':'http://{}/static/user/banner2.html'.format(SERVER_NAME)},
        {'image': 'http://7xnpdb.com2.z0.glb.qiniucdn.com/o_1a5cd7ihe2aokci1uqdpfk1ivq1banner_03.jpg',
         'link':'http://{}/user/menu_credit_apply/'.format(SERVER_NAME)},
        ]
    city_id     = get_cookie('city_id')
    city        = DataService.get_city_dict_by_id(city_id)
    _,  recommend_sub_cats  = ItemService.get_paged_recommend_subcats(_sort='sort_order', _sort_dir='ASC')
    fetch_item_subcat_refs(recommend_sub_cats)

    current_activity        = ActivityService.get_current_activity() or {}
    where                   = ActivityItem.activity_id==current_activity.get('id')
    fields                  = ('id', 'item_id', 'price', 'image')
    _,  activity_items      = ItemService.get_paged_activity_items(fields=fields, where=where, _sort='sort_order', _sort_dir='ASC')
    fields                  = ('id', 'item_id', 'image', 'desc')
    where                   = None
    _,  recommend_items     = ItemService.get_paged_recommend_items(fields=fields, where=where, _sort='sort_order', _sort_dir='ASC')

    img_keys                = [get_img_key(i['image']) for i in recommend_items]
    img_sizes               = DataService.get_imgs_size_by_keys(img_keys)
    img_key_size_map        = {i['key']:{'width':i['width'],'height':i['height']} for i in img_sizes}
    print img_key_size_map
    for rec in recommend_items:
        key                 = get_img_key(rec['image'])
        rec['width']        = img_key_size_map[key]['width']
        rec['height']       = img_key_size_map[key]['height']
    fields                  = ['id', 'hospital_id', 'title', 'price', 'orig_price', 'has_fee', 'support_choice_list']
    fetch_item_refs(chain(activity_items, recommend_items), fields=fields)

    recommend_sub_cats      = [
        {'image': 'http://www.meifenfen.com/static/user/img/home-btn1.png', 'id':5},
        {'image': 'http://www.meifenfen.com/static/user/img/home-btn2.png', 'id':8},
        {'image': 'http://www.meifenfen.com/static/user/img/home-btn3.png', 'id':3},
        ]
    first_activity_item     = None
    if activity_items:
        first_activity_item = activity_items[0]
        first_activity_item['hospital'] = ItemService.get_hospital_dict_by_id(first_activity_item['item']['hospital_id'])
    item_dict_list          = [i['item'] for i in chain(activity_items, recommend_items)]
    item_list               = []
    for i in item_dict_list:
        if i not in item_list:
            item_list.append(i)
    for item in activity_items:
        item['item']['price'] = item['price']

    fetch_min_period_info(item_list)

    where                   = BeautyEntry.status==1
    _, tutorials            = TutorialService.get_paged_tutorial_entries(where=where)
    tutorials               = tutorials[:2]
    tutorial_tags           = ['原理', '手法', '案例', '大人说']
    _sort_dir               = 'ASC'
    _sort                   = 'sort_order'
    _, recommend_hospitals  = ItemService.get_paged_recommend_hospitals(_sort_dir=_sort_dir, _sort=_sort)
    fetch_hospital_refs(recommend_hospitals)
    recommend_hospitals     = recommend_hospitals[:3]
    for tutorial in tutorials:
        tutorial['create_time'] = get_time_str_from_dt(tutorial['create_time'], '%-m.%-d')
    context                 = {
        'code'                 : ResponseCode.SUCCESS,
        'msg'                  : '',
        'tutorials'            : tutorials,
        'recommend_sub_cats'   : recommend_sub_cats,
        'activity_items'       : activity_items,
        'recommend_items'      : recommend_items,
        'activity'             : current_activity,
        'banners'              : banners,
        'tutorial_tags'        : tutorial_tags,
        'recommend_hospitals'  : recommend_hospitals,
        'city'                 : city
        }

    js_sdk_context          = get_jssdk_context()
    if request.args.get('json'):
        return jsonify_response(context)
    return render_template('user/meifenfen_new.html', **context)




@wechat_loggin_dec(required=False, need_openid=False)
def api_doc():
    ''' 接口文档 '''
    return send_from_directory('static', 'doc.html')



mei_tutorials_validator  = Inputs(
    {
     'cat'        : Optional(IntChoiceField(choices=[1,2,3], msg='攻略类型')), #1最新 2最早 3最热
     'offset'     : Optional(TextField(min_length=0, max_length=1000, msg='分页参数'))
    }
    )
@wechat_loggin_dec(required=False, validator=mei_tutorials_validator)
def mei_tutorials():
    ''' 美攻略 '''
    cat         = request.valid_data.get('cat')
    offset      = request.valid_data.get('offset')

    offset_id   = None
    _sort       = 'id'
    _sort_dir   = 'DESC'
    filters     = [BeautyEntry.status==1]
    if cat==1:
        if offset: filters.append(BeautyEntry.id<offset)
    if cat==2:
        _sort_dir = 'ASC'
        if offset: filters.append(BeautyEntry.id>offset)
    elif cat==3:
        _sort   = 'view_count'
        _sort_dir = 'DESC'
        if offset and len((offset or '').split('_')):
            view_count, offset_id = offset.split('_')
            where   = or_(
                and_(
                    BeautyEntry.view_count==view_count,
                    BeautyEntry.id<offset_id
                ),
                and_(
                    BeautyEntry.view_count<view_count,
                )
            )
            filters.append(where)
    where       = and_(*filters)
    has_more, infos     = TutorialService.get_paged_tutorial_entries(
        where=where,
        _sort=_sort, _sort_dir=_sort_dir)
    offset      = ''
    if infos:
        if cat!=3:
            offset  = str(infos[-1][_sort])
        else:
            offset  = '{}_{}'.format(infos[-1]['view_count'], infos[-1]['id'])
    for info in infos:
        info['create_time'] = get_time_str_from_dt(info['create_time'], '%-m-%-d')
    result      = {
        'code'     : ResponseCode.SUCCESS,
        'msg'      : '',
        'has_more' : has_more,
        'cat'      : cat,
        'infos'    : infos,
        'offset'   : offset
        }
    return jsonify_response(result)



tutorial_detail_validator  = Inputs(
    {
     'tutorial_id': IdField(msg='攻略id')
    }
    )
@wechat_loggin_dec(required=False, validator=tutorial_detail_validator)
def tutorial_detail():
    ''' 美攻略 '''
    tutorial_id = request.valid_data.get('tutorial_id')

    tutorial    = TutorialService.get_tutorial(tutorial_id)
    assert tutorial, '美攻略不存在'
    item_ids    = tutorial['item_id_list']
    items       = ItemService.get_items_by_ids(item_ids)
    fetch_min_period_info(items)
    fetch_hospital_refs(items, fields=['id','name'])
    TutorialService.incr_tutorial_view_count(tutorial_id)
    result      = {
        'code'     : ResponseCode.SUCCESS,
        'msg'      : '',
        'tutorial' : tutorial,
        'infos'    : items,
        }
    return jsonify_response(result)



daily_coupons_validator  = Inputs(
    {
     'offset'     : Optional(TextField(min_length=0, max_length=1000, msg='分页参数'))
    }
    )
@wechat_loggin_dec(required=False, validator=daily_coupons_validator)
def daily_coupons():
    ''' 每日优惠券 '''
    offset      = request.valid_data.get('offset')
    now         = dt_obj.now()
    where       = and_(
        DailyCoupon.start_time<now,
        DailyCoupon.end_time>now
        )
    limit       = 1000
    _sort       = 'start_time'
    _sort_dir   = 'DESC'
    has_more, coupons     = TutorialService.get_paged_daily_coupons(
        limit=1000, where=where, offset=offset, _sort=_sort, _sort_dir=_sort_dir
        )
    from collections import defaultdict
    datas       = defaultdict(list)

    fetch_coupon_refs(coupons)
    set_coupon_use_time(coupons)
    for coupon in coupons:
        coupon['create_time_str'] = format_dt(coupon['start_time'])
    for coupon in coupons:
        datas[coupon['create_time_str']].append(coupon)
    daily_ids   = [i['id'] for i in coupons]
    daily_received_map = TutorialService.get_user_daily_by_ids(request.user_id, daily_ids)
    for i in coupons:
        i['has_received'] = bool(daily_received_map.get(i['id']))

    offset      = ''
    if coupons:
        offset  = str(coupons[-1][_sort])

    infos_by_day = []
    for k,v in datas.items():
        tmp     = {
            'title': k,
            'infos': v,
            #'note': '每日10点，惊喜不断!'
            }
        if tmp['infos'][0]['title']:
            tmp['note'] = tmp['infos'][0]['title']
        else:
            tmp['note'] = ''
        infos_by_day.append(tmp)
    result      = {
        'code'     : ResponseCode.SUCCESS,
        'msg'      : '',
        'infos'    : infos_by_day,
        'has_more' : has_more,
        'offset'   : offset        
        }

    return jsonify_response(result)



receive_coupon_validator  = Inputs(
    {
     'daily_id'     : IdField(msg='请选择活动')
    }
    )
@wechat_loggin_dec(required=True, validator=receive_coupon_validator)
def receive_coupon():
    ''' 领取每日优惠券 '''
    daily_id    = request.valid_data.get('daily_id')

    daily       = TutorialService.get_user_daily(request.user_id, daily_id)

    assert not daily, '您已领取过'

    daily_coupon = TutorialService.get_daily_coupon(daily_id)
    assert daily_coupon, '活动不存在'
    assert daily_coupon['total']>daily_coupon['sent'], '已领取完'

    count       = TutorialService.incr_daily_coupon_received(daily_id)
    assert count, '领取完了'

    count       = TutorialService.send_daily_coupon(request.user_id, daily_id)
    if count:
        CouponService.send_user_coupon(request.user_id, daily_coupon['coupon_id'])
    daily_coupon = TutorialService.get_daily_coupon(daily_id)
    result      = {
        'code'     : ResponseCode.SUCCESS,
        'msg'      : '领取成功',
        'count'    : daily_coupon['remain']
        }

    return jsonify_response(result)


resend_user_coupon_validator  = Inputs(
    {
     'user_coupon_ids'   : TextField(min_length=1, max_length=100, msg='逗号分隔的优惠券id字符串'),
     'phone'             : MobileField(msg='用户手机号'),
    }
    )
@wechat_loggin_dec(required=True, validator=resend_user_coupon_validator, app=True)
def resend_user_coupon():
    phone           = request.valid_data.get('phone')
    user_coupon_ids = request.valid_data.get('user_coupon_ids')
    user_coupon_ids = str_to_int_list(user_coupon_ids)
    user           = UserService.get_user_by_phone(phone)
    assert user, '手机号对应用户不存在'
    assert user.id!=request.user_id, '不能转赠给自己'

    for user_coupon_id in user_coupon_ids:
        CouponService.resend_user_coupon(request.user_id, user.id, user_coupon_id)

    result          = {
        'code' : ResponseCode.SUCCESS,
        'msg'  : '转赠成功'
    }
    return jsonify_response(result)




@wechat_loggin_dec(required=False)
def set_open_id():
    result = {}
    response= jsonify_response(result, with_response=True)
    set_cookie(response, 'open_id', 'o56qvw-ThtwfthGGlZ-XbH-3fjRc', 86400*30)
    return response


@wechat_loggin_dec(required=False, need_openid=True)
def login_link():
    print 'login'
    return send_from_directory('static', 'user/login.html')


@wechat_loggin_dec(required=False, need_openid=True)
def wechat_room_link():
    print 'wechat_room_link'
    return send_from_directory('static', 'user/Activities/home.html')



