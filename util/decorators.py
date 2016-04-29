# -*- coding: utf-8 -*-
import re
import time
import json
from functools import wraps

from flask import request
from flask import Response
from flask import redirect
from flask import make_response
from util.utils        import union_dict
from util.utils        import jsonify_response
from util.utils        import jsonify 
from util.sign         import extract_user_id
from util.sign         import get_cookie
from util.sign         import sign_user
from util.sign         import check_token
from util.sign         import del_cookie
from util.sign         import check_hospital_token
from util.sign         import check_promote_token
from thirdparty.wechat import get_user_snsapi_base_url
from constants         import ResponseCode
from udp_server        import send_msg


def get_err_response(msg):
    ''' 异常响应模版 '''
    return jsonify_response(
        {
        "code": ResponseCode.SERVER_ERROR,
        "msg": msg
        },
        with_response=True
    )

p = re.compile('.*?"code": (?P<code>\d+)')

def is_err_response(result):
    ''' '''
    result = p.search(result or '')
    if result:
        a = result.groupdict() or {}
        if a.get('code')!='0':
            return True


def udp_log(resp=None):
    ''' udp日志 '''
    timestamp   = time.time()
    data        = {
        'timestamp'     : timestamp,
        'remote_addr'   : request.remote_addr,
        'url'           : request.path,
        'user_id'       : getattr(request, 'user_id', None),
        'data'          :  getattr(request, 'valid_data', None),
        'args'          : request.args,
        'form'          : request.form,
        'cookies'       : request.cookies.get('sign_user'),
        'cookies'       : request.cookies.get('sign_user'),
        'open_id'       : getattr(request, 'open_id', None),
        'user_agent'    : request.headers.get('User-Agent'),
        'resp'          : resp
        }
    data_line   = jsonify(data)
    send_msg(data_line)


def admin_udp_log():
    ''' admin udp日志 '''
    timestamp   = time.time()
    data        = {
        'timestamp'     : timestamp,
        'remote_addr'   : request.remote_addr,
        'url'           : request.path,
        'data'          : getattr(request, 'raw_data', None),
        'args'          : request.args,
        'form'          : request.form,
        'token'         : request.cookies.get('token'),
        'user_agent'    : request.headers.get('User-Agent'),
        'log_cat'       : 1, #1管理端
        }
    data_line   = jsonify(data)
    send_msg(data_line)


'''
只有在支付页面才需要open_id
'''
def wechat_loggin_dec(required=True, next='', need_openid=False,  validator=None, app=True):
    ''' need_openid 如果是在微信浏览器里面 则跳转到静默登录获取openid '''
    def _wechat_loggin_dec(func):
        @wraps(func)
        def _func(*args, **kw):
            has_err = True
            try:
                result  = None
                request.is_app      = app
                order_id            = str(request.args.get('order_id') or '')
                oauth_url           = get_user_snsapi_base_url(state=request.url)
                req_open_id         = get_cookie('open_id')
                req_user_sign       = get_cookie('sign_user')
                req_user_id         = extract_user_id(req_user_sign)
                if need_openid and not(req_open_id) and 'meifenfen.com' in request.url:
                        print 'redirect oauth'
                        print oauth_url
                        result= make_response(redirect(oauth_url))
                        return result
                request.valid_data  = None
                if validator:
                    raw_get_data    = request.args.to_dict()
                    raw_post_data   = request.form.to_dict()
                    raw_data        = union_dict(raw_get_data, raw_post_data)
                    err, valid_data = validator.validate(raw_data)
                    assert not err, err
                    request.valid_data = valid_data
                    request.raw_data   = raw_data
                    req_user_sign   = req_user_sign or valid_data.get('sign_user') or ''
                if not req_user_sign:#开发调试 兼容app
                    req_user_sign   = request.args.get('sign_user') or request.form.get('sign_user')
                    req_user_id     = extract_user_id(req_user_sign)
                if req_user_sign: req_user_id     = extract_user_id(req_user_sign)
                print 'req_user_sign:', req_user_sign
                if not(app) and not(req_open_id):
                    result = redirect(oauth_url)
                    return result
                if required and not(req_user_id and req_user_sign==sign_user(req_user_id)):
                    if not app:
                        result = redirect('/user/login?next='+(next or request.url))
                    else:
                        result = jsonify_response(
                            {
                             'code': ResponseCode.NEED_LOGIN,
                             'msg': '请登录'
                            }, with_response=True
                        )
                    del_cookie(result, 'sign_user')
                    return result
                request.open_id = req_open_id
                user_id         = req_user_id
                if user_id and user_id.isdigit() and req_user_sign==sign_user(req_user_id):
                    request.user_id = int(user_id)
                else:
                    request.user_id = None
                result  = func(*args, **kw)
                has_err = False
                return result
            except ValueError as e:
                import traceback
                traceback.print_exc()
                result  = get_err_response(getattr(e, 'message', '服务器异常'))
            except AssertionError as e:
                import traceback
                traceback.print_exc()
                result  = get_err_response(getattr(e, 'message', '服务器异常'))
            except Exception as e:
                import traceback
                traceback.print_exc()
                result  = get_err_response('服务器异常')
            else:
                return result
            finally:
                try:
                    resp = None
                    data = None
                    if isinstance(result, (list,tuple)):
                        data = result[0]
                    elif isinstance(result, Response):
                        try:
                            data = getattr(result, 'data', None)
                        except:
                            pass
                    if has_err:# or is_err_response(data):
                        resp=data
                    udp_log(resp)
                    return result
                except Exception as e:
                    import traceback
                    traceback.print_exc()
                    return get_err_response('服务器异常')
        return _func
    return _wechat_loggin_dec


def admin_json_dec(required=True, validator=None, roles=[]):
    def _admin_json_dec(func):
        @wraps(func)
        def _func(*args, **kw):
            from ops.admin import AdminService
            try:
                request.valid_data = None
                if validator:
                    raw_get_data    = request.args.to_dict()
                    raw_post_data   = request.form.to_dict()
                    raw_req_data    = json.loads(request.data) if request.data else {}
                    raw_data        = union_dict(raw_get_data, raw_post_data, raw_req_data)
                    err, valid_data = validator.validate(raw_data)
                    assert not err, err
                    request.valid_data = valid_data
                admin_name   = None
                is_valid     = False
                if get_cookie('token'):
                    is_valid, admin_name = check_token(get_cookie('token'))
                if required and not(get_cookie('token') and is_valid):
                    response = jsonify_response(
                        {
                        "code": -1,
                        "msg": '请登录'
                        }
                    )
                    return response
                if required:
                    admin   = AdminService.get_admin(admin_name)
                    request.admin = admin
                    request.name = admin_name
                    if not admin or (roles and admin.cat not in roles):
                        return jsonify_response(
                                {
                                "code": -2,
                                "msg": '没有相关权限'
                                }
                            )
                result = func(*args, **kw) or ''
            except ValueError as e:
                import traceback
                traceback.print_exc()
                return jsonify_response(
                    {
                    "code": 10000,
                    "msg": getattr(e, 'msg', '服务器异常')
                    }
                )
            except AssertionError as e:
                print 'assert'
                import traceback
                traceback.print_exc()
                return jsonify_response(
                    {
                    "code": 10000,
                    "msg": getattr(e, 'message', '') or '服务器异常'
                    }
                )
            except Exception as e:
                import traceback
                traceback.print_exc()
                return get_err_response('服务器异常')
            else:
                return result
            finally:
                try:
                    admin_udp_log()
                except Exception as e:
                    pass
        return _func
    return _admin_json_dec



def hospital_dec(required=True, validator=None):
    def _hospital_dec(func):
        @wraps(func)
        def _func(*args, **kw):
            try:
                request.valid_data = None
                if validator:
                    raw_get_data    = request.args.to_dict()
                    raw_post_data   = request.form.to_dict()
                    raw_req_data    = json.loads(request.data) if request.data else {}
                    print raw_req_data, 'raw_req_data'
                    raw_data        = union_dict(raw_get_data, raw_post_data, raw_req_data)
                    err, valid_data = validator.validate(raw_data)
                    print err, valid_data
                    assert not err, err
                    request.valid_data = valid_data
                print request.url
                print request.path
                print get_cookie('sign'), 'sign'
                is_valid, name  = check_hospital_token(get_cookie('sign'))
                if required and not(get_cookie('sign') and is_valid):
                    return redirect('/hospital/login/')
                    return jsonify_response(
                        {
                        "code": -1,
                        "msg": '请登录'
                        }
                    )
                request.name    = name
                result = func(*args, **kw) or ''
            except ValueError as e:
                import traceback
                traceback.print_exc()
                return jsonify_response(
                    {
                    "code": 10000,
                    "msg": getattr(e, 'msg', '服务器异常')
                    }
                )
            except AssertionError as e:
                print 'assert'
                import traceback
                traceback.print_exc()
                return jsonify_response(
                    {
                    "code": 10000,
                    "msg": getattr(e, 'message', '') or '服务器异常'
                    }
                )
            except Exception as e:
                import traceback
                traceback.print_exc()
                return get_err_response('服务器异常')
            else:
                return result
        return _func
    return _hospital_dec



def promote_dec(required=True, validator=None):
    ''' 推广登录 '''
    def _promote_dec(func):
        @wraps(func)
        def _func(*args, **kw):
            try:
                request.valid_data = None
                if validator:
                    raw_get_data    = request.args.to_dict()
                    raw_post_data   = request.form.to_dict()
                    raw_req_data    = json.loads(request.data) if request.data else {}
                    print raw_req_data, 'raw_req_data'
                    raw_data        = union_dict(raw_get_data, raw_post_data, raw_req_data)
                    err, valid_data = validator.validate(raw_data)
                    print err, valid_data
                    assert not err, err
                    request.valid_data = valid_data
                print request.url
                print request.path
                print get_cookie('promote_sign'), 'promote_sign'
                is_valid, name  = check_promote_token(get_cookie('promote_sign'))
                if required and not(get_cookie('promote_sign') and is_valid):
                    return redirect('/promote/login/')
                    return jsonify_response(
                        {
                        "code": -1,
                        "msg": '请登录'
                        }
                    )
                request.name    = name
                result = func(*args, **kw) or ''
            except ValueError as e:
                import traceback
                traceback.print_exc()
                return jsonify_response(
                    {
                    "code": 10000,
                    "msg": getattr(e, 'msg', '服务器异常')
                    }
                )
            except AssertionError as e:
                print 'assert'
                import traceback
                traceback.print_exc()
                return jsonify_response(
                    {
                    "code": 10000,
                    "msg": getattr(e, 'message', '') or '服务器异常'
                    }
                )
            except Exception as e:
                import traceback
                traceback.print_exc()
                return get_err_response('服务器异常')
            else:
                return result
        return _func
    return _promote_dec



def dev_dec(func):
    ''' 调试debug '''
    @wraps(func)
    def _inner(*args, **kw):
        try:
            return func(*args,**kw)
        except Exception as e:
            import traceback
            traceback.print_exc()
    return _inner





