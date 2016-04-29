#coding:utf-8
"""
pay_api:https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=2_1
Created on 2014-11-24
@author: http://blog.csdn.net/yueguanghaidao,yihaibo@longtugame.com
 * 微信支付帮助库
 * ====================================================
 * 接口分三种类型：
 * 【请求型接口】--Wxpay_client_
 *      统一支付接口类--UnifiedOrder
 *      订单查询接口--OrderQuery
 *      退款申请接口--Refund
 *      退款查询接口--RefundQuery
 *      对账单接口--DownloadBill
 *      短链接转换接口--ShortUrl
 * 【响应型接口】--Wxpay_server_
 *      通用通知接口--Notify
 *      Native支付——请求商家获取商品信息接口--NativeCall
 * 【其他】
 *      静态链接二维码--NativeLink
 *      JSAPI支付--JsApi
 * =====================================================
 * 【CommonUtil】常用工具：
 *      trimString()，设置参数时需要用到的字符处理函数
 *      createNoncestr()，产生随机字符串，不长于32位
 *      formatBizQueryParaMap(),格式化参数，签名过程需要用到
 *      getSign(),生成签名
 *      arrayToXml(),array转xml
 *      xmlToArray(),xml转 array
 *      postXmlCurl(),以post方式提交xml到对应的接口url
 *      postXmlSSLCurl(),使用证书，以post方式提交xml到对应的接口url
"""
import os
import json
import time
import random
import urllib2
import hashlib
import threading
from urllib import quote
import xml.etree.ElementTree as ET
from settings import BASE_DIR

from thirdparty.wechat import wechat
from settings import SERVER_NAME
from settings import WECHAT_CERT_PEM
from settings import WECHAT_KEY_PEM
from settings import WECHAT_KEY
from settings import WECHAT_MCHID
from settings import WECHAT_APP_ID
from settings import WECHAT_APP_SECRET
from settings import WX_PAY_NOTIFY_URL
from settings import WX_REPAYMENT_NOTIFY_URL
from settings import WX_REDPACK_NOTIFY_URL


try:
    import pycurl
    from cStringIO import StringIO
except ImportError:
    pycurl = None


class WxPayConf_pub(object):
    """配置账号信息"""

    #=======【基本信息设置】=====================================
    #微信公众号身份的唯一标识。审核通过后，在微信发送的邮件中查看
    APPID       = WECHAT_APP_ID
    APPSECRET   = WECHAT_APP_SECRET
    #受理商ID，身份标识
    MCHID       = WECHAT_MCHID
    #商户支付密钥Key。审核通过后，在微信发送的邮件中查看
    KEY         = WECHAT_KEY
   

    #=======【异步通知url设置】===================================
    #异步通知url，商户根据实际开发过程设定
    NOTIFY_URL = WX_PAY_NOTIFY_URL

    #=======【JSAPI路径设置】===================================
    #获取access_token过程中的跳转uri，通过跳转将code传入jsapi支付页面
    JS_API_CALL_URL = "http://{}/user/?showwxpaytitle=1".format(SERVER_NAME)

    #=======【证书路径设置】=====================================
    #证书路径,注意应该填写绝对路径
    SSLCERT_PATH = BASE_DIR+"/thirdparty/" + WECHAT_CERT_PEM
    SSLKEY_PATH =  BASE_DIR+"/thirdparty/" + WECHAT_KEY_PEM

    #=======【curl超时设置】===================================
    CURL_TIMEOUT = 30

    #=======【HTTP客户端设置】===================================
    HTTP_CLIENT = "CURL"  # ("URLLIB", "CURL")


class Singleton(object):
    """单例模式"""

    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with cls._instance_lock:
                if not hasattr(cls, "_instance"):
                    impl = cls.configure() if hasattr(cls, "configure") else cls
                    instance = super(Singleton, cls).__new__(impl, *args, **kwargs)
                    if not isinstance(instance, cls):
                        instance.__init__(*args, **kwargs)
                    cls._instance = instance
        return cls._instance


class UrllibClient(object):
    """使用urlib2发送请求"""

    def get(self, url, second=30):
        return self.postXml(None, url, second)

    def postXml(self, xml, url, second=30):
        """不使用证书"""
        data = urllib2.urlopen(url, xml, timeout=second).read()
        return data

    def postXmlSSL(self, xml, url, second=30):
        """使用证书"""
        raise TypeError("please use CurlClient")


class CurlClient(object):
    """使用Curl发送请求"""
    def __init__(self):
        self.curl = pycurl.Curl()
        self.curl.setopt(pycurl.SSL_VERIFYHOST, False)
        self.curl.setopt(pycurl.SSL_VERIFYPEER, False)
        #设置不输出header
        self.curl.setopt(pycurl.HEADER, False)

    def get(self, url, second=30):
        return self.postXmlSSL(None, url, second=second, cert=False, post=False)

    def postXml(self, xml, url, second=30):
        """不使用证书"""
        return self.postXmlSSL(xml, url, second=second, cert=False, post=True)
        

    def postXmlSSL(self, xml, url, second=30, cert=True, post=True):
        """使用证书"""
        self.curl.setopt(pycurl.URL, url)
        self.curl.setopt(pycurl.TIMEOUT, second)
        #设置证书
        #使用证书：cert 与 key 分别属于两个.pem文件
        #默认格式为PEM，可以注释
        print WxPayConf_pub.SSLCERT_PATH
        if cert:
            self.curl.setopt(pycurl.SSLKEYTYPE, "PEM")
            self.curl.setopt(pycurl.SSLKEY, WxPayConf_pub.SSLKEY_PATH)
            self.curl.setopt(pycurl.SSLCERTTYPE, "PEM")
            self.curl.setopt(pycurl.SSLCERT, WxPayConf_pub.SSLCERT_PATH)
        #post提交方式
        if post:
            self.curl.setopt(pycurl.POST, True)
            self.curl.setopt(pycurl.POSTFIELDS, xml)
        buff = StringIO()
        self.curl.setopt(pycurl.WRITEFUNCTION, buff.write)

        self.curl.perform()
        return buff.getvalue()


class HttpClient(Singleton):
    @classmethod
    def configure(cls):
        if pycurl is not None and WxPayConf_pub.HTTP_CLIENT != "URLLIB":
            return CurlClient
        else:
            return UrllibClient
            

class Common_util_pub(object):
    """所有接口的基类"""

    def trimString(self, value):
        if value is not None and len(value) == 0:
            value = None
        return value

    def createNoncestr(self, length = 32):
        """产生随机字符串，不长于32位"""
        chars = "abcdefghijklmnopqrstuvwxyz0123456789"
        strs = []
        for x in range(length):
            strs.append(chars[random.randrange(0, len(chars))])
        return "".join(strs)

    def formatBizQueryParaMap(self, paraMap, urlencode):
        """格式化参数，签名过程需要使用"""
        slist = sorted(paraMap)
        buff = []
        for k in slist:
            v = quote(paraMap[k]) if urlencode else paraMap[k]
            buff.append("{0}={1}".format(k, v))

        return "&".join(buff)

    def getSign(self, obj):
        """生成签名"""
        #签名步骤一：按字典序排序参数,formatBizQueryParaMap已做
        String = self.formatBizQueryParaMap(obj, False)
        #签名步骤二：在string后加入KEY
        String = "{0}&key={1}".format(String,WxPayConf_pub.KEY)
        #签名步骤三：MD5加密
        String = hashlib.md5(String).hexdigest()
        #签名步骤四：所有字符转为大写
        result_ = String.upper()
        return result_

    def arrayToXml(self, arr):
        """array转xml"""
        xml = ["<xml>"]
        for k, v in arr.iteritems():
            if v.isdigit():
                xml.append("<{0}>{1}</{0}>".format(k, v))
            else:
                xml.append("<{0}><![CDATA[{1}]]></{0}>".format(k, v))
        xml.append("</xml>")
        return "".join(xml)

    def xmlToArray(self, xml):
        """将xml转为array"""
        array_data = {}
        root = ET.fromstring(xml)
        for child in root:
            value = child.text
            array_data[child.tag] = value
        return array_data

    def postXmlCurl(self, xml, url, second=30):
        """以post方式提交xml到对应的接口url"""
        return HttpClient().postXml(xml, url, second=second)

    def postXmlSSLCurl(self, xml, url, second=30):
        """使用证书，以post方式提交xml到对应的接口url"""
        return CurlClient().postXmlSSL(xml, url, second=second)


class JsApi_pub(Common_util_pub):
    """JSAPI支付——H5网页端调起支付接口"""
    code = None    #code码，用以获取openid
    openid = None  #用户的openid
    parameters = None  #jsapi参数，格式为json
    prepay_id = None #使用统一支付接口得到的预支付id
    curl_timeout = None #curl超时时间

    def __init__(self, timeout=WxPayConf_pub.CURL_TIMEOUT):
        self.curl_timeout = timeout

    def createOauthUrlForCode(self, redirectUrl):
        """生成可以获得code的url"""
        urlObj = {}
        urlObj["appid"] = WxPayConf_pub.APPID
        urlObj["redirect_uri"] = redirectUrl
        urlObj["response_type"] = "code"
        urlObj["scope"] = "snsapi_base"
        urlObj["state"] = "STATE#wechat_redirect"
        bizString = self.formatBizQueryParaMap(urlObj, False)
        return "https://open.weixin.qq.com/connect/oauth2/authorize?"+bizString

    def createOauthUrlForOpenid(self):
        """生成可以获得openid的url"""
        urlObj = {}
        urlObj["appid"] = WxPayConf_pub.APPID
        urlObj["secret"] = WxPayConf_pub.APPSECRET
        urlObj["code"] = self.code
        urlObj["grant_type"] = "authorization_code"
        bizString = self.formatBizQueryParaMap(urlObj, False)
        return "https://api.weixin.qq.com/sns/oauth2/access_token?"+bizString

    def getOpenid(self):
        """通过curl向微信提交code，以获取openid"""
        url = self.createOauthUrlForOpenid()
        data = HttpClient().get(url)
        self.openid = json.loads(data)["openid"]
        return self.openid
        
    
    def setPrepayId(self, prepayId):
        """设置prepay_id"""
        self.prepay_id = prepayId

    def setCode(self, code):
        """设置code"""
        self.code = code

    def  getParameters(self):
        """设置jsapi的参数"""
        jsApiObj = {}
        jsApiObj["appId"] = WxPayConf_pub.APPID
        timeStamp = int(time.time())
        jsApiObj["timeStamp"] = "{0}".format(timeStamp)
        jsApiObj["nonceStr"] = self.createNoncestr()
        jsApiObj["package"] = "prepay_id={0}".format(self.prepay_id)
        jsApiObj["signType"] = "MD5"
        jsApiObj["paySign"] = self.getSign(jsApiObj)
        self.parameters = json.dumps(jsApiObj)

        return self.parameters


class Wxpay_client_pub(Common_util_pub):
    """请求型接口的基类"""
    response = None  #微信返回的响应
    url = None       #接口链接
    curl_timeout = None #curl超时时间

    def __init__(self):
        self.parameters = {} #请求参数，类型为关联数组
        self.result = {}     #返回参数，类型为关联数组


    def setParameter(self, parameter, parameterValue):
        """设置请求参数"""
        self.parameters[self.trimString(parameter)] = self.trimString(parameterValue)

    def createXml(self):
        """设置标配的请求参数，生成签名，生成接口参数xml"""
        self.parameters["appid"] = WxPayConf_pub.APPID   #公众账号ID
        self.parameters["mch_id"] = WxPayConf_pub.MCHID   #商户号
        self.parameters["nonce_str"] = self.createNoncestr()   #随机字符串
        self.parameters["sign"] = self.getSign(self.parameters)   #签名
        return  self.arrayToXml(self.parameters)

    def postXml(self):
        """post请求xml"""
        xml = self.createXml()
        self.response = self.postXmlCurl(xml, self.url, self.curl_timeout)
        return self.response

    def postXmlSSL(self):
        """使用证书post请求xml"""
        xml = self.createXml()
        self.response = self.postXmlSSLCurl(xml, self.url, self.curl_timeout)
        return self.response

    def getResult(self):
        """获取结果，默认不使用证书"""
        self.postXml()
        self.result = self.xmlToArray(self.response)
        return self.result


class UnifiedOrder_pub(Wxpay_client_pub):
    """统一支付接口类"""

    def __init__(self, timeout=WxPayConf_pub.CURL_TIMEOUT):
        #设置接口链接
        self.url = "https://api.mch.weixin.qq.com/pay/unifiedorder"
        #设置curl超时时间
        self.curl_timeout = timeout
        super(UnifiedOrder_pub, self).__init__()


    def createXml(self):
        """生成接口参数xml"""
        #检测必填参数
        if any(self.parameters[key] is None for key in ("out_trade_no", "body", "total_fee", "notify_url", "trade_type")):
            raise ValueError("missing parameter")
        if self.parameters["trade_type"] == "JSAPI" and self.parameters["openid"] is None:
            raise ValueError("JSAPI need openid parameters")

        self.parameters["appid"] = WxPayConf_pub.APPID  #公众账号ID
        self.parameters["mch_id"] = WxPayConf_pub.MCHID  #商户号
        self.parameters["spbill_create_ip"] = "127.0.0.1"  #终端ip      
        self.parameters["nonce_str"] = self.createNoncestr()  #随机字符串
        self.parameters["sign"] = self.getSign(self.parameters)  #签名
        return  self.arrayToXml(self.parameters)

    def getPrepayId(self):
        """获取prepay_id"""
        self.postXml()
        self.result = self.xmlToArray(self.response)
        print self.result
        if self.result.has_key('prepay_id'):
            prepay_id = self.result["prepay_id"]
            return prepay_id
        return ''


class OrderQuery_pub(Wxpay_client_pub):
    """订单查询接口"""

    def __init__(self, timeout=WxPayConf_pub.CURL_TIMEOUT):
        #设置接口链接
        self.url = "https://api.mch.weixin.qq.com/pay/orderquery"
        #设置curl超时时间
        self.curl_timeout = timeout
        super(OrderQuery_pub, self).__init__()

    def createXml(self):
        """生成接口参数xml"""

        #检测必填参数
        if any(self.parameters[key] is None for key in ("out_trade_no", "transaction_id")):
            raise ValueError("missing parameter")

        self.parameters["appid"] = WxPayConf_pub.APPID  #公众账号ID
        self.parameters["mch_id"] = WxPayConf_pub.MCHID  #商户号
        self.parameters["nonce_str"] = self.createNoncestr()  #随机字符串
        self.parameters["sign"] = self.getSign(self.parameters)  #签名
        return  self.arrayToXml(self.parameters)


class Refund_pub(Wxpay_client_pub):
    """退款申请接口"""

    def __init__(self, timeout=WxPayConf_pub.CURL_TIMEOUT):
        #设置接口链接
        self.url = "https://api.mch.weixin.qq.com/secapi/pay/refund"
        #设置curl超时时间
        self.curl_timeout = timeout
        super(Refund_pub, self).__init__()

    def createXml(self):
        """生成接口参数xml"""
        if any(self.parameters[key] is None for key in ("out_trade_no", "out_refund_no", "total_fee", "refund_fee", "op_user_id")):
            raise ValueError("missing parameter")

        self.parameters["appid"] = WxPayConf_pub.APPID  #公众账号ID
        self.parameters["mch_id"] = WxPayConf_pub.MCHID  #商户号
        self.parameters["nonce_str"] = self.createNoncestr()  #随机字符串
        self.parameters["sign"] = self.getSign(self.parameters)  #签名
        return  self.arrayToXml(self.parameters)

    def getResult(self):
        """ 获取结果，使用证书通信(需要双向证书)"""
        self.postXmlSSL()
        self.result = self.xmlToArray(self.response)
        return self.result


class RefundQuery_pub(Wxpay_client_pub):
    """退款查询接口"""

    def __init__(self, timeout=WxPayConf_pub.CURL_TIMEOUT):
        #设置接口链接
        self.url = "https://api.mch.weixin.qq.com/pay/refundquery"
        #设置curl超时时间
        self.curl_timeout = timeout
        super(RefundQuery_pub, self).__init__()

    def createXml(self):
        """生成接口参数xml"""
#         if any(self.parameters[key] is None for key in ("out_refund_no", "out_trade_no", "transaction_id", "refund_id")):
#             raise ValueError("missing parameter")
        self.parameters["appid"] = WxPayConf_pub.APPID  #公众账号ID
        self.parameters["mch_id"] = WxPayConf_pub.MCHID  #商户号
        self.parameters["nonce_str"] = self.createNoncestr()  #随机字符串
        self.parameters["sign"] = self.getSign(self.parameters)  #签名
        return  self.arrayToXml(self.parameters)

    def getResult(self):
        """ 获取结果，使用证书通信(需要双向证书)"""
        self.postXmlSSL()
        self.result = self.xmlToArray(self.response)
        return self.result


class DownloadBill_pub(Wxpay_client_pub):
    """对账单接口"""

    def __init__(self, timeout=WxPayConf_pub.CURL_TIMEOUT):
        #设置接口链接
        self.url = "https://api.mch.weixin.qq.com/pay/downloadbill"
        #设置curl超时时间
        self.curl_timeout = timeout
        super(DownloadBill_pub, self).__init__()

    def createXml(self):
        """生成接口参数xml"""
        if any(self.parameters[key] is None for key in ("bill_date", )):
            raise ValueError("missing parameter")

        self.parameters["appid"] = WxPayConf_pub.APPID  #公众账号ID
        self.parameters["mch_id"] = WxPayConf_pub.MCHID  #商户号
        self.parameters["nonce_str"] = self.createNoncestr()  #随机字符串
        self.parameters["sign"] = self.getSign(self.parameters)  #签名
        return  self.arrayToXml(self.parameters)

    def getResult(self):
        """获取结果，默认不使用证书"""
        self.postXml()
        self.result = self.xmlToArray(self.response)
        return self.result


class ShortUrl_pub(Wxpay_client_pub):
    """短链接转换接口"""

    def __init__(self, timeout=WxPayConf_pub.CURL_TIMEOUT):
        #设置接口链接
        self.url = "https://api.mch.weixin.qq.com/tools/shorturl"
        #设置curl超时时间
        self.curl_timeout = timeout
        super(ShortUrl_pub, self).__init__()

    def createXml(self):
        """生成接口参数xml"""
        if any(self.parameters[key] is None for key in ("long_url", )):
            raise ValueError("missing parameter")

        self.parameters["appid"] = WxPayConf_pub.APPID  #公众账号ID
        self.parameters["mch_id"] = WxPayConf_pub.MCHID  #商户号
        self.parameters["nonce_str"] = self.createNoncestr()  #随机字符串
        self.parameters["sign"] = self.getSign(self.parameters)  #签名
        return  self.arrayToXml(self.parameters)

    def getShortUrl(self):
        """获取prepay_id"""
        self.postXml()
        prepay_id = self.result["short_url"]
        return prepay_id



class Wxpay_server_pub(Common_util_pub):
    """响应型接口基类"""
    SUCCESS, FAIL = "SUCCESS", "FAIL"

    def __init__(self):
        self.data = {}  #接收到的数据，类型为关联数组
        self.returnParameters = {} #返回参数，类型为关联数组

    def saveData(self, xml):
        """将微信的请求xml转换成关联数组，以方便数据处理"""
        self.data = self.xmlToArray(xml)

    def checkSign(self):
        """校验签名"""
        tmpData = dict(self.data) #make a copy to save sign
        del tmpData['sign']
        sign = self.getSign(tmpData) #本地签名
        if self.data['sign'] == sign:
            return True
        return False

    def getData(self):
        """获取微信的请求数据"""
        return self.data

    def setReturnParameter(self, parameter, parameterValue):
        """设置返回微信的xml数据"""
        self.returnParameters[self.trimString(parameter)] = self.trimString(parameterValue)

    def createXml(self):
        """生成接口参数xml"""
        return self.arrayToXml(self.returnParameters)

    def returnXml(self):
        """将xml数据返回微信"""
        returnXml = self.createXml()
        return returnXml


class Notify_pub(Wxpay_server_pub):
    """通用通知接口"""
    def check_sign(self,xml):
        self.saveData(xml)
        return self.checkSign()
    def get_data(self):
        return self.data


class NativeCall_pub(Wxpay_server_pub):
    """请求商家获取商品信息接口"""

    def createXml(self):
        """生成接口参数xml"""
        if self.returnParameters["return_code"] == self.SUCCESS:
            self.returnParameters["appid"] = WxPayConf_pub.APPID #公众账号ID
            self.returnParameters["mch_id"] = WxPayConf_pub.MCHID #商户号
            self.returnParameters["nonce_str"] = self.createNoncestr() #随机字符串
            self.returnParameters["sign"] = self.getSign(self.returnParameters) #签名

        return self.arrayToXml(self.returnParameters)

    def getProductId(self):
        """获取product_id"""
        product_id = self.data["product_id"]
        return product_id


class NativeLink_pub(Common_util_pub):
    """静态链接二维码"""

    url = None #静态链接

    def __init__(self):
        self.parameters = {} #静态链接参数

    def setParameter(self, parameter, parameterValue):
        """设置参数"""
        self.parameters[self.trimString(parameter)] = self.trimString(parameterValue)

    def createLink(self):
        if any(self.parameters[key] is None for key in ("product_id", )):
            raise ValueError("missing parameter")

        self.parameters["appid"] = WxPayConf_pub.APPID  #公众账号ID
        self.parameters["mch_id"] = WxPayConf_pub.MCHID  #商户号
        time_stamp = int(time.time())
        self.parameters["time_stamp"] = "{0}".format(time_stamp)  #时间戳
        self.parameters["nonce_str"] = self.createNoncestr()  #随机字符串
        self.parameters["sign"] = self.getSign(self.parameters)  #签名          
        bizString = self.formatBizQueryParaMap(self.parameters, False)
        self.url = "weixin://wxpay/bizpayurl?"+bizString

    def getUrl(self):
        """返回链接"""
        self.createLink()
        return self.url


from util.utils import gen_redpack_billno

class Redpack_pub(Wxpay_client_pub):
    """红包发送接口"""

    def __init__(self, timeout=WxPayConf_pub.CURL_TIMEOUT):
        #设置接口链接
        self.url = "https://api.mch.weixin.qq.com/mmpaymkttransfers/sendredpack"
        #设置curl超时时间
        self.curl_timeout = timeout
        super(Redpack_pub, self).__init__()

    def createXml(self):
        """生成接口参数xml"""
        if any(self.parameters[key] is None for key in (
            "mch_billno", "re_openid",
            "total_amount", "total_num", "client_ip", "act_name",
            "remark")
            ):
            raise ValueError("missing parameter")

        self.parameters["wxappid"] = WxPayConf_pub.APPID  #公众账号ID
        self.parameters["send_name"] = "美分分"
        self.parameters["mch_id"] = WxPayConf_pub.MCHID  #商户号
        self.parameters["mch_billno"] = str(WxPayConf_pub.MCHID) +self.parameters["mch_billno"]
        self.parameters["nonce_str"] = self.createNoncestr()  #随机字符串
        self.parameters["sign"] = self.getSign(self.parameters)  #签名
        return  self.arrayToXml(self.parameters)

    def getResult(self):
        """ 获取结果，使用证书通信(需要双向证书)"""
        self.postXmlSSL()
        self.result = self.xmlToArray(self.response)
        return self.result


class GroupRedpack_pub(Wxpay_client_pub):
    """裂变红包发送接口"""

    def __init__(self, timeout=WxPayConf_pub.CURL_TIMEOUT):
        #设置接口链接
        self.url = "https://api.mch.weixin.qq.com/mmpaymkttransfers/sendgroupredpack"
        #设置curl超时时间
        self.curl_timeout = timeout
        super(GroupRedpack_pub, self).__init__()

    def createXml(self):
        """生成接口参数xml"""
        if any(self.parameters[key] is None for key in (
            "mch_billno", "re_openid",
            "total_amount", "total_num", "act_name",
            "remark")
            ):
            raise ValueError("missing parameter")

        self.parameters["wxappid"] = WxPayConf_pub.APPID  #公众账号ID
        self.parameters["send_name"] = "收红包神器"
        self.parameters["amt_type"] = "ALL_RAND"
        self.parameters["mch_id"] = WxPayConf_pub.MCHID  #商户号
        self.parameters["mch_billno"] = str(WxPayConf_pub.MCHID) +self.parameters["mch_billno"]
        self.parameters["nonce_str"] = self.createNoncestr()  #随机字符串
        self.parameters["sign"] = self.getSign(self.parameters)  #签名
        return  self.arrayToXml(self.parameters)

    def getResult(self):
        """ 获取结果，使用证书通信(需要双向证书)"""
        self.postXmlSSL()
        self.result = self.xmlToArray(self.response)
        return self.result


def send_redpack(open_id, price, name):
    ''' 送红包接口  'o56qvw-ThtwfthGGlZ-XbH-3fjRc'''
    pub     = Redpack_pub()
    amount  = str(int(price*100))
    pub.setParameter('re_openid', open_id)
    pub.setParameter('mch_billno', gen_redpack_billno())
    pub.setParameter('total_amount', amount)
    pub.setParameter('total_num', '1')
    pub.setParameter('client_ip', '139.196.6.231')
    pub.setParameter('act_name', '大学生收红包神器活动')
    pub.setParameter('remark', '美分分答题红包备注')
    pub.setParameter('wishing', '好友{}查看答案'.format(name))
    result  = pub.getResult()
    print result['result_code'], 'result code--------------'
    print result
    return result

def send_groupredpack():
    ''' 送裂变红包接口 '''
    pub     = GroupRedpack_pub()
    pub.setParameter('re_openid', 'o56qvw-ThtwfthGGlZ-XbH-3fjRc')
    pub.setParameter('mch_billno', gen_redpack_billno())
    pub.setParameter('total_amount', '500')
    pub.setParameter('total_num', '3')
    pub.setParameter('act_name', '美分分答题裂变红包')
    pub.setParameter('remark', '美分分答题裂变红包备注')
    pub.setParameter('wishing', '美分分答题裂变红包祝福')
    return pub.getResult()



def send_draw_cash(open_id, price):
    ''' 现金抽奖  'o56qvw-ThtwfthGGlZ-XbH-3fjRc'''
    pub     = Redpack_pub()
    amount  = str(int(price*100))
    pub.setParameter('re_openid', open_id)
    pub.setParameter('mch_billno', gen_redpack_billno())
    pub.setParameter('total_amount', amount)
    pub.setParameter('total_num', '1')
    pub.setParameter('client_ip', '139.196.6.231')
    pub.setParameter('act_name', '完善资料领红包')
    pub.setParameter('remark', '完善资料领红包备注')
    pub.setParameter('wishing', '完善资料领红包')
    result  = pub.getResult()
    print result['result_code'], 'result code--------------'
    print result
    return result


def test():
    c = HttpClient()
    assert c.get("http://www.baidu.com")[:15] == "<!DOCTYPE html>"
    c2 = HttpClient()
    assert id(c) == id(c2)



def refund_order(order, fee=None):
    assert order
    total_fee       = str(int(order.price*100))
    print total_fee, 'total_fee'
    if os.environ.get('APP_ENV')=='dev':
        total_fee   = '1'
    transaction_id  = order.transaction_id
    out_trade_no    = order.order_no
    out_refund_no   = order.order_no
    refund = Refund_pub()
    refund.setParameter("transaction_id",str(transaction_id))
    refund.setParameter('out_trade_no', out_trade_no)
    refund.setParameter('out_refund_no', out_refund_no)
    refund.setParameter('total_fee', total_fee)
    refund.setParameter('refund_fee', fee or total_fee)
    refund.setParameter('op_user_id', WECHAT_MCHID)
    result = refund.getResult()
    print 'refund......', '-'*80
    print result
    print '-'*80
    return result


def refund_repayment(amount, total_fee, order_no, transaction_id):
    ''' 还款的金额退换 '''

    total_fee   = str(int(total_fee*100))
    amount      = str(int(amount*100))

    out_refund_no   = '{}_{}'.format(order_no, int(time.time()))
    refund = Refund_pub()
    refund.setParameter("transaction_id",str(transaction_id))
    refund.setParameter('out_trade_no', order_no)
    refund.setParameter('out_refund_no', out_refund_no)
    refund.setParameter('total_fee', total_fee)
    refund.setParameter('refund_fee', amount)
    refund.setParameter('op_user_id', WECHAT_MCHID)
    result = refund.getResult()
    print 'refund......', '-'*80
    print result
    print '-'*80
    return result



def get_wx_pay_params(open_id, price, order_no, notify_url, body, no_credit=None):
    ''' 微信支付参数 '''
    unifie      = UnifiedOrder_pub()
    total_fee   = str(int(price*100))
    print total_fee, 'total_fee'
    if no_credit: unifie.parameters['limit_pay'] = no_credit
    print 'wx_pay_params', '-'*60, no_credit
    unifie.setParameter("out_trade_no", order_no)
    unifie.setParameter("total_fee",    total_fee)
    unifie.setParameter("notify_url",   notify_url)
    unifie.setParameter("trade_type",   "JSAPI")
    unifie.setParameter("body",         body)
    unifie.setParameter("openid",       open_id)
    prepay_id           = unifie.getPrepayId()

    err             = False
    print prepay_id, 'prepay_id'
    if not prepay_id: #获取不到prepay_id, 可能token有问题?
        wechat.refresh_wechat_token()
        err         = True
        return {}, err
    jsapi           = JsApi_pub()
    jsapi.setPrepayId(prepay_id)
    wx_pay_params = jsapi.getParameters()
    if wx_pay_params: wx_pay_params = json.loads(wx_pay_params)
    return wx_pay_params, err


def get_redpack_pay_params(open_id, price, order_no):
    ''' 发红包查看问题 '''
    notify_url      = WX_REDPACK_NOTIFY_URL
    body            = '美分分大学生收红包神器活动'
    return get_wx_pay_params(open_id, price, order_no, notify_url, body, no_credit='no_credit')



if __name__ == "__main__":
    test()