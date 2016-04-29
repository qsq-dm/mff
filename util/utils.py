# -*- coding: utf-8 -*-
import random
import hashlib
import hmac
import time
import json
import datetime
import calendar
import datetime                   as dt_mod
from   datetime     import datetime as dt_obj
from random         import Random

from flask          import Response

from settings       import IMAGE_HOST_URL_DOMAIN
from settings       import SERVER_NAME


def get_time_str_from_dt(date, format='%Y-%m-%d %H:%M:%S'):
    return date.strftime(format)


def format_dt(date, format='%Y-%m-%d %H:%M:%S'):
    now     = dt_obj.now()
    if now.year==date.year and now.month==date.month and now.day==date.day:
        return '今日'
    return date.strftime('%m.%d')


def get_timestamp(s,format='%Y-%m-%d %H:%M:%S'):
    return int(time.mktime(dt_obj.strptime(s, format).timetuple()))

def date_to_datetime(date, format='%Y-%m-%d'):
    date            = date[:19]
    timestamp       = get_timestamp(date, format)
    current_time    = dt_mod.datetime.fromtimestamp(timestamp)
    return current_time


def prefix_img_domain(img_key, domain=IMAGE_HOST_URL_DOMAIN):
    if not img_key: return ''
    if 'http' in img_key: return img_key
    if domain in img_key:
        return img_key
    return 'http://'+domain+'/'+img_key

def prefix_http(link):
    ''' 前缀http '''
    if not link: return ''
    if 'http' in link: return link
    return 'http://' + link


def prefix_servername(link):
    if not link: return ''
    if 'http' in link: return link
    link    = link.lstrip('/')
    return 'http://{}/{}'.format(SERVER_NAME, link)


def prefix_img_list(images, domain=IMAGE_HOST_URL_DOMAIN):
    ''' 图片链接绝对路径带http '''
    images =   map(lambda i:i.strip(), (images or '').split(','))
    return map(lambda key:prefix_img_domain(key, domain), images)

def prefix_img_list_thumb(images, domain=IMAGE_HOST_URL_DOMAIN, width=200):
    ''' 图片链接绝对路径带http '''
    images   = filter(bool, (images or '').split(','))
    result   = map(lambda key:prefix_img_domain(key, domain), images)
    fix_func = lambda i: i+'?imageView2/1/w/{}/h/{}'.format(width, width)
    return map(fix_func, result)


def str_to_int_list(comma_str):
    ''' "1,2,3" > [1,2,3] '''
    str_list    = filter(bool, (comma_str or '').split(','))
    return map(int, str_list)


def jsonify(data, encoder=None):
    if isinstance(data, dict):
        data  = Utf8Dict(data)()
    if isinstance(data, (tuple, list)):
        data  = Utf8Dict.Utf8List(list(data))
    return json.dumps(data, ensure_ascii=False, cls=encoder or Utf8Encoder)


def jsonify_response(result, with_response=False):
#     if not with_response:
#         return jsonify(result), 200, {'Content-Type': 'application/json; charset=utf-8'}
    return Response(
        response=jsonify(result),
        content_type='application/json; charset=utf-8',
        mimetype="application/json"
        )


def template_response(result):
    return Response(
        response=result
        )


def js_response(result):
    return Response(
        response=(result),
        content_type='application/javascript; charset=utf-8',
        mimetype="application/javascript"
        )


class Utf8Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, unicode):
            return obj.encode('utf8')
        else:
            return json.JSONEncoder.default(self, obj)

class Utf8Dict(dict):
    class Utf8List(list):
        def __init__(self, obj):
            self._obj = obj

        def __iter__(self, *args, **kwargs):
            iter = list.__iter__(self._obj, *args, **kwargs)
            for k in iter:
                if isinstance(k, (tuple, list)):
                    yield Utf8Dict.Utf8List(k)
                elif isinstance(k, dict):
                    yield Utf8Dict(k)()
                elif isinstance(k, unicode):
                    yield k.encode('utf8')
                elif isinstance(k, dt_obj):
                    yield str(k)
                else:
                    yield k
    def __init__(self, obj):
        self._obj = obj

    def __iter__(self, *args, **kwargs):
        iter = dict.__iter__(self._obj, *args, **kwargs)
        for k in iter:
            yield k

    def __getitem__(self, *args, **kwargs):
        value = dict.__getitem__(self._obj, *args, **kwargs)
        if isinstance(value, unicode):
            return value.encode('utf8')
        elif isinstance(value, (tuple,list)):
            value = list(value)
            for i in xrange(len(value)):
                if isinstance(value[i], unicode):
                    value[i] = value[i].encode('utf8')
                elif isinstance(value[i], dict):
                    value[i] = Utf8Dict(value[i])()
                elif isinstance(value[i], (tuple,list)):
                    value[i] = Utf8Dict.Utf8List(value[i])
            return value
        elif isinstance(value, dict):
            return Utf8Dict(value)()
        elif isinstance(value, dt_obj):
            return str(value)
        else:
            return value
    def __setitem__(self, *args, **kwargs):
        return dict.__setitem__(self._obj, *args, **kwargs)

    def __call__(self):
        data = {}
        for k in self:
            data[k] = self.__getitem__(k)
        return data


def union_dict(*args):
    ''' 把多个字典合并 后面的覆盖前面的'''
    result = {}
    for i in args:
        result.update(i)
    return result


def comma_str_to_list(comma_str):
    ''' 逗号分割的字符串转化为列表 '''
    comma_str   = comma_str or ''
    comma_str   = comma_str.replace('，', ',')
    str_list    = comma_str.split(',')
    return filter(bool, str_list)


def keep_fields_from_list(items, fields):
    ''' 保留列表item中的指定字段 去掉其余字段 '''
    for item in items:
        for key in item.keys():
            if key not in fields: item.pop(key)


def template_response(result):
    return Response(
        response=result
        )


def random_str(randomlength=6):
    string  = ''
    chars   = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length  = len(chars) - 1
    random  = Random()
    for i in range(randomlength):
        string += chars[random.randint(0, length)]
    return string.lower()


def gen_item_no():
    ''' 商品编号 '''
    now     = dt_obj.now()
    prefix  = get_time_str_from_dt(now, '%y%m%d')
    return prefix + random_no(randomlength=4)


def random_no(randomlength=6):
    string  = ''
    chars   = '0123456789'
    length  = len(chars) - 1
    random  = Random()
    for i in range(randomlength):
        string  += chars[random.randint(0, length)]
    return string


def trans_list(items, field, new_field, trans_dict, pop=False):
    print trans_dict, field
    for item in items:
        field_val = item[field]
        item[new_field]  =   trans_dict.get(field_val) \
                            if not pop else trans_dict.pop(field_val)


day_delta       = dt_mod.timedelta(days=1)
hour_delta      = dt_mod.timedelta(hours=1)
minute_delta    = dt_mod.timedelta(minutes=1)
second_delta    = dt_mod.timedelta(seconds=1)


def calc_expire_remain(end_time_str, status=0):
    end_time        = date_to_datetime(end_time_str, '%Y-%m-%d %H:%M:%S')
    delta           = end_time-dt_obj.now()
    total_seconds   = int(delta.total_seconds())
    if total_seconds>86400:
        return '{}天到期'.format(total_seconds/86400)
    elif total_seconds>3600:
        return '{}小时到期'.format(total_seconds/3600)
    elif total_seconds>60:
        return '{}分钟到期'.format(total_seconds/60)
    elif status==0:
        return '已过期'
    else:
        return '{}前'.format(end_time_str[:10])


def get_current_period():
    ''' 本期帐单log开始 本期结束 '''
    now         = dt_obj.now()
    year        = now.year
    month       = now.month
    day         = now.day
    end         = dt_obj(year=year, month=month, day=1) - second_delta
    if month>1:
        start   = dt_obj(year=year, month=month-1, day=1)
    else:
        start   = dt_obj(year=year-1, month=12, day=1)
    return start, end


def get_current_deadline():
    ''' 获取当期帐单截止日期 '''
    now         = dt_obj.now()
    year        = now.year
    month       = now.month
    day         = now.day
    if month+1>12:
        end         = dt_obj(year=year+1, month=month+1-12, day=2) - second_delta
    else:
        end         = dt_obj(year=year, month=month+1, day=2) - second_delta
    return end


def is_delayed():
    return dt_obj.now().day>15


def get_next_period():
    ''' 下期开始 下期结束 '''
    now         = dt_obj.now()
    year        = now.year
    month       = now.month
    day         = now.day
    start       = dt_obj(year=year, month=month, day=1)
    if month==12:
        end     = dt_obj(year=year+1, month=1, day=1) - second_delta
    else:
        end     = dt_obj(year=year, month=month+1, day=1) -second_delta
    return start, end


def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = int(sourcedate.year + month / 12 )
    month = month % 12 + 1
    day = min(sourcedate.day,calendar.monthrange(year,month)[1])
    day = datetime.date(year,month,day)
    hour            = sourcedate.hour
    minute          = sourcedate.minute
    second          = sourcedate.second
    return dt_obj(year=day.year, month=day.month, day=day.day, hour=hour, minute=minute, second=second)


def get_due_time(index):
    ''' 计算每一期应还时间 '''
    due_time_start  = get_current_deadline()
    hour            = due_time_start.hour
    minute          = due_time_start.minute
    second          = due_time_start.second
    return add_months(due_time_start, index)


def abbreviated_pages(n, page):
    """
    分页数 eg 1 2 3 ... 10 11 ... 100
    """
    if not(0 < n): return {}
    assert(0 < page <= n)

    if n <= 10:
        pages = set(range(1, n + 1))
    else:
        pages = (set(range(1, 4))
                 | set(range(max(1, page - 2), min(page + 3, n + 1)))
                 | set(range(n - 2, n + 1)))

    def display():
        last_page = 0
        for p in sorted(pages):
            if p != last_page + 1: yield '...'
            yield p
            last_page = p
    d       = []
    for i in display():
        if i not in d:
            d.append(i)
        else:
            d.append(i*2)
    return {
        'total'  : n,
        'current': page,
        'pages'  : tuple(d)
        }


def cacl_punish_fee(info):
    ''' 计算滞纳金 '''
    amount   = info['amount']
    deadline = date_to_datetime(info['deadline'], format='%Y-%m-%d %H:%M:%S')
    if deadline<dt_obj.now() and info['status']==0:
        delta          = get_date_delta(str(deadline)[:19], str(dt_obj.now())[:19])
        for i in range(delta):
            info['punish'] = (info['amount']+ (info['punish'] or 0))/100.0
        info['punish'] = format_price(info['punish'])


def format_price(field):
    result = round(float(field), 2)
    if int(result)==result:
        result  = int(result)
    return result


def format_rate(field):
    return round(float(field), 1)


def get_date_delta(date, other_date):
    ''' 获取时间差 '''
    date_time  = date_to_datetime(date, format='%Y-%m-%d %H:%M:%S')
    other_time = date_to_datetime(other_date, format='%Y-%m-%d %H:%M:%S')

    return (other_time - date_time).days


def get_delayed_info(log):
    ''' 返回 是否逾期  逾期天数 '''
    delayed        = False
    delayed_days   = 0
    if log['repayment_time'] and log['repayment_time'] > log['deadline']:
        delayed    = True
        delayed_days = get_date_delta(log['deadline'], log['repayment_time'])
    elif log['status']==0 and log['deadline']<str(dt_obj.now()):
        delayed    = True
        delayed_days = get_date_delta(log['deadline'], str(dt_obj.now()))
    log['delayed'] = delayed
    log['delayed_days'] = delayed_days


def deadline_zh(deadline):
    orig_deadline = deadline
    deadline = add_months(deadline, -1)
    year   = deadline.year
    month  = deadline.month
    end  = dt_obj(year=year, month=month, day=1)-second_delta
    if month-1>=1:
        begin  = dt_obj(year=year, month=month-1, day=1)
    else:
        begin  = dt_obj(year=year-1, month=12, day=1)

    title = get_time_str_from_dt(deadline, '%Y年%m月帐单') + \
            get_time_str_from_dt(begin, '(%m.%d-') + get_time_str_from_dt(end, '%m.%d)')
    return title, get_time_str_from_dt(orig_deadline, '还款日截至%Y年%m月%d日')


def get_next_working_day(submit_time=None):
    ''' 下个工作日 '''
    if not submit_time:
        now     = dt_obj.now()
    else:
        now     = date_to_datetime(submit_time[:19], format='%Y-%m-%d %H:%M:%S')
    weekday = now.weekday()
    if weekday in [4, 5, 6]:
        return now+(7-weekday)*day_delta
    return now+day_delta



def md5_str(val, key='meifenfen'):
    result = hmac.new(key, val, hashlib.md5).hexdigest()
    return result


now = lambda : int(time.time())
def get_today_timestamp():
    now = dt_obj.now()
    year, month, day = now.year, now.month, now.day
    now = dt_obj(year=year, month=month, day=day)
    return int(time.mktime(now.timetuple()))


def delta_time_str(end_time, start_time=None):
    ''' 时间差字符串 '''
    if not start_time:
        start_time = dt_obj.now()
    if not end_time > start_time:
        return '已结束'
    delta       = end_time - start_time
    days        = delta.days
    hours       = delta.seconds / 3600
    minutes     = ( delta.seconds % 3600 ) / 60
    seconds     = ( delta.seconds % 3600 ) % 60
    return '{}天{}时{}分{}秒'.format(days, hours, minutes, seconds)


import re
url_pattern        = re.compile('http.*?.com/')
def get_img_key(full_url):
    return re.split(url_pattern, full_url)[1]


def translate_location(latlng=None):
    '''
    http://www.gpsspg.com/api/convert/latlng/
    0= WGS84 / GPS硬件 / Google Earth / Google Maps 卫星模式
    1= Google Maps 地图模式
    2= 百度地图坐标
    3= QQ腾讯地图坐标 / 高德地图坐标 / 阿里云地图坐标
    4= MapBar图吧地图坐标
    '''
    import requests
    import urllib
    data    = {
        'oid': '1753',
        'key': '64D8B0DF48E904DCEA7A264FC8811EAF',
        'from': '0',
        'to': '3',
        'latlng': latlng
        }
    params_str = urllib.urlencode(data)
    data       = requests.get('http://api.gpsspg.com/convert/latlng/?'+params_str)
    return data


def set_coupon_use_time(dailys):
    ''' 设置优惠券使用时间 '''
    now        = dt_obj.now()
    year       = now.year
    month      = now.month
    day        = now.day
    hour       = now.hour
    minute     = now.minute
    now        = dt_obj(year=year, month=month, day=day, hour=hour, minute=minute)

    for daily in dailys:
        assert daily.get('coupon'), '优惠券不存在'
        effective   = daily['coupon']['effective']
        start       = now
        end         = now + second_delta*effective
        daily['use_time_start'] = start
        daily['use_time_end']   = end
        daily['use_time']       = get_time_str_from_dt(start, '%-m.%-d') + '-' + get_time_str_from_dt(end, '%-m.%-d')


def convert_locaton(lnglat):
    ''' '''
    import requests
#     url = 'http://restapi.amap.com/rgeocode/simple?resType=json&encode=utf-8&range=3000&roadnum=0&crossnum=0&poinum=0&retvalue=1&sid=7001&region=&key=da03b0f06b056963d2f823d6ddffad6c' + lnglat
#     response = requests.get(url)
#     return response.json()
    lng, lat = lnglat.split(',')
    url = 'http://api.map.baidu.com/geocoder/v2/?ak=74136f02e6474fb72f3000e449e93c97&location='+lat+','+lng+'&output=json&pois=1'
    print url
    response = requests.get(url)
    return response.json()



def gen_redpack_billno():
    ''' 红包订单编号 '''
    now     = dt_obj.now()
    prefix  = get_time_str_from_dt(now, '%Y%m%d')
    return prefix + random_no(randomlength=10)


def random_redpack_price():
    val     = int(random.random()*100)/10.0
    if val<1: val += 1
    if val>5: val -= 5
    return max(1, format_price(val))


def imgs_to_list(pics):
    ''' '''
    str_list    = (pics or '').split(',')
    length      = len(str_list)
    if length<4:
        for i in range(4-length):
            str_list.append('')
    return str_list



