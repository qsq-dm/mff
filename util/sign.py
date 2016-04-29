# -*- coding: utf-8 -*-
import os
import time
import hashlib

from flask import request

from settings import ADMIN_COOKIE_KEY
from settings import HOSPITAL_COOKIE_KEY
from settings import PROMOTE_COOKIE_KEY
from settings import SECRET_USER_COOKIE
from settings import DOMAIN


def sign_user(user_id):
    if not user_id: return None
    md5     = hashlib.md5()
    md5.update(str(user_id)+SECRET_USER_COOKIE)
    return str(user_id)+'.'+md5.hexdigest()


def extract_user_id(sign_user_str):
    ''' '''
    return (sign_user_str or '').split('.')[0]


def get_cookie(name):
    return request.cookies.get(name) or os.environ.get(name.upper())


def set_cookie(response, key, val, expire=86400*30):
    response.delete_cookie(key, domain=DOMAIN)
    response.set_cookie(key, str(val), expire, DOMAIN)


def del_cookie(response, key):
    response.delete_cookie(key, domain=DOMAIN)
    response.set_cookie(key, expires=0)


TOKEN_DLIMITER = ','
def check_token(token_str, key=ADMIN_COOKIE_KEY):
    token_args = (token_str or '').split(TOKEN_DLIMITER)
    if len(token_args)!=3: return False, None

    name, time_str, token = token_args
    md5 = hashlib.new("md5")
    data = '.'.join((unicode(name), unicode(time_str), key))
    md5.update(str(data))
    access_token = md5.hexdigest()

    is_valid = token==access_token
    return is_valid, name


def check_hospital_token(token_str):
    return check_token(token_str, HOSPITAL_COOKIE_KEY)


def check_promote_token(token_str):
    return check_token(token_str, PROMOTE_COOKIE_KEY)


def gen_token(name, key=ADMIN_COOKIE_KEY):
    name  = unicode(name)
    md5  = hashlib.new("md5")
    data = {}
    current_time = unicode(int(time.time()))
    data = name+'.'+current_time+'.'+key
    md5.update(str(data))
    access_token = md5.hexdigest()
    token = TOKEN_DLIMITER.join([name, current_time, access_token])
    #token = encode(token)
    return token


def gen_hospital_token(name):
    return gen_token(name, HOSPITAL_COOKIE_KEY)


def gen_promote_token(name):
    return gen_token(name, PROMOTE_COOKIE_KEY)



