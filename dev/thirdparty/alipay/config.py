#-*- coding:utf-8 -*-
from settings import SERVER_NAME


class settings:
  # 安全检验码，以数字和字母组成的32位字符
  ALIPAY_KEY = 'knpsiyyep0ertnut5mmt844dkntswotd'

  ALIPAY_INPUT_CHARSET = 'utf-8'

  # 合作身份者ID，以2088开头的16位纯数字
  ALIPAY_PARTNER = '2088021957827236'

  # 签约支付宝账号或卖家支付宝帐户
  ALIPAY_SELLER_EMAIL = 'zhaohh@meifenfen.com'

  ALIPAY_SIGN_TYPE = 'RSA'

  # 付完款后跳转的页面（同步通知） 要用 http://格式的完整路径，不允许加?id=123这类自定义参数
  ALIPAY_RETURN_URL = 'http://{}/user/finish_pay'.format(SERVER_NAME)
  
  # 交易过程中服务器异步通知的页面 要用 http://格式的完整路径，不允许加?id=123这类自定义参数
  ALIPAY_NOTIFY_URL='http://{}/api/alipay_notify/'.format(SERVER_NAME)
  ALIPAY_REPAYMENT_NOTIFY_URL='http://{}/api/alipay_repayment_notify/'.format(SERVER_NAME)

  ALIPAY_SHOW_URL=''

  # 网关地址
  #WEB_GATEWAY = 'https://mapi.alipay.com/gateway.do?'
  WEB_GATEWAY = 'http://wappaygw.alipay.com/service/rest.htm?'
  WEB_GATEWAY = 'https://mapi.alipay.com/gateway.do?'
  # 访问模式,根据自己的服务器是否支持ssl访问，若支持请选择https；若不支持请选择http
  ALIPAY_TRANSPORT='https'


  PRIVATE_KEY = '''-----BEGIN RSA PRIVATE KEY-----
MIICWwIBAAKBgQCg6pjF7bK7dxQnFVIJAWCdOPraLIkPOsFuIvKFYXQTd5PtFSEv
5zsKwXd4dolTTge7QbabKY8RHPlukyDfM+mogsMkZ1/AdZqRj3xLU0twXWi5UfO9
hA6bgUcDQM4tsg5QDLOuTc//4YQ/71XSbvbvKznHGD7M6p0JVS8Au7C2fwIDAQAB
AoGAM0SLCASDPVbjBNC2IkheD7lnsrsdr8x4dC6ONhCmes1OQ+rHeAujs/mPpsGd
Xv0tWWvGUgkbm8gvcBtQDczsVFJwCkDZpC4WOFIH5sBffOmVjunXaSdrcgczZlbJ
yosUWXw22lBcKUVwd+cv50yGUH9i5fJcJkLwdZ4h9Hqu2wECQQDRcZzH2HDUnelK
bTrsVukfad4V8ShZVdMJ9b8BLfh3w1gAXY1i2D1q8x39P+kcI/U3pga6xfv2nYS+
QkpENoyJAkEAxK+I/ES/i96QoNzu87pMrDZElZTjQZ39Ab70eqvD+o03y8r3C6YJ
EHCZ6C5zeFJTh9bGk/spoerQuGBrkk+4xwJAdypVMb+MMuzF13rek6m/aggqPAHC
G1IhiQExc9JcFIgogcy4rQyrpTY+UeETGNe8pbTpD0umWGK3LCk7aCRBQQJAM9FT
M7MhC8Z9MARE5+1jGdPKSeZJ4RWwfG9ElbT/Etl1o7k7UNRTewNPaP4j6cU2wIjz
FDWNiF0G1CyC6q8aLQJAPdqJTCLlxGAzDtOfAAYrJKycxixOpZZ2z857Xdf8jTYL
xnzl0xanRphWrLmbqhCPpGc2esxO0HbUq/OodLKWcQ==
-----END RSA PRIVATE KEY-----'''


  PUBLIC_KEY = '''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCg6pjF7bK7dxQnFVIJAWCdOPra
LIkPOsFuIvKFYXQTd5PtFSEv5zsKwXd4dolTTge7QbabKY8RHPlukyDfM+mogsMk
Z1/AdZqRj3xLU0twXWi5UfO9hA6bgUcDQM4tsg5QDLOuTc//4YQ/71XSbvbvKznH
GD7M6p0JVS8Au7C2fwIDAQAB
-----END PUBLIC KEY-----'''
  

