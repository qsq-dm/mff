# -*- coding: utf-8 -*-

from flask      import request
from sqlalchemy import and_
from sqlalchemy import or_
from models     import *
from models     import Order
from ops.order  import OrderService
from ops.trial  import TrialService
from util.utils import dt_obj
from util.utils import date_to_datetime
from util.utils import delta_time_str
from util.utils import jsonify_response
from util.decorators    import wechat_loggin_dec
from util.validators    import Inputs
from util.validators    import Optional
from util.validators    import IdField
from util.validators    import TextField
from util.validators    import MobileField
from util.validators    import IntChoiceField
from ops.bulks          import fetch_user_refs
from ops.coupon         import CouponService
from constants import ResponseCode



def set_trial_apply_status(apply, comment=None, order=None):
    ''' 0等待审核 1获得了试用，写试用体会 2获得了试用，去下单 3写试用体会 4查看试用体会 5未获得资格 '''
    if apply['status']==1 and apply['cat']==1:
        apply['status'] = 2
    if apply['status']==1 and comment:
        apply['status'] = 4
    if apply['status']==2 and order:
        apply['status']==3
    if apply['status']==3 and comment:
        apply['status'] = 4
    if apply['status']==0 and apply['trial']['total']==apply['trial']['sent']:
        apply['status'] = 5


trial_list_validator  = Inputs(
    {
     'cat'                  : IntChoiceField(choices=[1,2], msg='试用分类'),
     'offset'               : Optional(TextField(min_length=0, max_length=10000, msg='分页参数')),
    }
    )
@wechat_loggin_dec(required=False, validator=trial_list_validator, app=True)
def trial_list():
    ''' 试用列表 '''
    offset              = request.valid_data.get('offset')
    cat                 = request.valid_data.get('cat') #1当期试用 2往期试用

    _sort_dir           = 'ASC'
    _sort               = 'sort_order'
    if cat==1:
        where           = and_(
            Trial.end_time>dt_obj.now(),
            Trial.start_time<dt_obj.now()
            )
    else:
        _sort_dir       = 'DESC'
        _sort           = 'end_time'
        where           = Trial.end_time<=dt_obj.now()
    fields              = ['id', 'sort_order', 'cat_str', 'title', 'total', 'apply_count', 'end_time', 'image']

    has_more, infos     = TrialService.get_paged_trials(
            _sort_dir=_sort_dir, _sort=_sort, where=where, offset=offset, fields=fields)
    for info in infos:
        end_time              = date_to_datetime(str(info['end_time']), format='%Y-%m-%d %H:%M:%S')
        info['end_time_str']  = delta_time_str(end_time)

    offset              = ''
    if infos:
        offset          = str(infos[-1]['sort_order'])
    if cat==2 and infos:
        offset          = str(infos[-1]['end_time'])
    result              = {
        'code'          : ResponseCode.SUCCESS,
        'msg'           : '',
        'infos'         : infos,
        'offset'        : offset,
        'has_more'      : has_more
        }
    return jsonify_response(result)



my_trial_list_validator  = Inputs(
    {
     'offset'               : Optional(TextField(min_length=0, max_length=10000, msg='分页参数')),
    }
    )
@wechat_loggin_dec(validator=my_trial_list_validator)
def my_trial_list():
    ''' 我的试用 '''
    offset              = request.valid_data.get('offset')
    where               = TrialApply.user_id==request.user_id
    fields              = ['id', 'cat', 'coupon_id', 'trial_id', 'status', 'create_time']
    has_more, infos     = TrialService.get_paged_apply_user_list(where=where, fields=fields, offset=offset)
    trial_ids           = [ i['trial_id'] for i in infos ]
    user_coupon_ids     = [i['coupon_id'] for i in infos if i['coupon_id']]
    where               = Trial.id.in_(trial_ids)
    fields              = ['id', 'cat_str', 'title', 'total', 'apply_count', 'end_time', 'image', 'sent']
    _, trials           = TrialService.get_paged_trials(where=where, fields=fields)

    where               = and_(
        TrialComment.trial_id.in_(trial_ids),
        TrialComment.user_id==request.user_id
        )
    _, comments         = TrialService.get_paged_trial_comments(where=where)
    trial_comment_map   = {i['trial_id']:i['id'] for i in comments}
    trials_map          = {i['id']:i for i in trials}
    where               = Order.coupon_id.in_(user_coupon_ids)
    _, orders           = OrderService.get_paged_orders(where=where)
    coupon_order_map    = {i['coupon_id']:1 for i in orders}
    where               = UserCoupon.id.in_(user_coupon_ids)
    _, user_coupons     = CouponService.get_paged_user_coupons(where=where)
    coupon_item_map     = {i['id']:i['item_id'] for i in user_coupons}
    for info in infos:
        info['trial']   = trials_map[info['trial_id']]
    for info in infos:
        coupon_id       = info['coupon_id']
        order           = coupon_order_map.get('coupon_id')
        item_id         = coupon_item_map.get(coupon_id)
        info['item_id'] = item_id
        set_trial_apply_status(
            info, comment=trial_comment_map.get(info['trial']['id']), order=order)

    offset              = ''
    if infos:
        offset          = str(infos[-1]['id'])
    result              = {
        'code'          : ResponseCode.SUCCESS,
        'msg'           : '',
        'infos'         : infos,
        'has_more'      : has_more,
        'offset'        : offset
        }
    return jsonify_response(result)



comment_trial_validator  = Inputs(
    {
     'trial_id'             : IdField(msg='试用id'),
     'content'              : TextField(min_length=0, max_length=10000, msg='试用体会'),
     'photos'               : Optional(TextField(min_length=0, max_length=10000, msg='图片')),
    }
    )
@wechat_loggin_dec(validator=comment_trial_validator)
def comment_trial():
    ''' 试用体会 '''
    trial_id        = request.valid_data.get('trial_id')
    content         = request.valid_data.get('content')
    photos          = request.valid_data.get('photos')
    trial           = TrialService.get_trial(trial_id)
    assert trial, '试用商品不存在'
    apply           = TrialService.get_user_apply(request.user_id, trial_id)
    assert apply, '请先提交申请'
    assert apply['status']==1, '您未获得试用资格'
    comment_id      = TrialService.comment(trial_id, request.user_id, content, photos)

    result          = {
        'code'         : ResponseCode.SUCCESS,
        'msg'          : '发表成功'
    }
    return jsonify_response(result)


apply_trial_validator  = Inputs(
    {
     'trial_id'             : IdField(msg='试用id'),
     'sex'                  : IntChoiceField(choices=[1,2], msg='性别'),
     'name'                 : TextField(min_length=0, max_length=10000, msg='申请人名字'),
     'phone'                : MobileField(msg='申请人手机号'),
     'content'              : TextField(min_length=0, max_length=10000, msg='申请理由'),
     'addr'                 : TextField(min_length=0, max_length=10000, msg='宿舍地址'),
     'school'               : TextField(min_length=0, max_length=10000, msg='学校'),
    }
    )
@wechat_loggin_dec(required=True, validator=apply_trial_validator)
def apply_trial():
    ''' 申请试用 '''
    trial_id    = request.valid_data.get('trial_id')
    sex         = request.valid_data.get('sex')
    name        = request.valid_data.get('name')
    phone       = request.valid_data.get('phone')
    content     = request.valid_data.get('content')
    addr        = request.valid_data.get('addr')
    school      = request.valid_data.get('school')

    trial       = TrialService.get_trial(trial_id)
    assert trial, '试用不存在'
    assert trial['end_time']>dt_obj.now(), '试用已结束'
    apply_id    = TrialService.add_apply(
        request.user_id, name, phone, school, trial_id, content, sex, addr)
    TrialService.incr_trial_apply_count(trial_id)
    result      = {
        'code'      : ResponseCode.SUCCESS,
        'msg'       : '申请成功'
        }
    return jsonify_response(result)


trial_comment_list_validator  = Inputs(
    {
     'trial_id'             : IdField(msg='试用id'),
     'offset'               : Optional(TextField(min_length=0, max_length=10000, msg='分页参数'))
    }
    )
@wechat_loggin_dec(required=False, validator=trial_comment_list_validator)
def trial_comment_list():
    ''' 试用评论列表 '''
    trial_id        = request.valid_data.get('trial_id')
    offset          = request.valid_data.get('offset')
    where           = TrialComment.trial_id==trial_id
    has_more, infos = TrialService.get_paged_trial_comments(where=where, offset=offset)
    user_ids        = [i['user_id'] for i in infos]
    fetch_user_refs(infos, fields=['id', 'name', 'avatar'])

    apply_list      = TrialService.get_trial_applies_by_user_ids(trial_id, user_ids)
    user_school_map = {i['user_id']:i['school'] for i in apply_list}
    for info in infos:
        info['school'] = user_school_map[info['user']['id']]
    offset          = ''
    if infos:
        offset      = infos[-1]['id']
    result          = {
        'code'          : ResponseCode.SUCCESS,
        'msg'           : '',
        'infos'         : infos,
        'offset'        : offset
        }
    return jsonify_response(result)


trial_applyers_validator  = Inputs(
    {
     'trial_id'             : IdField(msg='试用id'),
     'offset'               : Optional(TextField(min_length=0, max_length=10000, msg='分页参数'))
    }
    )
@wechat_loggin_dec(required=False, validator=trial_applyers_validator)
def trial_applyers():
    ''' 试用申请者 '''
    trial_id        = request.valid_data.get('trial_id')
    offset          = request.valid_data.get('offset')
    status          = None
    info_id         = None
    length          = len((offset or '').split('_'))
    if offset and length==2:
        print offset, length
        status, info_id     = offset.split('_')
        status              = int(status)
        info_id             = int(info_id)
        where               = or_()
        where.append(
            and_(
                TrialApply.status==status,
                TrialApply.id<info_id
            )
            )
        if status==1:
            where.append(
                TrialApply.status==0
            )
        where       = and_(
            where,
            TrialApply.trial_id==trial_id
            )
    else:
        where           = TrialApply.trial_id==trial_id
    fields          = ['id', 'school', 'status', 'user_id', 'create_time']
    order_by        = TrialApply.status.desc(), TrialApply.id.desc()
    has_more, infos = TrialService.get_paged_apply_user_list(
        order_by=order_by, where=where, fields=fields
        )
    fetch_user_refs(infos, fields=['id', 'name', 'avatar'])
    offset          = ''
    if infos:
        status      = str(infos[-1]['status'])
        info_id     = str(infos[-1]['id'])
        offset      = '{}_{}'.format(status, info_id)
    result          = {
        'code'         : ResponseCode.SUCCESS,
        'msg'          : '',
        'infos'        : infos,
        'has_more'     : has_more,
        'offset'       : offset
    }
    return jsonify_response(result)


trial_detail_validator  = Inputs(
    {
    'trial_id'    : IdField(msg='试用id'),
    })
@wechat_loggin_dec(required=False, validator=trial_detail_validator)
def get_trial_detail():
    ''' '''
    trial_id        = request.valid_data.get('trial_id')
    trial           = TrialService.get_trial(trial_id)

    apply           = TrialService.get_trial_apply(request.user_id, trial_id)

    status          = -1 #未申请
    item_id         = 0
    if apply:
        comment     = TrialService.get_trial_comment(trial_id, request.user_id)
        order       = OrderService.get_order_by_coupon_id(apply['coupon_id'])
        where       = Trial.id==apply['trial_id']
        _, trials   = TrialService.get_paged_trials(where=where, fields=None)
        apply['trial']  = trials[0]
        set_trial_apply_status(apply, comment, order)
        status      = apply['status']
        coupon      = CouponService.get_user_coupon_by_id(apply['coupon_id']) if apply['coupon_id'] else None
        if coupon: item_id = coupon['item_id']
    elif trial['end_time']<dt_obj.now():
        status      = 6 #已结束

    result          = {
        'trial'         : trial,
        'item_id'       : item_id,
        'status'        : status,
        'apply'         : apply,
        'code'          : ResponseCode.SUCCESS,
        'msg'           : ''
    }

    return jsonify_response(result)


@wechat_loggin_dec()
def get_history_apply():
    ''' 获取最近一次填写的数据 '''
    apply   = TrialService.get_latest_apply(request.user_id)
    result  = {
        'code': ResponseCode.SUCCESS,
        'msg' : '',
        'data': apply or {}
        }
    return jsonify_response(result)








