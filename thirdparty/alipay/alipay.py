#coding=utf-8

import rsa
import types
import random
import base64
import urllib
import urllib2
import hashlib
from urllib import urlencode, urlopen, quote

from thirdparty.alipay import config

settings    = config.settings



def smart_str(s, encoding='utf-8', strings_only=False, errors='strict'):
    '''
    Returns a bytestring version of 's', encoded as specified in 'encoding'.
    If strings_only is True, don't convert (some) non-string-like objects.

    '''
    if strings_only and isinstance(s, (types.NoneType, int)):
        return s
    if not isinstance(s, basestring):
        try:
            return str(s)
        except UnicodeEncodeError:
            if isinstance(s, Exception):
                # An Exception subclass containing non-ASCII data that doesn't
                # know how to print itself properly. We shouldn't raise a
                # further exception.
                return ' '.join([smart_str(arg, encoding, strings_only,
                        errors) for arg in s])
            return unicode(s).encode(encoding, errors)
    elif isinstance(s, unicode):
        return s.encode(encoding, errors)
    elif s and encoding != 'utf-8':
        return s.decode('utf-8', errors).encode(encoding, errors)
    else:
        return s


#对数组排序并除去数组中的空值和签名参数 返回数组和链接串
def params_filter(params):
    ks = params.keys()
    ks.sort()
    newparams = {}
    prestr = ''
    for k in ks:
        v = params[k]
        k = smart_str(k, settings.ALIPAY_INPUT_CHARSET)
        if k not in ('sign', 'sign_type') and v != '':
            newparams[k] = smart_str(v, settings.ALIPAY_INPUT_CHARSET)
            prestr += '%s="%s"&' % (k, newparams[k])
    prestr = prestr[:-1]

    return newparams, prestr


def params_filter_web(params):
    ks = params.keys()
    ks.sort()
    newparams = {}
    prestr = ''
    for k in ks:
        v = params[k]
        k = smart_str(k, settings.ALIPAY_INPUT_CHARSET)
        if k not in ('sign', 'sign_type') and v != '':
            newparams[k] = smart_str(v, settings.ALIPAY_INPUT_CHARSET)
            prestr += '%s=%s&' % (k, newparams[k])
    prestr = prestr[:-1]
    return newparams, prestr


def params_sign_md5(prestr, key):
    return hashlib.md5(prestr+key).hexdigest()


def params_sign_rsa(data):
    with open('thirdparty/alipay/rsa_private_key.pem') as privatefile:
        p = privatefile.read()
        privkey = rsa.PrivateKey.load_pkcs1(p)

    signature = rsa.sign(data, privkey, 'SHA-1')
    signature_encode = quote(base64.b64encode(signature),'')
    return signature_encode

# def params_sign_0(data):
#     key = RSA.importKey(settings.PRIVATE_KEY)
#     h = SHA.new(data)
#     signer = PKCS1_v1_5.new(key)
#     signature = signer.sign(h)
#     return base64.b64encode(signature)

# def params_sign_1(data):
#     key = load_privatekey(FILETYPE_PEM, open("alipay/rsa_private_key.pem").read())
#     d =  sign(key, data, 'sha1')  #d为经过SHA1算法进行摘要、使用私钥进行签名之后的数据  
#     b = base64.b64encode(d)  #将d转换为BASE64的格式
#     return b

def params_decrypt(data):
    with open('thirdparty/alipay/rsa_private_key.pem') as privatefile:
        p = privatefile.read()
        privkey = rsa.PrivateKey.load_pkcs1(p)
    res_data = rsa.decrypt(base64.b64decode(data), privkey)
    return res_data

def params_verify(data, signature):
    with open('thirdparty/alipay/alipay_public_key.pem') as publicfile:
        p = publicfile.read()
        publickey = rsa.PublicKey.load_pkcs1_openssl_pem(p)
    res = rsa.verify(data,base64.b64decode(signature),publickey)
    return res 

# 即时到账交易接口
def mobile_sdk_pay(tn, subject, body, total_fee, notify_url=settings.ALIPAY_NOTIFY_URL):
    params = {}
    params['service']       = 'mobile.securitypay.pay'
    # 获取配置文件
    params['partner']           = settings.ALIPAY_PARTNER
    params['notify_url']        = quote(notify_url,'')
    params['_input_charset']    = settings.ALIPAY_INPUT_CHARSET
    params['seller_id']         = settings.ALIPAY_SELLER_EMAIL #卖家支付宝账号
    # 从订单数据中动态获取到的必填参数
    params['out_trade_no']  = tn        # 订单号
    params['subject']       = subject   # 订单名称，显示在支付宝收银台里的“商品名称”里，显示在支付宝的交易管理的“商品名称”的列表里。
    params['payment_type']  = '1'
    params['body']          = body      # 订单描述、订单详细、订单备注，显示在支付宝收银台里的“商品描述”里
    params['total_fee']     = total_fee # 订单总金额，显示在支付宝收银台里的“应付总额”里
    
    params, prestr = params_filter(params)
    
    params['sign'] = params_sign_rsa(prestr)
    params['sign_type'] = settings.ALIPAY_SIGN_TYPE

    prestr = prestr + '&sign="%s"'%params['sign'] + '&sign_type="%s"'%params['sign_type']
    print prestr," prestr\n"
    return prestr

def mobile_sdk_repayment(tn, subject, body, total_fee, notify_url=settings.ALIPAY_REPAYMENT_NOTIFY_URL):
    ''' 还款参数 '''
    return mobile_sdk_pay(tn, subject, body, total_fee, notify_url)


def mobile_web_pay(tn, subject, body, total_fee):
    params = {}
    params['service']           = 'alipay.wap.trade.create.direct'
    # 获取配置文件
    params['partner']           = settings.ALIPAY_PARTNER
    params['format']            = 'xml'
    params['v']                 = '2.0'
    params['req_id']            = tn   #请求号
    params['sec_id']            = 'MD5'
    params['_input_charset']    = settings.ALIPAY_INPUT_CHARSET

    params['req_data']          = "<direct_trade_create_req><notify_url>" + settings.ALIPAY_NOTIFY_URL + "</notify_url><call_back_url>" + settings.ALIPAY_RETURN_URL + "</call_back_url><seller_account_name>" + settings.ALIPAY_SELLER_EMAIL + "</seller_account_name><out_trade_no>" + tn + "</out_trade_no><subject>" + subject + "</subject><total_fee>" + str(total_fee) + "</total_fee><merchant_url>" + settings.ALIPAY_RETURN_URL + "</merchant_url></direct_trade_create_req>";

    params['subject']             = subject  # 订单名称，显示在支付宝收银台里的“商品名称”里，显示在支付宝的交易管理的“商品名称”的列表里。
    params['out_trade_no']        = tn        # 订单号
    params['total_fee']           = total_fee # 订单总金额，显示在支付宝收银台里的“应付总额”里
    params['seller_account_name'] = settings.ALIPAY_SELLER_EMAIL
    params['seller_email']        = settings.ALIPAY_SELLER_EMAIL
    #params['call_back_url']       = 'http://restapi.meiya.me/alipay/web/CallBack'
    params['call_back_url']       = 'http://xtestapi.meiya.me/alipay/web/success/CallBack'
    params['notify_url']          = settings.ALIPAY_NOTIFY_URL
    #params['merchant_url']        = settings.ALIPAY_RETURN_URL
    params['pay_expire']          = '300'
   
    params, prestr = params_filter_web(params)
    params['sign'] = params_sign_md5(prestr, settings.ALIPAY_KEY)
    
    params_data = urllib.urlencode(params)
    request = urllib2.Request(url=settings.WEB_GATEWAY, data=params_data)
    result_data = urllib2.urlopen(request)
    result = result_data.read()
    result = urllib.unquote(result).decode('utf8')
    res_data = result.split('>')
    print result
    request_token = ''
    for s in res_data:
        if '</request_token' in s:
            request_token = s.split('<')[0]
    if request_token:
        params['req_data'] = '<auth_and_execute_req><request_token>' + request_token + '</request_token></auth_and_execute_req>'
        params['request_token'] = request_token
        params['service'] = 'alipay.wap.auth.authAndExecute'
        params, prestr = params_filter_web(params)   
        params['sign'] = params_sign_md5(prestr, settings.ALIPAY_KEY)
        url = settings.WEB_GATEWAY + prestr + '&sign=%s'%params['sign']
        return url
    else:
        return ''


def notify_verify(post, payment_type=None):
    if payment_type==4:
        params, prestr = params_filter(post)
        mysign = params_sign_rsa(prestr)
        if mysign != post.get('sign'):
            return False
    if payment_type==16:
        params, prestr = params_filter_web(post)
        mysign = params_sign_md5(prestr, settings.ALIPAY_KEY)
        if mysign != post.get('sign'):
            return False
    # 二级验证--查询支付宝服务器此条信息是否有效
    params = {}
    params['partner'] = settings.ALIPAY_PARTNER
    params['notify_id'] = post.get('notify_id')
    if settings.ALIPAY_TRANSPORT == 'https':
        params['service'] = 'notify_verify'
        gateway = 'https://mapi.alipay.com/gateway.do'
    else:
        gateway = 'http://notify.alipay.com/trade/notify_query.do'
    veryfy_result = urlopen(gateway, urlencode(params)).read()
    if veryfy_result.lower().strip() == 'true':
        return True

    return False


def get_batch_no():
    from util.utils import dt_obj
    from util.utils import random_no
    current_time    = dt_obj.now()
    from util.utils import get_time_str_from_dt
    return get_time_str_from_dt(current_time, '%Y%m%d') + random_no()


def gen_format_detail(data, reason):
    ''' '2016010521001004850065282281^0.02^美分分退款
        refund_order({'2016010521001004850065282281':'0.02'}, '美分分退款')
    '''
    result    = []
    for order_no in data:
        fee       = data[order_no]
        result.append('{}^{}^{}'.format(order_no, fee, reason))
    return '#'.join(result)

'''
文档链接：
https://doc.open.alipay.com/doc2/detail.htm?spm=0.0.0.0.bHVaSg&treeId=66&articleId=103600&docType=1
https://mapi.alipay.com/gateway.do?seller_email=Jier1105%40alitest.com&batch_num=1&refund_date=2011-01-12+11%3A21%3A00&notify_url=http%3A%2F%2Fapi.test.alipay.net%2Fatinterface%2Freceive_notify.htm&sign=9b3426cac65d36f64bffbfbc6ce50549&service=refund_fastpay_by_platform_pwd&partner=2088101008267254&detail_data=2011011201037066%5E5.00%5E%D0%AD%C9%CC%CD%CB%BF%EE&sign_type=MD5&batch_no=201101120001
'''
from util.utils import dt_obj
import urllib
def refund_order(refund_data, reason):
    data    = {
        'service': 'refund_fastpay_by_platform_pwd',
        'partner': settings.ALIPAY_PARTNER,
        '_input_charset': 'utf-8',
        'sign_type': 'MD5',
        'notify_url': '',
        'seller_email': 'zhaohh@meifenfen.com',
        'seller_user_id': settings.ALIPAY_PARTNER,
        'refund_date': str(dt_obj.now())[:19],
        'batch_no': get_batch_no(),
        'batch_num': '1',
        'detail_data': gen_format_detail(refund_data, reason)
        }
    params, prestr = params_filter_web(data)   
    params['sign'] = params_sign_md5(prestr, settings.ALIPAY_KEY)
    print params
    return 'https://mapi.alipay.com/gateway.do?'+urllib.urlencode(params)


def test_demo():
    ''' '''
    tn = '0819145412-' + str(random.randint(1000, 9999))
    subject = '拉拉啊拉拉阿拉'
    body = 'd司机好吧司机呢'
    total_fee = '0.01'
    return mobile_web_pay(tn, subject, body, total_fee)


if __name__=='__main__':
    tn = '0819145412-' + str(random.randint(1000, 9999))
    subject = '拉拉啊拉拉阿拉'
    body = 'd司机好吧司机呢'
    total_fee = '0.01'
    mobile_web_pay(tn, subject, body, total_fee)
    # url = mobile_web_order_pay(tn, subject, body, total_fee)
    
 
