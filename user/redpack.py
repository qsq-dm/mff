# -*- coding: utf-8 -*-
import os
from flask import request
from flask import redirect
from flask import render_template

from sqlalchemy      import and_
from sqlalchemy      import or_
from models          import db
from models          import RedpackQuestion
from models          import RedpackUserQuestion
from models          import RedpackPay
from models          import RedpackPayUser

from util.utils      import jsonify_response
from util.utils      import random_str
from util.utils      import str_to_int_list
from util.utils      import random_redpack_price
from util.utils      import keep_fields_from_list
from util.utils      import random_redpack_price
from util.decorators import wechat_loggin_dec
from util.validators import Optional
from util.validators import Inputs
from util.validators import MobileField
from util.validators import TextField
from util.validators import IdField
from util.validators import FloatField
from util.validators import IntChoiceField
from util.sign       import sign_user
from util.sign       import set_cookie
from util.sign       import del_cookie
from ops.bulks       import fetch_user_refs
from ops.bulks       import fetch_qrcodeuser_refs
from ops.log         import LogService
from ops.order       import OrderService
from ops.redpack     import RedpackService
from ops.promote     import PromoteService

from thirdparty.wechat      import exchange_code_for_token
from thirdparty.wx_pay      import Notify_pub
from thirdparty.wx_pay      import get_redpack_pay_params
from constants       import REDPACK_PAY_STATUS
from constants       import PAY_METHOD
from constants       import ResponseCode
from ops.tasks       import send_redpack_after_pay
from settings        import DEFAULT_IMAGE


@wechat_loggin_dec(required=False, need_openid=True, validator=None)
def redpack_index():
    ''' '''
    user                = RedpackService.get_qruser_by_openid(request.open_id)
    has_followed        = False
    avatar              = ''
    question_count      = 0
    if user:
        has_followed = True if user.nickname else False
        avatar       = user.headimgurl
        question_count  = RedpackService.count_user_question(user.id)
        if not has_followed: PromoteService.set_user_sex.delay(request.open_id)
    else:
        qrcode_id    = None
        open_id      = request.open_id
        PromoteService.log_qr_user(qrcode_id, open_id, -1)
        PromoteService.set_user_sex.delay(open_id)
    need_login      = question_count>=5 and not request.user_id

    result          = {
        'code'          : ResponseCode.SUCCESS,
        'msg'           : '',
        'has_followed'  : has_followed,
        'question_count': question_count,
        'avatar'        : avatar or DEFAULT_IMAGE,
        'need_login'    : need_login
        }
    return render_template('user/redpack_index.html', **result)


def new_question():
    ''' '''
    return render_template('user/create_question.html')


def question_list():
    ''' '''
    where               = RedpackQuestion.status==1
    fields              = ['id', 'content']
    has_more, infos     = RedpackService.get_paged_redpack_questions(where=where, limit=50, fields=fields)

    result              = {
        'code'        : ResponseCode.SUCCESS,
        'msg'         : '',
        'infos'       : infos
        }
    return jsonify_response(result)


new_question_post_validator = Inputs(
    {
     'question_id'    : Optional(IdField(msg='请选择问题')),
     'question'       : TextField(min_length=1, max_length=100, msg='请输入问题内容'),
     'answer'         : TextField(min_length=1, max_length=100, msg='请输入答案内容'),
     'is_random'      : IntChoiceField(choices=[0,1], msg='是否随机奖励'),
     'is_custom'      : IntChoiceField(choices=[0,1], msg='是否自定义问题'),
     'price'          : Optional(FloatField(msg='请输入红包金额')),
    }
)
@wechat_loggin_dec(required=False, need_openid=True, validator=new_question_post_validator)
def new_question_post():
    ''' 创建收红包问答 '''
    question_id         = request.valid_data.get('question_id') or None
    question            = request.valid_data.get('question')
    answer              = request.valid_data.get('answer')
    is_random           = request.valid_data.get('is_random')
    is_custom           = request.valid_data.get('is_custom')
    price               = request.valid_data.get('price') or None
    question            = (question or '').replace('xianpeng', '王前发')
    question            = (question or '').replace('显鹏', '王前发')
    if not is_random: assert price and 1<=price<=200, '请输入红包金额，范围在1~200'
    else: price = random_redpack_price()

    if not is_custom: assert question, '请输入问题内容'

    user                = RedpackService.get_qruser_by_openid(request.open_id)

    assert user and user.nickname, '请先关注我们的微信'

    if RedpackService.count_user_question(user.id)>5: assert request.user_id, '想收取更多红包，请先注册成我们的用户吧'
    question_id         = RedpackService.create_user_question(user.id, question_id, question, answer, is_custom, is_random, price)

    result      = {
        'code'          : ResponseCode.SUCCESS,
        'user_question_id'   : question_id,
        'msg'           : '创建成功'
        }
    return jsonify_response(result)



my_questions_validator = Inputs(
    {
     'offset'       : Optional(TextField(min_length=0, max_length=100, msg='请输入问题内容')),
    }
)
@wechat_loggin_dec(required=False, need_openid=True, validator=my_questions_validator)
def my_questions():
    ''' 我的收红包纪录列表 '''
    offset              = request.valid_data.get('offset')
    user                = RedpackService.get_qruser_by_openid(request.open_id)
    assert user and user.nickname, '请先关注我们的微信'

    where               = RedpackUserQuestion.qr_user_id==user.id
    has_more, questions = RedpackService.get_paged_user_question(where=where, offset=offset)

    all_viewers         = []
    for question in questions:
        latest_viewers      = []
        if question['view_count']:
            where              = RedpackPayUser.user_question_id==question['id']
            _, latest_viewers  = RedpackService.get_question_viewers(where=where, limit=2)
        question['latest_viewers'] = latest_viewers
        all_viewers.extend(latest_viewers)
        if question['question_id']:
            mff_question        = RedpackService.get_question_by_id(question['question_id'])
            question['question']= mff_question['content']
    fetch_qrcodeuser_refs(all_viewers, fields=['id', 'nickname', 'headimgurl'])
    for i in all_viewers:
        i['qr_user']['nickname']       = i['qr_user'].get('nickname') or '好友'

    offset              = ''
    if questions:
        offset          = str(questions[-1]['id'])
    result              = {
        'code'          : ResponseCode.SUCCESS,
        'msg'           : '',
        'infos'         : questions,
        'has_more'      : has_more,
        'offset'        : offset
        }
    return jsonify_response(result)


question_detail_validator = Inputs(
    {
     'user_question_id'       : IdField(msg='问题id'),
    }
)
@wechat_loggin_dec(required=False, need_openid=True, validator=question_detail_validator, app=True)
def question_detail():
    ''' 问题详情 '''
    user_question_id    = request.valid_data.get('user_question_id')
    user                = RedpackService.get_qruser_by_openid(request.open_id)

    has_viewed          = RedpackService.get_user_question_viewer(user_question_id, user.id) if user else False
    question            = RedpackService.get_user_question_by_id(user_question_id)
    assert question, '问题不存在'
    creator             = PromoteService.get_qrcodeuser_by_id(question['qr_user_id'])
    if question['question_id']:
        mff_question        = RedpackService.get_question_by_id(question['question_id'])
        question['question']= mff_question['content']
    where                   = RedpackPayUser.user_question_id==user_question_id
    has_more, infos         = RedpackService.get_question_viewers(where=where)
    fetch_qrcodeuser_refs(infos, fields=['id', 'nickname', 'headimgurl'])
    for i in infos:
        i['qr_user']['nickname']       = i['qr_user']['nickname'] or '好友'
    is_myself           = question['qr_user_id']==user.id if user else False
    result              = {
        'code'         : ResponseCode.SUCCESS,
        'msg'          : '',
        'is_myself'    : is_myself,
        'infos'        : infos,
        'creator'      : creator,
        'has_viewed'   : has_viewed,
        'question'     : question
        }
    return render_template('user/redpack_detail.html', **result)
    return jsonify_response(result)


redpack_pay_validator = Inputs(
    {
     'user_question_id'       : IdField(msg='问题id'),
    }
)
@wechat_loggin_dec(required=False, need_openid=True, validator=redpack_pay_validator, app=True)
def redpack_pay():
    ''' 问题详情 '''
    user                = RedpackService.get_qruser_by_openid(request.open_id)
    if not user:
        if request.open_id:
            PromoteService.log_qr_user(None, request.open_id, -1)
            user        = RedpackService.get_qruser_by_openid(request.open_id)
        else:
            assert False, '请先关注我们的微信公众号美分分'
    user_question_id    = request.valid_data.get('user_question_id')
    question            = RedpackService.get_user_question_by_id(user_question_id)
    assert question, '问题不存在'
    has_viewed          = RedpackService.get_user_question_viewer(user_question_id, user.id) if user else False
    assert not has_viewed, '您已查看过此问题'
    if question['is_random']: question['price'] = random_redpack_price()
    order_no            = OrderService.create_no()
    RedpackService.add_pay(user.id, user_question_id, order_no, question['price'])
    wx_pay_params, err  = get_redpack_pay_params(request.open_id, question['price'], order_no);
    result              = {
        'code'         : ResponseCode.SUCCESS,
        'msg'          : '',
        'question'     : question,
        'params'       : wx_pay_params
        }
    return jsonify_response(result)


question_viewers_validator = Inputs(
    {
     'user_question_id'       : IdField(msg='问题id'),
     'offset'       : Optional(TextField(min_length=0, max_length=100, msg='请输入问题内容')),
    }
)
@wechat_loggin_dec(required=False, need_openid=True, validator=question_viewers_validator, app=True)
def question_viewers():
    ''' 问题红包查看人列表 '''
    user_question_id        = request.valid_data.get('user_question_id')
    offset                  = request.valid_data.get('offset')
    where                   = RedpackPayUser.user_question_id==user_question_id
    has_more, infos         = RedpackService.get_question_viewers(where=where, offset=offset)

    offset                  = ''
    if infos:
        offset              = str(infos[-1]['id'])
    fetch_qrcodeuser_refs(infos, fields=['id', 'nickname', 'headimgurl'])
    for i in infos:
        i['qr_user']['nickname']       = i['qr_user']['nickname'] or '好友'
    result                  = {
        'code'           : ResponseCode.SUCCESS,
        'msg'            : '',
        'has_more'       : has_more,
        'infos'          : infos,
        'offset'         : offset
        }
    return jsonify_response(result)




def wx_redpack_callback():
    ''' 微信红包支付回调 '''
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

    pay             = RedpackService.get_pay_by_orderno(order_no)
    if not pay:
        re['return_code']   = 'FAIL'
        re['return_msg']    = '订单不存在:'+order_no
        return notify.arrayToXml(re)

    total_price     = float(total_fee)/100
    order_price     = float(pay.price)
    if order_price != total_price and (os.environ.get('APP_ENV')=='production'):
        print order_price, total_price, '金额不匹配'
        re['return_code']   = 'FAIL'
        re['return_msg']    = '金额不匹配'
        return notify.arrayToXml(re)

    msg             = ''
    if (pay.status==REDPACK_PAY_STATUS.PAY_SUCCESS):
        re                  = {'return_code':'SUCCESS','return_msg':'ok'}
        return notify.arrayToXml(re)
    if result_code.upper()  == 'FAIL':
        re['return_code']   = 'FAIL'
        redpack_error_action(pay)
    elif result_code.upper()=='SUCCESS':
        re['return_code']   = 'SUCCESS'
        redpack_success_action(pay, transaction_id=transaction_id)
    else:
        print 'wxpay_notify:',result_code
        re['return_code']   = 'SUCCESS'
        msg                 = '未知返回码'

    re['return_msg']        = msg
    return notify.arrayToXml(re)


def redpack_error_action(pay):
    pass


def redpack_success_action(pay, **kw):
    where           = and_(
        RedpackPay.id==pay.id,
        RedpackPay.status.in_([REDPACK_PAY_STATUS.TO_PAY, REDPACK_PAY_STATUS.NEW]),
        )
    kw['status']    = REDPACK_PAY_STATUS.PAY_SUCCESS
    count           = RedpackService.update_redpack_pay(where, **kw)
    print 'redpack pay success'
    if count:
        RedpackService.add_redpack_user(pay.id, pay.qr_user_id, pay.user_question_id, pay.price)
        RedpackService.incr_question_view_count(pay.user_question_id)
        user_question = RedpackService.get_user_question_by_id(pay.user_question_id)
        creator_id    = user_question['qr_user_id']
        user          = PromoteService.get_qrcodeuser_by_id(pay.qr_user_id)
        creator       = PromoteService.get_qrcodeuser_by_id(creator_id)
        RedpackService.incr_user_question_money(pay.user_question_id, pay.price)
        send_redpack_after_pay.delay(creator.open_id, pay.price, user.nickname or '')

















