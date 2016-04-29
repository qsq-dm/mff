# -*- coding: utf-8 -*-
import datetime

from flask import request
from flask import redirect
from flask import render_template

from sqlalchemy      import and_
from models          import ItemComment 
from util.utils      import jsonify_response
from util.utils      import random_str
from util.decorators import wechat_loggin_dec
from util.validators import Optional
from util.validators import Inputs
from util.validators import MobileField
from util.validators import TextField
from util.validators import IdField
from util.sign       import sign_user
from util.sign       import set_cookie
from util.sign       import del_cookie
from ops.bulks       import fetch_user_refs
from ops.item        import ItemService
from ops.user        import UserService
from ops.promote     import PromoteService
from ops.log         import LogService
from ops.cache       import SmsCache
from ops.cache       import InvalidUserPasswdCache
from ops.cache       import InvalidUserSignupVcodeCache
from ops.cache       import InvalidUserResetVcodeCache
from ops.comment     import CommentService
from constants       import ResponseCode
from thirdparty.sms  import send_sms
from thirdparty.sms  import gen_vcode
from thirdparty.wechat      import exchange_code_for_token
from settings               import MAX_TODAY_PASSWD_ATTEMPT
from settings               import MAX_TODAY_VCODE_ATTEMPT
from settings               import CONTACT


get_vcode_validator  = Inputs(
    {
     'phone'    : MobileField(msg='请输入手机号'),
    }
)
@wechat_loggin_dec(required=False, validator=get_vcode_validator, app=True)
def get_vcode():
    ''' 获取验证码 '''
    phone       = request.valid_data.get('phone')
    vcode       = gen_vcode()
    user        = UserService.get_user_by_phone(phone)
    assert user, '手机号不存在'

    send_sms.delay(phone, vcode)

    SmsCache.set_vcode(phone, vcode)
    result      = {
        'code'      : ResponseCode.SUCCESS,
        'msg'       : '发送成功'
    }
    return jsonify_response(result)



get_reg_vcode_validator  = Inputs(
    {
     'phone'    : MobileField(msg='请输入手机号'),
    }
)
@wechat_loggin_dec(required=False, validator=get_reg_vcode_validator, app=True)
def get_reg_vcode():
    ''' 获取注册验证码 '''
    phone       = request.valid_data.get('phone')
    user        = UserService.get_user_by_phone(phone)
    assert not user, '手机号码已存在'
    vcode       = gen_vcode()
    send_sms.delay(phone, vcode)

    SmsCache.set_vcode(phone, vcode)
    result      = {
        'code'      : ResponseCode.SUCCESS,
        'msg'       : '发送成功'
    }
    return jsonify_response(result)


reset_passwd_validator  = Inputs(
    {
     'phone'    : MobileField(msg='请输入手机号'),
     'passwd'   : TextField(msg='请输入密码'),
     'vcode'    : TextField(msg='请输入验证码'),
    }
)
@wechat_loggin_dec(required=False, validator=reset_passwd_validator)
def reset_passwd():
    ''' 重置密码 '''
    phone       = request.valid_data.get('phone')
    passwd      = request.valid_data.get('passwd')
    vcode       = request.valid_data.get('vcode')

    code        = ResponseCode.SUCCESS
    msg         = '重置成功'
    real_vcode  = SmsCache.get_vcode(phone)
    print real_vcode, vcode, phone, passwd
    attempt     = InvalidUserResetVcodeCache.incr(phone, 1)
    assert attempt<MAX_TODAY_VCODE_ATTEMPT+1, '今日重置密码验证码错误次数超限'
    if real_vcode==vcode:
        InvalidUserResetVcodeCache.incr(phone, -1)
        UserService.update_passwd(phone, passwd)
        SmsCache.expire_vcode(phone)
        InvalidUserPasswdCache.clear_today_counter(phone)
    else:
        code    = ResponseCode.INVALID_VCODE
        msg     = '验证码错误'
    result      = {
        'code'      : code,
        'msg'       : msg
    }
    return jsonify_response(result)



signup_validator  = Inputs(
    {
     'phone'    : MobileField(msg='请输入手机号'),
     'passwd'   : TextField(msg='请输入密码'),
     'vcode'    : TextField(msg='请输入验证码'),
    }
)
@wechat_loggin_dec(required=False, validator=signup_validator, app=True)
def signup_post():
    ''' 注册'''
    phone       = request.valid_data.get('phone')
    passwd      = request.valid_data.get('passwd')
    vcode       = request.valid_data.get('vcode')

    attempt     = InvalidUserSignupVcodeCache.incr(phone, 1)
    assert attempt<MAX_TODAY_VCODE_ATTEMPT+1, '今日注册验证码错误次数超限'
    real_vcode  = SmsCache.get_vcode(phone)
    if real_vcode==vcode:
        InvalidUserSignupVcodeCache.incr(phone, -1)
        code    = ResponseCode.SUCCESS
        msg     = '注册成功'
        name    = random_str(10)
        user_id = UserService.create_user(name, phone, passwd)
        SmsCache.expire_vcode(phone)
        token   = sign_user(user_id)
        result      = {
            'code'      : code,
            'token'     : token,
            'msg'       : msg,
        }
        if request.open_id:
            # 存在问题 退出美分分换个手机号注册 注册数加1
            PromoteService.set_wechat_user_id(request.open_id, user_id)
            print 'set_wechat_user_id', request.open_id, user_id, 'incr_promote----------<<<<<<<<'
            qrcode_user = PromoteService.get_qrcodeuser_by_open_id(request.open_id)
            if qrcode_user:
                qrcode  = PromoteService.get_qrcode(qrcode_user.qrcode_id)
                print 'qrcode_user', qrcode_user.qrcode_id, 'incr_promote'
                if qrcode:
                    print str(datetime.datetime.now()), request.open_id, user_id, 'incr_promote'
                    PromoteService.incr_promote_reg_count(qrcode.promoter_id)
                    if qrcode.act_type==9:
                        PromoteService.incr_rd_reg_count(qrcode.id)
                        rdcode = PromoteService.get_rd_code_by_qrcode_id(qrcode.id)
#                         if rdcode.reg_count==3:
#                             PromoteService.add_rd_draw_count(user_id, 2)
                else:
                    print 'reg qrcode not exist', 'incr_promote------->>>>>'
        response= jsonify_response(result, with_response=True)
        set_cookie(response, 'sign_user', token, 86400*30)
        return response
    else:
        code    = ResponseCode.INVALID_VCODE
        msg     = '验证码错误'
        result      = {
            'code': code,
            'msg' : msg
            }
        return jsonify_response(result)


from flask import send_from_directory
@wechat_loggin_dec(required=False, need_openid=True, app=True)
def signup():
    ''' 用户注册页面 '''
    #return render_template('user/reg.html')
    return send_from_directory('static/user', 'reg.html')


@wechat_loggin_dec(required=False, need_openid=True, app=True)
def user_login():
    ''' 用户登录页面 '''
    return render_template('user/login.html')


user_login_post_validator  = Inputs(
    {
     'phone'    : MobileField(msg='请输入手机号'),
     'passwd'   : TextField(min_length=1, max_length=100, msg='请输入密码'),
    }
    )
@wechat_loggin_dec(required=False, validator=user_login_post_validator, app=True)
def user_login_post():
    ''' 用户登录post请求 '''
    phone       = request.valid_data.get('phone')
    passwd      = request.valid_data.get('passwd')

    token       = ''
    user        = UserService.get_user_by_phone(phone)
    attempt     = InvalidUserPasswdCache.incr(phone, 1)
    assert attempt<MAX_TODAY_PASSWD_ATTEMPT+1, '今日密码错误次数超限，如需帮助，请联系美分分客服{}'.format(CONTACT)
    if not(user) or user.passwd!=passwd:
        code    = ResponseCode.INVALID_USERNAME_OR_PASSWD
        msg     = '用户名或密码错误'
        result  = {
        'code'      : code,
        'msg'       : msg,
        }
        return jsonify_response(result)
    else:
        InvalidUserPasswdCache.incr(phone, -1)
        code    = ResponseCode.SUCCESS
        msg     = '登录成功'
        token   = sign_user(user.id)
        print request.open_id, user.id , 'open-id  user-id'
        if request.open_id: PromoteService.set_user_open_id(user.id, request.open_id)
        result      = {
            'code'      : code,
            'msg'       : msg,
            'token'     : token
        }
        response= jsonify_response(result, with_response=True)
        set_cookie(response, 'sign_user', token, 86400*30)
        device_id   = request.raw_data.get('device_id')
        if device_id: LogService.log_user_device(device_id, user.id)
        return response



def auth_wechat():
    code    = request.args.get('code')
    state   = request.args.get('state')
    info    = exchange_code_for_token(code)
    access_token    = info['access_token']
    open_id         = info['openid']
    response        = redirect('/user') if not state else redirect(state)
    qr_key          = None
    PromoteService.log_qr_user(qr_key, open_id, -1)
    set_cookie(response, 'open_id', open_id, 86400*30)
    return response



def logout():
    try:
        response = redirect('/static/user/my-not-reg.html')
        del_cookie(response, 'sign_user')
        return response
    except:
        import traceback
        traceback.print_exc()
    return ''




