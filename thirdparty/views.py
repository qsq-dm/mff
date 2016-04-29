# -*- coding: utf-8 -*-

from flask import request
from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from thirdparty.wechat import wechat
from settings import CONTACT
from ops.promote import PromoteService


server_verify       = Blueprint('server_verify', __name__,
                        template_folder='templates')

meifenfen_open_ids  = set([
"o56qvw-ThtwfthGGlZ-XbH-3fjRc",
"o56qvw-OyM2NRJ6jHQDxsOXdF0Pc",
"o56qvw3FG1tt39dw4i8L0SrpBFCQ",
"o56qvw2lAC5eXqIa87o35EYvtxJw",
"o56qvw0fwSQlUMl4ChyafE4ajKjM",
"o56qvw63JsGh6Lz2BU5cUEYlZNAw",
"o56qvw-cLgV-CLxVyKU3P-zJ0aJk",
"o56qvw-hxHtmnZ8bNGYSxFihTjRk",
"o56qvw-hFbnnIMzQA3ArpsYNRylE",
"o56qvwy77LP82ZWZ8q5Gy-ebCOeU",
"o56qvw0PnwLCK7Okesvhkc7d6UGA",
"o56qvwy2plGL6LeBY-gzFtn6_Yis",
"o56qvwzrgKsuO28J7PKymLChJrSY",
"o56qvwwzTB80JXYJYnqKsEO-vXqE",
"o56qvw4oaWtk600BtO1Tsa6BbAQY",
"o56qvw2buPRaEWJ1TdKLn-HxqyBo",
"o56qvw2u0B7NcHfKseEDy-oDK1bI",
"o56qvw3ppto7QGZq96W5zd4p58YQ",
"o56qvwxvcD7ddq1GoEr0XNyVAyYs",
"o56qvw9XQZ2-JATmeVcdMNveGJzk"
])

def check_signature():
    try:
        signature = request.args['signature']
        timestamp = request.args['timestamp']
        nonce = request.args['nonce']
        echostr = request.args.get('echostr') or 'success'
        if wechat.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
            return echostr
    except:
        import traceback
        traceback.print_exc()
        return ''

index_link= '''http://www.meifenfen.com/user/index/'''

q_link= '''http://www.meifenfen.com/static/user/Activities/home.html'''
WELCOME_MSG = '''这位小主，欢迎关注美分分

美分分，为你加分！
“微整形，分期付，美丽加分0负担 ” 
<a href='{}'>→点此查看详情</a>

上海大学生寝室设计大赛火热进行中，
2000元现金大奖，坐等你来抢
<a href='{}'>→点此报名领百元大礼包</a>
'''.format(index_link, q_link)

WELCOME_MSG = '''<a href='http://www.meifenfen.com/static/user/login.html'>美分分，为你加分！</a>
'''

'''
http://omgitsmgp.com/2012/10/13/notes-on-flask/
If a URL has a trailing slash, accessing it without one will automatically redirect;
if a URL doesn’t have a trailing slash, accessing it with one will generate a 404.
'''
@server_verify.route('', methods=['POST','GET'])
def wechat_verify():
    try:
        if request.method == 'GET':
            echostr = check_signature()
            if echostr: return echostr
            return 'error'
        elif request.method == 'POST':
            if check_signature():
                print request.form, 'form'
                print(request.data), 'data'
                wechat.parse_data(request.data)
                message = wechat.get_message()
                response = None
                print message.type;
                print message.__dict__
                if message.type=='click' and message.key=='contact_us':
                    return wechat.response_text(u'客服电话:{}'.format(CONTACT))
                if message.type=='subscribe':
                    #if message.key: #扫码关注
                    key         = None
                    if message.key:
                        key     = message.key.split('_')[-1]
                    log_id      = PromoteService.log_qr_user(key, message.source)
                    if not log_id:
                        PromoteService.set_wechat_status(message.source, 1)
                    print log_id, key,'-------qrcode sub'
                    if key:
                        qrcode  = PromoteService.get_qrcode(key)
                        if qrcode:
                            if log_id: PromoteService.incr_promote_follow_count(qrcode.promoter_id)
                        else:
                            print 'qrcode not exist'
                    PromoteService.set_user_sex.delay(message.source)
                    if message.source in meifenfen_open_ids:
                        return wechat.response_text(WELCOME_MSG)       
                    return wechat.response_text('')
                if message.type=='unsubscribe':
                    PromoteService.set_wechat_status(message.source, 0)
                    qrcode_user = PromoteService.get_qrcodeuser_by_open_id(message.source)
                    if qrcode_user:
                        qrcode  = PromoteService.get_qrcode(qrcode_user.qrcode_id)
                        if qrcode:
                            PromoteService.incr_promote_unfollow_count(qrcode.promoter_id)
                    return wechat.response_text('')
                if message.type == 'text':
                    if message.content == 'wechat':
                        response = wechat.response_text(u'哈哈')
                    else:
                        response = wechat.response_text(u'?')
                elif message.type == 'image':
                    response = wechat.response_text(u'图片')
                elif message.type == 'location':
                    print message.longitude, message.latitude #经纬度
                    open_id     = message.source
                    lng         = message.longitude
                    lat         = message.latitude
                    is_first    = not PromoteService.get_first_location(open_id)
                    PromoteService.log_wechat_location(open_id, lng, lat)
                    if is_first: PromoteService.set_first_location(open_id, lng, lat)
                    response = wechat.response_text(u'地理位置')
                else:
                    response = wechat.response_text(u'未知')
                return ''
            else:
                return ''
    except Exception as e:
        import traceback
        traceback.print_exc()
        return ''









