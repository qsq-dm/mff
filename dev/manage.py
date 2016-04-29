# -*- coding: utf-8 -*-
'''
创建管理员
python manage.py create_admin --name=用户名 --passwd=密码

支付成功
python manage.py mock_pay --order_id=1

创建假用户
python manage.py create_fake_user --start=10000009000

检查重复注册用户
python manage.py find_duplicate_reg

导出推广人员数据
python manage.py download_csv --promoter_id=1

恢复推广数据
python manage.py recover_promoter_count

'''

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


from flask import Flask

from flask.ext.script   import Manager
from flask.ext.migrate  import Migrate, MigrateCommand

from models             import app
from models             import db
from ops.item           import ItemService
from ops.data           import DataService
from ops.admin          import AdminService


migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)



@manager.command
def create_coupons():
    ''' 创建优惠券 '''
    from ops.coupon import CouponService
    effective       = 86400*30
    item_id         = None
    sub_cat_id      = None
    price           = 100
    cat             = 0
    #通用优惠券
    print CouponService.create_coupon(cat, '通用代金券', price, effective, item_id, sub_cat_id)
    #分类优惠券
    cat             = 6
    print CouponService.create_coupon(cat, '空腔分类代金券', price, effective, item_id, sub_cat_id)
    #子类优惠券 以牙齿为例 sub_cat_id 13
    cat             = 6
    sub_cat_id      = 13
    print CouponService.create_coupon(cat, '牙齿小类代金券', price, effective, item_id, sub_cat_id)
    #项目优惠券        冷光牙齿美白
    item_id         = 8
    print CouponService.create_coupon(cat, '指定项目代金券', price, effective, item_id, sub_cat_id)


@manager.command
def create_cats():
    types       = [
        {
           'name':'眼部', 'cats': [{'name': '双眼皮'},{'name': '单眼皮'}]
        },
        {
           'name':'鼻部', 'cats': [{'name': '扁'},{'name': '平'}]
        },
        {
           'name':'牙齿', 'cats': [{'name': '白'},{'name': '亮'}]
        },
        ]
    for parent in types:
        name        = parent['name']
        cat_id      = ItemService.create_cat(name)
        for i in parent['cats']:
            sub_cat_name = i['name']
            ItemService.create_sub_cat(cat_id, sub_cat_name, '', '水白白白亮')
    return types


@manager.command
def create_helps():
    ''' 帮助条目 '''
    from ops.data import DataService
    from setting.help import cats
    from setting.help import questions
    for cat in cats:
        DataService.create_help_cat(cat['id'], cat['name'])
    for question in questions:
        DataService.create_help_entry(question['cat_id'],  question['title'], question['content'])

@manager.command
def create_period_choices():
    from ops.credit import CreditService
    choices     = [
        {'id':1, 'period_count':3, 'period_fee': 0.01},
        {'id':2, 'period_count':6, 'period_fee': 0.03},
        {'id':3, 'period_count':12, 'period_fee': 0.05},
        {'id':4, 'period_count':18, 'period_fee': 0.07},    
    ]
    for i in choices:
        CreditService.create_period_choice(**i)

@manager.command
def create_admin(name=None, passwd=None):
    print name, passwd
    AdminService.create_admin(name, passwd)


def crawl_schools(page=1, head=True):
    ''' 抓取高校信息chrome xpath $x() '''
    from lxml import html
    import requests
    data    = {
        'ddlProvince'           : 0,
        '__VIEWSTATE'           : '/wEPDwUKMTE2NjY0ODc3Nw9kFgICAw9kFgQCAQ8QDxYGHg1EYXRhVGV4dEZpZWxkBQxQcm92aW5jZU5hbWUeDkRhdGFWYWx1ZUZpZWxkBQpQcm92aW5jZUlEHgtfIURhdGFCb3VuZGdkEBUjBuWFqOmDqAblm5vlt50G6YeN5bqGBuWMl+S6rAblpKnmtKUG5LiK5rW3Buays+WMlwblsbHopb8J5YaF6JKZ5Y+kBui+veWugQblkInmnpcJ6buR6b6Z5rGfBuaxn+iLjwbmtZnmsZ8G5a6J5b69Buemj+W7ugbmsZ/opb8G5bGx5LicBuays+WNlwbmuZbljJcG5rmW5Y2XBuW5v+S4nAblub/opb8G5rW35Y2XBui0teW3ngbkupHljZcG6KW/6JePBumZleilvwbnlJjogoMG6Z2S5rW3BuWugeWkjwbmlrDnloYG6aaZ5rivBua+s+mXqAblhbblroMVIwEwATEBMgEzATQBNQE2ATcBOAE5AjEwAjExAjEyAjEzAjE0AjE1AjE2AjE3AjE4AjE5AjIwAjIxAjIyAjIzAjI0AjI1AjI2AjI3AjI4AjI5AjMwAjMxAjMyAjMzAjM0FCsDI2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZGQCCQ8PFgIeC1JlY29yZGNvdW50AsMQZGQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgEFCWlidFNlYXJjaL9QO6naEBBAIEeLnXliOHBov+rx',
        '__VIEWSTATEGENERATOR'  : 'C818AE9B',
        '__EVENTVALIDATION'     : '/wEWKgLZ4pbwBgLGu9ryBwLZu9ryBwLYu9ryBwLbu9ryBwLau9ryBwLdu9ryBwLcu9ryBwLfu9ryBwLOu9ryBwLBu9ryBwLZu5rxBwLZu5bxBwLZu5LxBwLZu67xBwLZu6rxBwLZu6bxBwLZu6LxBwLZu77xBwLZu/ryBwLZu/byBwLYu5rxBwLYu5bxBwLYu5LxBwLYu67xBwLYu6rxBwLYu6bxBwLYu6LxBwLYu77xBwLYu/ryBwLYu/byBwLbu5rxBwLbu5bxBwLbu5LxBwLbu67xBwLbu6rxBwLa2vviBQLN0qSmAwLA15+mCwK1que1CgLYn9b4BgL6wv3hDD8SCUUQtAvvVBm+fe4GVrXDbLVb',
        '__EVENTTARGET'         : 'collegeListPager$lbtnNext',
        'collegeListPager$btGo' : 'GO',
        'collegeListPager$tbCurrentPage': page,
        }
    response    = requests.post('http://uhmajor.cdzk.net/college.aspx', data)
    tree    = html.fromstring(response.text)
    province_select  = tree.xpath('//*[@id="ddlProvince"]') #省份选项
    for i in province_select[0].getchildren():
        if head: print i.text

    pager   = tree.xpath('//*[@id="collegeListPager_lbTotalPage"]') #省份选项
    page_count  = int(pager[0].text)

    if head:
        print '-'*80
        print '共{}页'.format(page_count)
        print '-'*80
        for i in range(1, page_count+1):
            crawl_schools(i, False)

    if not head:
        rows    = tree.xpath('//*[@id="right"]/table')
        print response.text
        print page, rows, 'rows'
        for i in rows[0].getchildren()[1:]:
            childs  = i.getchildren()
            name, location, link, remark    = childs
            name    = (name.text or '').decode('utf8').strip()
            location= (location.getchildren()[0].text or '').decode('utf8').strip()
            link    = (link.getchildren()[0].text or '').decode('utf8').strip()
            remark  = ''
            print name, location, link, remark
            DataService.create_school(name, link, location)
    return province_select


@manager.command
def mock_pay(order_id=None):
    ''' 直接命令行使支付成功 '''
    import os
    if os.environ.get('APP_DEV')=='production': return
    from ops.order  import OrderService
    from user.views import pay_success_action
    order    = OrderService.get_order_by_id(order_id)
    if not order:
        print '订单不存在'
        return
    need_pay = not order.price and order.credit_verified
    pay_success_action(order, need_pay=need_pay)


@manager.command
def md5_user_passwd():
    ''' md5保存用户名密码 '''
    from models import *
    from util.utils import md5_str
    users       = User.query.all()
    for user in users:
        if len(user.passwd)!=32:
            passwd          = md5_str(user.passwd)
            User.query.filter(User.id==user.id).update({'passwd':passwd})
    db.session.commit()


@manager.command
def create_fake_user(start=10000009000, limit=20):
    ''' 创建用户 '''
    from ops.user import UserService
    from ops.promote import PromoteService
    from util.utils import md5_str
    start     = int(start)
    for i in range(int(limit)):
        phone = start + i
        print phone
        user_id = UserService.create_user(phone, phone, md5_str('meifenfen'))
        if user_id: PromoteService.add_fakeuser(user_id)


@manager.command
def add_imgs_width():
    ''' 设置图片宽高 '''
    from ops.item import ItemService
    from ops.data import DataService
    from util.utils import get_img_key
    has_more, infos = ItemService.get_paged_recommend_items()
    while infos:
        offset      = infos[-1]['id']
        for info in infos:
            DataService.set_img_size(get_img_key(info['image']))
        has_more, infos = ItemService.get_paged_recommend_items(offset=offset)


@manager.command
def check_promoter_detail(promoter_id=None):
    ''' '''
    from sqlalchemy import func
    from sqlalchemy import and_
    from models import *
    sub_promoters = Promoter.query.filter(Promoter.create_by==promoter_id).all()
    total = 0
    for p in sub_promoters:
        qrcodes = Qrcode.query.filter(Qrcode.promoter_id==p.id).all()
        qrcode_ids = [q.id for q in qrcodes]
        query   = and_(
            QrCodeUser.qrcode_id.in_(qrcode_ids),
            QrCodeUser.user_id>0
            )
        count   = db.session.query(func.count(QrCodeUser.id)).filter(query).first()[0]
        print p.name, count
        total += count
    print 'total', total

@manager.command
def set_user_first_location():
    from models import db
    from models import QrCodeUser
    from ops.promote import PromoteService
    from models import WechatLocation
    rows=db.session.query(WechatLocation.open_id, WechatLocation.lng, WechatLocation.lat).group_by(WechatLocation.open_id).all()
    for row in rows:
        open_id = row[0]
        lng     = row[1]
        lat     = row[2]
        PromoteService.set_first_location(open_id, lng, lat)

'''
>>> '{0: <5}'.format('ss')
'ss   '
>>> '{0: <5}'.format('sss')
'sss  '
>>> '{0: <5}'.format('ssss')
'ssss '
>>> '{0: <5}'.format('sssss')
'sssss'
'''
@manager.command
def find_duplicate_reg():
    from models import *
    from sqlalchemy import func
    from collections import defaultdict
    rows        = db.session.query(WechatReg.open_id, func.count(WechatReg.id)).group_by(WechatReg.open_id)
    duplicates  = []
    for i in rows:
        if i[1]>1: duplicates.append(i)
    print '{0: <5} {1: <10} {2: <11} {3: <25} {4: <20} {5: <3}'.format('id', '用户名', '手机号', '创建时间', 'open_id', '注册数')
    total = 0
    data  = defaultdict(lambda:0)
    for i in duplicates:
        reg_count   = i[1]
        open_id     = i[0]
        qrcodeuser  = QrCodeUser.query.filter(QrCodeUser.open_id==open_id).first()
        qrcode_id   = qrcodeuser.qrcode_id
        if qrcode_id:
            qrcode      = Qrcode.query.filter(Qrcode.id==qrcode_id).first()
            promoter_id = qrcode.promoter_id
            print promoter_id, 'promoter_id', i[1]
            data[promoter_id]+=i[1]-1
            total += i[1]-1
        user_id     = qrcodeuser.user_id
        user        = User.query.filter(User.id==user_id).first()
        format_str  = '{0: <5} {1: <10} {2: <11} {3: <25} {4: <20} {5: <3}'.format(
            user.id, user.name, user.phone, str(user.create_time)[:16], i[0], i[1])
        print format_str
    print 'total', total
    #return 
    data_admin  = defaultdict(lambda:0)
    for k, v in data.items():
        Promoter.query.filter(Promoter.id==k).update({'dup_count': v})
        db.session.commit()
        promoter    = Promoter.query.filter(Promoter.id==k).first()
        parent_id   = promoter.create_by
        if parent_id:
            data_admin[parent_id]+=v
    for k,v in data_admin.items():
        promoter = Promoter.query.filter(Promoter.id==k).first()
        print promoter.id, promoter.name, promoter.phone, v

def write_to_csv():
    import csv
    schools         = DataService.get_schools()
    with open('schools.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for i in schools:
            writer.writerow([i.name, i.city_name, i.link])



@manager.command
def download_csv(promoter_id=None, output_file=''):
    from models import *
    from sqlalchemy import and_
    from ops.promote import PromoteService
    from ops.bulks  import fetch_user_refs
    promoters   = Promoter.query.filter(Promoter.create_by==promoter_id).all()
    promoter_ids= [i.id for i in promoters]
    qrcodes     = Qrcode.query.filter(Qrcode.promoter_id.in_(promoter_ids)).all()
    qr_code_ids = [i.id for i in qrcodes]
    query       = and_(
        QrCodeUser.user_id>0,
        QrCodeUser.qrcode_id.in_(qr_code_ids)
        )
    qrcode_user = QrCodeUser.query.filter(query).all()
    qrcode_user_dict_list = [i.as_dict() for i in qrcode_user]
    fetch_user_refs(qrcode_user_dict_list)
    print len(qrcode_user_dict_list)
    import csv
    with open('/tmp/meifenfen/export/promoter_users_{}.csv'.format(promoter_id), 'w') as csvfile:
        for i in qrcode_user_dict_list:
            user_name   = i['user']['name']
            create_time = str(i['user']['create_time'])
            user_sex    = i['sex'] or ''
            user_id     = i['user']['id']
            user_phone  = i['user']['phone']
            user_location = i['location'] or ''
            if user_sex==1:
                user_sex    = '男'
            elif user_sex==2:
                user_sex    = '女'
            print user_id, user_name, user_sex, user_phone, user_location, create_time
            promoter_map    = PromoteService.get_qrcodeusers_by_open_ids(([i['open_id']]))
            promoter        = promoter_map[i['open_id']]['promoter']
            parent          = promoter_map[i['open_id']]['parent']
            print promoter, parent
            writer = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
            promoter_name   = promoter['name']
            promoter_admin_name = parent['name']
            writer.writerow([
                user_id, user_name, user_sex, user_phone,
                user_location, promoter_name, promoter_admin_name, create_time
                ])

    print len(qrcode_user_dict_list)


@manager.command
def recover_promoter_count():
    from models import *
    from sqlalchemy import func
    from sqlalchemy import and_
    Promoter.query.update({"follow_count":0,"reg_count":0, "unfollow_count": 0})
    db.session.commit()
    rows    = db.session.query(QrCodeUser.qrcode_id, func.count(QrCodeUser.open_id)).group_by(QrCodeUser.qrcode_id)
    for i in rows:
        promoter = Qrcode.query.filter(Qrcode.id==i[0]).first()
        if promoter:
            print promoter.promoter_id
            Promoter.query.filter(Promoter.id==promoter.promoter_id).update({'follow_count':Promoter.follow_count+i[1]})
            db.session.commit()
    query   = QrCodeUser.user_id>0
    rows    = db.session.query(QrCodeUser.qrcode_id, func.count(QrCodeUser.open_id)).filter(query).group_by(QrCodeUser.qrcode_id)
    for i in rows:
        promoter = Qrcode.query.filter(Qrcode.id==i[0]).first()
        if promoter:
            print promoter.promoter_id
            Promoter.query.filter(Promoter.id==promoter.promoter_id).update({'reg_count':Promoter.reg_count+i[1]})
            db.session.commit()

    query   = and_(
        QrCodeUser.user_id>0,
        QrCodeUser.status==0
        )
    rows    = db.session.query(QrCodeUser.qrcode_id, func.count(QrCodeUser.open_id)).filter(query).group_by(QrCodeUser.qrcode_id)
    for i in rows:
        promoter = Qrcode.query.filter(Qrcode.id==i[0]).first()
        if promoter:
            print promoter.promoter_id
            Promoter.query.filter(Promoter.id==promoter.promoter_id).update({'unfollow_count':Promoter.unfollow_count+i[1]})
            db.session.commit()



@manager.command
def dump_edit_log():
    from models import EditNameLog
    import csv
    rows    = EditNameLog.query.all()
    with open('/tmp/edit_name.csv', 'w') as csvfile:
        for i in rows:
            writer = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([
                i.id, i.user_id, i.create_time
                ])

@manager.command
def recover_edit_name():
    import csv
    from models import EditNameLog
    reader = csv.reader(file('edit_name.csv', 'rb'))
    for line in reader:
        print line
        log     = EditNameLog(id=line[0], user_id=line[1], create_time=line[2])
        db.session.add(log)
        db.session.commit()


@manager.command
def clear_invalid_counter(phone=None):
    ''' 清空用户错误短信码计数 '''
    from ops.cache import get_today_timestamp
    from ops.cache import cache
    from ops.cache import InvalidUserPasswdCache
    print InvalidUserPasswdCache.clear_today_counter(phone)


@manager.command
def import_school_from_csv():
    import csv
    from ops.data import DataService
    reader = csv.reader(file('schools.csv', 'rb'))
    for line in reader:
        name, city_name, link = line[:3]
        DataService.create_school(name, link, city_name)


@manager.command
def reset_user_question_money():
    ''' '''
    from ops.redpack import RedpackService
    money_map   = RedpackService.total_money_group_by_question([])
    from models import db
    from models import RedpackUserQuestion
    for user_question_id, money in money_map.items():
        RedpackUserQuestion.query.filter(RedpackUserQuestion.id==user_question_id).update({'money': money})
        db.session.commit()


@manager.command
def reset_room_vote():
    from ops.cache  import RoomDesignVoteCounter
    from models import *
    from sqlalchemy import func
    RoomDesignVoteCounter.reset()
    rooms   = RoomDesignDetail.query.order_by(RoomDesignDetail.id.desc()).all()
    max_no  = db.session.query(func.max(RoomDesignDetail.apply_no)).scalar() or 1000000
    RoomDesignVoteCounter.incr_apply_no(int(max_no))
    for room in rooms:
        RoomDesignVoteCounter.init(room.id)
        RoomDesignVoteCounter.incr(room.id, room.vote_count)
        RoomDesignVoteCounter.add_score(room.vote_count)
    RoomDesignVoteCounter.add_score(0)


@manager.command
def add_priviledge():
    ''' 之前已经通过额度申请的投票权限 '''
    from models import CreditApply
    from constants import CREDIT_STATUS
    from ops.cache import RoomDesignVoteCounter
    from ops.room_design import RoomDesignService
    result  = CreditApply.query.all()
    for apply in result:
        if apply.status!=3: continue
        RoomDesignService.add_user_vote_privilege(apply.user_id, 1)

@manager.command
def get_unfollowed():
    ''' 取消关注用户列表 '''
    from app import app
    from thirdparty.wechat import wechat
    from models import QrCodeUser
    from ops.promote import PromoteService
    users = db.session.query(QrCodeUser.id).order_by(QrCodeUser.id.desc()).all()
    for user_id in users:
        #if user_id[0]>3779: continue
        i = QrCodeUser.query.filter(QrCodeUser.id==user_id[0]).first()
        print i.id, '-'*80, i.open_id
        if len(i.open_id or '')<10: continue
        #info = wechat.get_user_info(i.open_id)
        PromoteService.set_user_sex(i.open_id)
        continue
        if not info['subscribe']:
             print i.open_id
             if i.nickname:PromoteService.set_wechat_status(i.open_id, 0)

@manager.command
def init_prize():
    ''' 初始化抽奖 '''
    from models import RdMoneyPrize
    from models import db
    prize_types     = [
        {'id':1, 'amount':1, 'total':700},
        {'id':2, 'amount':2, 'total':200},
        {'id':3, 'amount':3, 'total':50},
        {'id':4, 'amount':5, 'total':30},
        {'id':5, 'amount':10, 'total':20},
        {'id':6, 'amount':30, 'total':0},
        {'id':7, 'amount':50, 'total':0},
        {'id':8, 'amount':100, 'total':0},
        ]
    for i in prize_types:
        prize = RdMoneyPrize(**i)
        db.session.add(prize)
        db.session.commit()



@manager.command
def export_room_sms():
    ''' 到处发短信用户 '''
    import csv
    from models import *
    from thirdparty.sms import send_room_one
    from thirdparty.sms import send_room_two
    no_vote_set     = set()
    vote_set        = set()
    old_user_set    = set()
    rooms           = RoomDesignDetail.query.all()
    for i in rooms:
        user        = User.query.filter(User.id==i.user_id).first()
        if (user.phone or '').startswith('1000000'): continue
        if i.vote_count==0:
            no_vote_set.add(user.phone)
        else:
            vote_set.add(user.phone)
    users           = User.query.all()
    for user in users:
        if (user.phone or '').startswith('1000000'): continue
        if user.phone in vote_set or user.phone in no_vote_set: continue
        old_user_set.add(user.phone)

    #return
        
    with open('vote_set.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for index, i in enumerate(sorted(vote_set)):
            print 'send vote set....', index, i ;
            #send_room_two(i)
            continue
            writer.writerow([i])
    with open('no_vote_set.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for index, i in enumerate(sorted(no_vote_set)):
            print 'send no vote set....', index, i ;
            #send_room_two(i)
            continue
            writer.writerow([i])
    with open('old_user_set.csv', 'w') as csvfile:
        import time
        writer = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for index, i in enumerate(sorted(old_user_set)):
            if i<='13817485053':
                print 'small continue'
                continue
            time.sleep(0.1)
            print 'send old user set....', index, i ;
            send_room_one(i)
            continue
            writer.writerow([i])

    print len(no_vote_set), len(old_user_set), len(vote_set)



if __name__ == '__main__':
    manager.run()


