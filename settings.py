# -*- coding: utf-8 -*-
import os
import time


MAX_TODAY_PASSWD_ATTEMPT= 6
MAX_TODAY_VCODE_ATTEMPT = 10
BASE_DIR                = os.path.abspath(os.path.dirname(__file__))
STATIC_DIR              = os.path.join(BASE_DIR,'static/')
TEMPLATE_DIR            = os.path.join(BASE_DIR,'templates/')


APPEND_SLASH            = True

RUN_PORT                = 80

DEFAULT_CREDIT          = 10000

CONTACT                 = '021-60483658'

WECHAT_APP_ID           = 'wx284c24dbdca7b377test'
WECHAT_APP_SECRET       = 'df80d4d3213883e804eca31137c1de1f---'
WECHAT_APP_TOKEN        = 'vDKXGxLyN23PEX'
WECHAT_MCHID            = '1278286901'
WECHAT_KEY              = 'ggH73uoRJnYjqFXfRKWijidzAZxUgLvb'
WECHAT_CERT_PEM         = 'wx_cert/apiclient_cert.pem'
WECHAT_KEY_PEM          = 'wx_cert/apiclient_key.pem'
APP_WECHAT_CERT_PEM     = 'wx_app_cert/apiclient_cert.pem'
APP_WECHAT_KEY_PEM      = 'wx_app_cert/apiclient_key.pem'

APP_WECHAT_ID           = 'wx1e8901446967b46b'
APP_WECHAT_SECRET       = '6a683136a58f5d152daee995dde838f5'
APP_MCH_ID              = '1305025101'
APP_WECHAT_KEY          = 'y4JetJrzMMctjnVJUnRFvqitURMgwYsz'

DOMAIN                  = '127.0.0.1'
SERVER_NAME             = '139.196.6.231'


SECRET_USER_COOKIE      = os.environ.get('APP_USER_COOKIE_SIGN', 'df2121280332d4d3213883e804eca31137c1de1f')
ADMIN_COOKIE_KEY        = 'ADMIN_COOKIE_KEY' 
HOSPITAL_COOKIE_KEY     = 'HOSPITAL_COOKIE_KEY'
PROMOTE_COOKIE_KEY      = 'PROMOTE_COOKIE_KEY_2015'

REDIS_PORT              = 6379
REDIS_HOST              = '127.0.0.1'
MAIN_MYSQL_URI          = 'mysql://root@localhost/main?charset=utf8mb4'
IMAGE_HOST_URL_DOMAIN   = '7xnpdb.com1.z0.glb.clouddn.com'

DEFAULT_IMAGE           = 'http://7xnpdb.com2.z0.glb.qiniucdn.com/o_1a4u9raim1rpcckf59vq7q1gth1LG11IG]7F5G5%7D861P1IUW[T.jpg'
ANONY_IMAGE             = 'http://7xnpdb.com2.z0.glb.qiniucdn.com/o_1a4u9raim1rpcckf59vq7q1gth1LG11IG]7F5G5%7D861P1IUW[T.jpg'

CACHE_DB_NO                    = 0

if os.environ.get('APP_ENV')=='dev':
    print 'env', 'dev'
    from setting.dev import *
    from sql_profile import *
elif os.environ.get('APP_ENV')=='production':
    print 'env', 'production'
    from setting.production import *
else:
    print 'env', 'local'
    from setting.local import *
from sql_profile import *


WX_PAY_NOTIFY_URL              = "http://{}/user/wx_pay_callback/".format(SERVER_NAME)
WX_REPAYMENT_NOTIFY_URL        = "http://{}/user/wx_repayment_callback/".format(SERVER_NAME)
WX_REDPACK_NOTIFY_URL          = "http://{}/user/wx_redpack_callback/".format(SERVER_NAME)

WX_APP_PAY_NOTIFY_URL          = "http://{}/api/wxapp_pay_callback/".format(SERVER_NAME)
WX_APP_REPAYMENT_NOTIFY_URL    = "http://{}/api/wxapp_repayment_callback/".format(SERVER_NAME)

from celery import Celery
celery = Celery()
celery.config_from_object('setting.celeryconfig')


ITEM_ORDER_CHOICES   = [
    {'id':1, 'name':'综合排序'},
    {'id':2, 'name':'销量优先'},
    {'id':3, 'name':'低价优先'},
    {'id':4, 'name':'高价优先'},
    ]

HOSPITAL_ORDER_CHOICES   = [
    {'id':1, 'name':'综合排序'},
    {'id':2, 'name':'销量优先'},
    {'id':3, 'name':'好评优先'},
    ]



CAT_ICONS                  = {
    0: 'http://www.meifenfen.com/static/user/img/tuijian_hui.png',
    1: 'http://www.meifenfen.com/static/user/img/pifu_hui.png',
    2: 'http://www.meifenfen.com/static/user/img/yanbu_hui.png',
    3: 'http://www.meifenfen.com/static/user/img/bibu_hui.png',
    4: 'http://www.meifenfen.com/static/user/img/maofa_hui.png',
    5: 'http://www.meifenfen.com/static/user/img/weizhengxing_hui.png',
    6: 'http://www.meifenfen.com/static/user/img/yachi_hui.png',
    7: 'http://www.meifenfen.com/static/user/img/xingti_hui.png',
    8: 'http://www.meifenfen.com/static/user/img/pf-hui.png',
    9: 'http://www.meifenfen.com/static/user/img/banyongjiu-hui.png',
    10: 'http://www.meifenfen.com/static/user/img/icon-cb0.png',
    11: 'http://www.meifenfen.com/static/user/img/icon-eb0.png',
    }
CAT_ICONS_ACTIVE           = {
    0: 'http://www.meifenfen.com/static/user/img/tuijian_hong.png',
    1: 'http://www.meifenfen.com/static/user/img/pifu_hong.png',
    2: 'http://www.meifenfen.com/static/user/img/yanbu_hong.png',
    3: 'http://www.meifenfen.com/static/user/img/bibu_hong.png',
    4: 'http://www.meifenfen.com/static/user/img/maofa_hong.png',
    5: 'http://www.meifenfen.com/static/user/img/weizhengxing_hong.png',
    6: 'http://www.meifenfen.com/static/user/img/yachi_hong.png',
    7: 'http://www.meifenfen.com/static/user/img/xingti_hong.png',
    8: 'http://www.meifenfen.com/static/user/img/pf-hong.png',
    9: 'http://www.meifenfen.com/static/user/img/banyongjiu-hong.png',
    10: 'http://www.meifenfen.com/static/user/img/icon-cb1.png',
    11: 'http://www.meifenfen.com/static/user/img/icon-eb1.png',
    }

