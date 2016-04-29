# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import json
import math
import random
import time
from datetime import datetime

import redis

from util.utils import get_today_timestamp
from settings import REDIS_HOST
from settings import REDIS_PORT
from settings import CACHE_DB_NO


cache           =   redis.Redis(REDIS_HOST, REDIS_PORT, CACHE_DB_NO)

sms_cache       =   redis.Redis(REDIS_HOST, REDIS_PORT, 1)

common_cache    =   redis.Redis(REDIS_HOST, REDIS_PORT, 10)


current_time = lambda:int(time.time())
def today_remain_seconds():
    now = datetime.now()
    year, month, day = now.year, now.month, now.day
    now_second = time.mktime(now.timetuple())
    cut_now = datetime(year, month, day)
    cut_now_second = time.mktime(cut_now.timetuple())
    return 86400 - int(now_second-cut_now_second)


class SmsCache:
    sms_key = 'sms_vcode:{0}'
    sms_total_key = 'sms_vcode_count:{0}'

    @classmethod
    def set_vcode(cls, phone, vcode, expire=600):
        key = cls.sms_key.format(phone)
        return sms_cache.set(key, vcode, expire)
    @classmethod
    def get_vcode(cls, phone):
        key = cls.sms_key.format(phone)
        return sms_cache.get(key)
    @classmethod
    def expire_vcode(cls, phone):
        key = cls.sms_key.format(phone)
        return sms_cache.expire(key, 0)
        
    @classmethod
    def get_sent_count(cls, phone):
        key = cls.sms_total_key.format(phone)
        return int(sms_cache.get(key) or 0)

    @classmethod
    def incr_sent_count(cls, phone, ex=None):
        key   = cls.sms_total_key.format(phone)
        count = sms_cache.incr(key)
        if not ex: ex = today_remain_seconds()
        sms_cache.expire(key, ex)
        return count

    @classmethod
    def decr_sent_count(cls, phone, ex=None):
        key   = cls.sms_total_key.format(phone)
        count = sms_cache.decr(key)
        if not ex: ex = today_remain_seconds()
        sms_cache.expire(key, ex)
        return count

    @classmethod
    def clear_sent_count(cls, phone):
        key   = cls.sms_total_key.format(phone)
        return sms_cache.expire(key, 1)



class WechatTokenCache(object):
    cache_key   = 'wechat_access_token_cache_key'
    cache       = common_cache

    @classmethod
    def set(cls, access_token, ex=None):
        return cls.cache.set(cls.cache_key, access_token, ex=ex)

    @classmethod
    def get(cls):
        return cls.cache.get(cls.cache_key)


class ChsiCache(object):
    ''' 学信网session缓存 '''
    cache_key   = 'chsi_session_user_id_cache'
    cache       = cache

    @classmethod
    def make_key(cls, user_id):
        return cls.cache_key+str(user_id)

    @classmethod
    def set(cls, user_id, session_pickle):
        cache_key   = cls.make_key(user_id)
        return cls.cache.set(cache_key, session_pickle)

    @classmethod
    def get(cls, user_id):
        cache_key   = cls.make_key(user_id)
        return cls.cache.get(cache_key)


class TodayInvalidCounter(object):
    @classmethod
    def make_key(cls, phone, timestamp):
        return cls.cache_key.format(phone) + '_' + str(timestamp)

    @classmethod
    def incr(cls, phone, amount=1, timestamp=None):
        if not timestamp: timestamp = get_today_timestamp()
        key     = cls.make_key(phone, timestamp=timestamp)
        count   = cls.cache.incr(key, amount)
        return int(count)

    @classmethod
    def clear_today_counter(cls, phone):
        ''' '''
        key     = cls.make_key(phone, get_today_timestamp())
        return cls.cache.delete(key)


class InvalidUserPasswdCache(TodayInvalidCounter):
    ''' 每日用户名错误次数计数 '''
    cache       = cache
    cache_key   = 'invalid_user_passwd_counter_{}'


class InvalidUserSignupVcodeCache(TodayInvalidCounter):
    ''' 每日注册验证码错误次数计数 '''
    cache       = cache
    cache_key   = 'invalid_user_signup_vcode_counter_{}'


class InvalidUserResetVcodeCache(TodayInvalidCounter):
    ''' 每日重置密码验证码错误次数计数 '''
    cache       = cache
    cache_key   = 'invalid_user_reset_vcode_counter_{}'


class AdminInvalidUserPasswdCache(TodayInvalidCounter):
    ''' 管理员每日用户名错误次数计数 '''
    cache       = cache
    cache_key   = 'invalid_admin_user_passwd_counter_{}'


class HospitalInvalidUserPasswdCache(TodayInvalidCounter):
    ''' 医院端管理员每日用户名错误次数计数 '''
    cache       = cache
    cache_key   = 'invalid_hospital_admin_user_passwd_counter_{}'



API_VERSION     = '1.0'

class AppVersion(object):
    ''' 设置app版本 '''
    cache          = cache
    force_key      = 'app_version_force_update_{}'.format(API_VERSION)
    download_key   = 'app_version_android_download_link_{}'.format(API_VERSION)
    title_key      = 'app_version_title_{}'.format(API_VERSION)
    content_key    = 'app_version_content_{}'.format(API_VERSION)
    @classmethod
    def make_key(cls, client_type):
        return 'app_version_{}_{}'.format(API_VERSION, client_type)

    @classmethod
    def set_version(cls, client_type, version_no):
        key     = cls.make_key(client_type)
        return cls.cache.set(key, version_no)

    @classmethod
    def get_version(cls,  client_type):
        key     = cls.make_key(client_type)
        version = cls.cache.get(key) or 0
        return float(version)

    @classmethod
    def set_force_update(cls, is_force):
        val     = '1' if is_force else ''
        return cls.cache.set(cls.force_key, val)
    @classmethod
    def get_force_update(cls):
        return bool(cls.cache.get(cls.force_key))

    @classmethod
    def set_download_link(cls, link):
        return cls.cache.set(cls.download_key, link)
    @classmethod
    def get_download_link(cls):
        return cls.cache.get(cls.download_key) or ''

    @classmethod
    def set_title(cls, title):
        return cls.cache.set(cls.title_key, title)
    @classmethod
    def get_title(cls):
        return cls.cache.get(cls.title_key)

    @classmethod
    def set_content(cls, content):
        return cls.cache.set(cls.content_key, content)
    @classmethod
    def get_content(cls):
        return cls.cache.get(cls.content_key)   



class RoomDesignVoteCounter(object):
    cache       = cache
    cache_key   = 'roomdesign_vote_counter'
    apply_no_key= 'roomdesign_apply_no_key'

    @classmethod
    def incr(cls, room_id, amount=1):
        ''' '''
        return int(math.floor(cls.cache.zincrby(cls.cache_key, room_id, amount)))

    @classmethod
    def rank(cls, room_id):
        return cls.cache.zrevrank(cls.cache_key, room_id) + 1

    @classmethod
    def init(cls, room_id):
        differ = float('.{}'.format(room_id))
        return int(cls.cache.zincrby(cls.cache_key, room_id, differ))

    @classmethod
    def get_vote_by_rank(cls, rank):
        ''' 由排名获得票数 '''
        result  = cls.cache.zrevrange(cls.cache_key, rank-1, rank-1, withscores=True)
        if result: return int(math.floor(result[1]))

    @classmethod
    def incr_apply_no(cls, count=1):
        ''' 生成参赛编号'''
        return str(cls.cache.incr(cls.apply_no_key, count))


if not RoomDesignVoteCounter.cache.get(RoomDesignVoteCounter.apply_no_key):
    RoomDesignVoteCounter.incr_apply_no(1000000) #初始化参赛编号







