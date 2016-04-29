# -*- coding: utf-8 -*-
import time

from qiniu import Auth
from qiniu import put_data


ONE_DAY_SECOND = 86400*30
AK = 'FwH58jaCU_l7npqyNLn6cQYlvdfMbijwNOP4P8D4'
SK = 'zfDKpDPGLAAWN48v6lJOIWewTK3gKCuIwmj69Co_'

q  = Auth(AK, SK)

bucket_name = 'meifenfen'


def gen_qn_token():
    token = q.upload_token(bucket_name, expires=ONE_DAY_SECOND)
    return  token

def gen_backup_token():
    token = q.upload_token('backup', expires=ONE_DAY_SECOND)
    return  token


def upload_img(key, content):
    token = gen_qn_token();
    ret, info = put_data(token, key, content, mime_type="application/octet-stream", check_crc=True)
    assert info.status_code==200, '上传图片失败'
    return key


def backup_db():
    ''' 备份mysql '''
    import time
    import os
    from datetime import datetime
    while True:
        now   = datetime.now()
        year  = now.year
        month = now.month
        day   = now.day
        hour  = now.hour
        minute= now.minute
        token = gen_backup_token(); print token
        time_str = 'mysql_backup_{}-{}-{}-{}-{}.sql'.format(year, month, day, hour, minute)
        os.system('mysqldump -u root  main > main.sql')
        print 'backing up...', time_str
        with open('main.sql', 'rb') as f:
            content = f.read()
            print put_data(token, time_str, content, check_crc=True)
        time.sleep(60*60)
        if hour==3 and 0<minute<6: #每天凌晨三点删除多余的备份
            list_qniufile()


def list_qniufile():
    ''' '''
    from settings import IMAGE_HOST_URL_DOMAIN
    from thirdparty.qn import q
    from datetime   import datetime
    from util.utils import date_to_datetime
    from util.utils import day_delta
    RESOURCE_HOST = 'rs.qiniu.com'
    now         = datetime.now()
    import requests
    url_query   = '/list?bucket=backup&prefix=mysql'
    q.token(url_query)
    print q.token(url_query)
    import requests
    headers = {
        'Host': 'rsf.qbox.me',
        'content-type': 'application/x-www-form-urlencoded',
        'Authorization': 'QBox {}'.format(q.token(url_query+'\n'))
    }
    print headers
    request_url = 'http://{}{}'.format(RESOURCE_HOST, url_query)
    print request_url
    response    = requests.get(request_url, headers=headers)
    if response.status_code!=200:
        print '状态异常'
    else:
        for i in response.json()['items']:
            date_str    = i['key'][13:23]
            time_d      = date_to_datetime(date_str)
            print i['key'], time_d, time_d<now-1*day_delta
            if time_d<now-1*day_delta:
                remove_img('backup', i['key'])


def remove_img(bucket_name, key):
    '''
    该请求无须设置任何参数
    http://developer.qiniu.com/docs/v6/api/reference/rs/delete.html#delete-request-params
    '''
    from qiniu.utils import urlsafe_base64_encode
    entry           = '{}:{}'.format(bucket_name, key)
    RESOURCE_HOST   = 'rs.qiniu.com'
    encoded         = urlsafe_base64_encode(entry)
    url_query       = '/delete/' + encoded
    q.token(url_query)
    import requests
    headers = {
        'Authorization': 'QBox {}'.format(q.token(url_query+'\n'))
    }
    request_url = 'http://{}{}'.format(RESOURCE_HOST, url_query)
    response    = requests.post(request_url, headers=headers)
    if response.status_code==200:
        print '删除成功'
    else:
        print response.status_code, '删除失败'


if __name__ == '__main__':
    with open('static/test.jpg', 'rb') as f:
        content = f.read()
    token = gen_qn_token(); print token
    ret, info = put_data(token, str(time.time()), content, mime_type="application/octet-stream", check_crc=True)
    print ret, info