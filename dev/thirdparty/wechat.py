# -*- coding: utf-8 -*-
import time
import urllib
import urllib2
import hashlib

from flask import request
import weixin.client
WechatAuthAPI = weixin.client.WeixinAPI

from wechat_sdk import WechatBasic
from settings   import WECHAT_APP_ID
from settings   import WECHAT_APP_SECRET
from settings   import WECHAT_APP_TOKEN
from settings   import SERVER_NAME
from celery.contrib.methods import task_method
from celery import current_app

class WechatInfo(WechatBasic):

    def set_cache(self, cache):
        self.cache = cache

    @property
    def access_token(self):
        token   = self.cache.get()
        if not token:
            self.refresh_wechat_token()
        token   = self.cache.get()
        return token

    @current_app.task(filter=task_method)
    def refresh_wechat_token(self):
        ''' 比较特殊 tasks的参数第一个bound了self '''
        data            = self.grant_token()
        access_token    = data["access_token"]
        expires_in      = data["expires_in"]
        self.cache.set(access_token, expires_in-60)

    @property
    def jsapi_ticket(self):
        self._check_appid_appsecret()
    
        if getattr(self, '__jsapi_ticket', None):
            now = time.time()
            if self.__jsapi_ticket_expires_at - now > 60:
                return self.__jsapi_ticket
        else:
            self.grant_jsapi_ticket()
        data    = self.grant_jsapi_ticket()
        return self.__jsapi_ticket

    def grant_jsapi_ticket(self, override=True):
        """
        获取 Jsapi Ticket
        详情请参考 http://mp.weixin.qq.com/wiki/7/aaa137b55fb2e0456bf8dd9148dd613f.html#.E9.99.84.E5.BD.951-JS-SDK.E4.BD.BF.E7.94.A8.E6.9D.83.E9.99.90.E7.AD.BE.E5.90.8D.E7.AE.97.E6.B3.95
        :param override: 是否在获取的同时覆盖已有 jsapi_ticket (默认为True)
        :return: 返回的 JSON 数据包
        :raise HTTPError: 微信api http 请求失败
        """
        self._check_appid_appsecret()
        # force to grant new access_token to avoid invalid credential issue
        response_json = self._get(
            url="https://api.weixin.qq.com/cgi-bin/ticket/getticket",
            params={
                "access_token": self.access_token,
                "type": "jsapi",
            }
        )
        if override:
            self.__jsapi_ticket = response_json['ticket']
            self.__jsapi_ticket_expires_at = int(time.time()) + response_json['expires_in']
        return response_json

wechat      = WechatInfo(token=WECHAT_APP_TOKEN, appid=WECHAT_APP_ID, appsecret=WECHAT_APP_SECRET)


menu_data   = {
    "button":[
        {
            "type": "view",
            "name": u"分期整形",
            "url": "http://{}/user/index".format(SERVER_NAME),
        },
        {
            "type": "view",
            "name": u"寝室大赛",
            "url": "http://{}/static/user/Activities/home.html".format(SERVER_NAME),
        },
        {
            "name": u"更多",
            "sub_button":[
                {
                    "type":"view",
                    "name":u"我",
                    "url": "http://{}/static/user/my-not-reg.html".format(SERVER_NAME),
                },
                {
                    "type":"view",
                    "name":u"下载APP",
                    "url": "http://{}/static/user/downLoad.html".format(SERVER_NAME),
                },
                {
                    "type":"view",
                    "name":u"帮助中心",
                    "url": "http://{}/user/help.html".format(SERVER_NAME),
                },
                {
                    "type": "click",
                    "name": u"联系客服",
                    "key": "contact_us",
                },
                {
                    "type":"view",
                    "name":u"医院入口",
                    "url": "http://{}/hospital/".format(SERVER_NAME),
                },
            ]
        }
    ]}


def create_menu():
    ''' 创建公众号菜单 '''
    return wechat.create_menu(menu_data)




REDIRECT_URI = 'http://{}/user/'.format(SERVER_NAME)


AuthApi = WechatAuthAPI(appid=WECHAT_APP_ID,
                        app_secret=WECHAT_APP_SECRET,
                        redirect_uri=REDIRECT_URI)


def get_user_snsapi_base_url(redirecturi='http://{}/user/auth'.format(SERVER_NAME), state='STATE'):
    '''返回snsapi_base静默登录url '''
    link = ('''
https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_base&state=%s#wechat_redirect
'''%(WECHAT_APP_ID, urllib.quote_plus(redirecturi), state)).strip()
    return link

def exchange_code_for_token(code):
    ''' 通过微信oauth静默登录认证回调的code参数 获取 access_token openid
        返回值是一个字典 包含access_token, openid
    '''
    return AuthApi.exchange_code_for_access_token(code=code)


def get_user_info(access_token, openid):
    ''' 通过code获取的access_token及open_id获取oauth授权登录用户信息 '''
    auth_api = WechatAuthAPI(access_token=access_token)
    user     = auth_api.user(openid=openid)
    return user
 
 

def create_link_str(params):
    result = ''
    for i in sorted(params.keys()):
        result += i+'='+params[i]+'&'
    return result.rstrip('&')
from util.utils import random_str
def gen_noncestr():
    return random_str(10)

def get_sign(path, timestamp, noncestr):
    data =  dict(
        jsapi_ticket = wechat.jsapi_ticket,
        noncestr= noncestr,
        timestamp= timestamp,
        url = path,
        )
    m = hashlib.sha1()
    m.update(create_link_str(data))
    print create_link_str(data)
    return m.hexdigest()


def get_jssdk_context(link=None):
    ''' js sdk 参数 '''
    try:
        noncestr = gen_noncestr()
        timestamp= str(time.time())
        sign     = get_sign(link or request.url, timestamp, noncestr)
    
        context = {
            'domain': SERVER_NAME,
            'appid': WECHAT_APP_ID,
            'noncestr': noncestr,
            'timestamp': timestamp,
            'sign': sign,
            }
    
        return context
    except:
        import traceback
        traceback.print_exc()
        print 'jssdk error'
        return {}



def create_qrcode(scene_id):
    ''' 创建二维码ticket'''
    data = {
        "action_name": "QR_LIMIT_SCENE",
        "action_info": {"scene": {"scene_id": scene_id}}
        }
    a = wechat.create_qrcode(data)
    ticket  = a['ticket']
    print ticket, 'ticket'
    return ticket, wechat.show_qrcode(ticket)

import json
import requests
def send_group_mnews(open_ids, media_id):
    ''' 群发消息 '''
    link    = 'https://api.weixin.qq.com/cgi-bin/message/mass/send?access_token={}'.format(wechat.access_token)
    data    = {
        "touser": open_ids,
        "mpnews":{
            "media_id":"123dsdajkasd231jhksad"
        },
        "msgtype":"mpnews"
        }
    response= requests.post(link, data=json.dumps(data))
    return response


def create_article():
    link    = 'https://api.weixin.qq.com/cgi-bin/media/uploadnews?access_token={}'.format(wechat.access_token)
    article = {
       "articles": [
             {
                 "thumb_media_id":'vtZ1MJiazhv0FicHsbhOicw7fRKPbKDQtH85oERG82aia2Eicn5BlEoyYZff6KXTgN8X3gYWVeRVx1ZR7bMmhIU7JgQ',
                 "author":"xxx",
                 "title":"Happy Day",
                 "content_source_url":"www.qq.com",
                 "content":"content",
                 "digest":"digest",
                 "show_cover_pic":"1"
             },
             {
                 "thumb_media_id":'vtZ1MJiazhv0FicHsbhOicw7fRKPbKDQtH85oERG82aia2Eicn5BlEoyYZff6KXTgN8X3gYWVeRVx1ZR7bMmhIU7JgQ',
                 "author":"xxx",
                 "title":"Happy Day",
                 "content_source_url":"www.qq.com",
                 "content":"content",
                 "digest":"digest",
                 "show_cover_pic":"0"
             }
       ]
    }
    response= requests.post(link, data=json.dumps(article))
    print response.text
    return response


def upload_image():
    ''' '''
    link = 'https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token={}'.format(wechat.access_token)
    files = {'media': open('/tmp/meifenfen/static/user/img/logo.png', 'rb')}
    return requests.post(link, files=files)




