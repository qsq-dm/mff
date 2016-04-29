# -*- coding: utf-8 -*-


from thirdparty.qn import upload_img



def login_xuexin(username, passwd):
    ''' 抓取学信网数据 '''
    link    = 'https://account.chsi.com.cn/passport/login'
    import requests
    from lxml import html
    import urllib
    payload = {
        'username': username,
        'password': passwd,
    }
    response = None
    success  = False
    return_captcha = False
    try:
        with requests.Session() as session:
            print session.cookies
            r   = session.get('https://account.chsi.com.cn/passport/login')
            tree= html.fromstring(r.text)
            _lt = tree.xpath('//*[@id="fm1"]/input[1]')[0].value
            print _lt, 'lt'
            payload['lt']       = _lt
            payload['_eventId'] = 'submit'
            payload['submit']   = '登录'

            headers = {
                'content-type': 'application/x-www-form-urlencoded'
                }
            print urllib.urlencode(payload)
            data = urllib.urlencode(payload)
            p   = session.post(link, data=payload, headers=headers)
            print 'logged in'
            response = session.get('http://my.chsi.com.cn/archive/xjarchive.action')
            tree            = html.fromstring(response.text)
            table           = tree.xpath('//*[@id="resultTable"]')[0]
            enroll_time     = tree.xpath('//*[@id="resultTable"]/table/tr[9]/td[2]')[0].text.strip()
            grade           = tree.xpath('//*[@id="resultTable"]/table/tr[7]/td[2]')[0].text.strip()
            graduate_time   = tree.xpath('//*[@id="resultTable"]/table/tr[10]/td[2]')[0].text.strip()
            birth_day       = tree.xpath('//*[@id="resultTable"]/table/tr[3]/td[1]')[0].text.strip()
            school          = tree.xpath('//*[@id="resultTable"]/table/tr[5]/td[1]')[0].text.strip()
            name            = tree.xpath('//*[@id="resultTable"]/table/tr[1]/td[1]')[0].text.strip()
            sex             = tree.xpath('//*[@id="resultTable"]/table/tr[2]/td[1]')[0].text.strip()
            years           = tree.xpath('//*[@id="resultTable"]/table/tr[8]/td[1]')[0].text.strip()
            major           = tree.xpath('//*[@id="resultTable"]/table/tr[6]/td[2]')[0].text.strip()
            id_no           = tree.xpath('//*[@id="resultTable"]/table/tr[3]/td[2]')[0].text.strip()
            #print table.text_content()
            print '姓名',          name
            print '性别',          sex
            print '身份证号',       id_no
            print '学校',          school
            print '学制',          years
            print '学历',          grade
            print '入学时间',       enroll_time
            print '毕业时间',       graduate_time
            print '出生日期',       birth_day
            print '专业',          major
    
            result  = {
                'name'          : name,
                'sex'           : sex,
                'school'        : school,
                'years'         : years,
                'grade'         : grade,
                'enroll_time'   : enroll_time,
                'graduate_time' : graduate_time,
                'birth_day'     : birth_day,
                'major'         : major,
                'id_no'         : id_no
                }
            success = True
            return result, success, return_captcha, session

    except Exception as e:
        import traceback
        traceback.print_exc()
        img_res     = session.get('https://account.chsi.com.cn/passport/captcha.image')
        #return img_res
        print img_res.status_code, len(img_res.content)
        captcha_img = img_res.content
        import time
        key = str(time.time())+'.jpg'
        print 'key', key
        upload_img(key, captcha_img)
        success         = False
        return_captcha  = True
        return key, success, return_captcha, session


import urllib
from lxml import html
def get_chsi_info(username, passwd, captcha, session):
    payload = {
        'username': username,
        'password': passwd,
    }
    print session.cookies
    r   = session.get('https://account.chsi.com.cn/passport/login')
    tree= html.fromstring(r.text)
    _lt = tree.xpath('//*[@id="fm1"]/input[1]')[0].value
    print _lt, 'lt'
    payload['lt']       = _lt
    payload['_eventId'] = 'submit'
    payload['submit']   = '登录'
    payload['captcha']  = captcha
    headers = {
        'content-type': 'application/x-www-form-urlencoded'
        }
    print urllib.urlencode(payload)
    data = urllib.urlencode(payload)
    link = 'https://account.chsi.com.cn/passport/login'
    p   = session.post(link, data=payload, headers=headers)
    response = session.get('http://my.chsi.com.cn/archive/xjarchive.action')
    tree            = html.fromstring(response.text)
    table           = tree.xpath('//*[@id="resultTable"]')[0]
    enroll_time     = tree.xpath('//*[@id="resultTable"]/table/tr[9]/td[2]')[0].text.strip()
    grade           = tree.xpath('//*[@id="resultTable"]/table/tr[7]/td[2]')[0].text.strip()
    graduate_time   = tree.xpath('//*[@id="resultTable"]/table/tr[10]/td[2]')[0].text.strip()
    birth_day       = tree.xpath('//*[@id="resultTable"]/table/tr[3]/td[1]')[0].text.strip()
    school          = tree.xpath('//*[@id="resultTable"]/table/tr[5]/td[1]')[0].text.strip()
    name            = tree.xpath('//*[@id="resultTable"]/table/tr[1]/td[1]')[0].text.strip()
    sex             = tree.xpath('//*[@id="resultTable"]/table/tr[2]/td[1]')[0].text.strip()
    years           = tree.xpath('//*[@id="resultTable"]/table/tr[8]/td[1]')[0].text.strip()
    major           = tree.xpath('//*[@id="resultTable"]/table/tr[6]/td[2]')[0].text.strip()
    id_no           = tree.xpath('//*[@id="resultTable"]/table/tr[3]/td[2]')[0].text.strip()
    #print table.text_content()
    print '姓名',          name
    print '性别',          sex
    print '身份证号',       id_no
    print '学校',          school
    print '学制',          years
    print '学历',          grade
    print '入学时间',       enroll_time
    print '毕业时间',       graduate_time
    print '出生日期',       birth_day
    print '专业',          major

    result  = {
        'name'          : name,
        'sex'           : sex,
        'school'        : school,
        'years'         : years,
        'grade'         : grade,
        'enroll_time'   : enroll_time,
        'graduate_time' : graduate_time,
        'birth_day'     : birth_day,
        'major'         : major,
        'id_no'         : id_no
        }
    return result


def refresh_chsi_captcha(session):
    img_res     = session.get('https://account.chsi.com.cn/passport/captcha.image')
    captcha_img = img_res.content
    import time
    key = str(time.time())+'.jpg'
    print 'key', key
    upload_img(key, captcha_img)
    return key
