# -*- coding: utf-8 -*-

from sqlalchemy     import and_
from sqlalchemy     import or_
from sqlalchemy     import func
from util.sqlerr    import SQL_DUPLICATE
from util.sqlerr    import SQL_DUPLICATE_PHONE
from util.utils     import convert_locaton
from models         import db
from models         import Promoter
from models         import Qrcode
from models         import QrCodeUser
from models         import WechatLocation
from models         import FakeUser
from models         import WechatReg

from ops.utils      import get_items
from ops.utils      import get_page
from ops.utils      import count_items
from thirdparty.wechat import wechat
from thirdparty.wechat import create_qrcode
from thirdparty.qn   import upload_img
from settings        import celery


class PromoteService(object):

    @staticmethod
    def log_qr_user(qr_key, open_id):
        ''' 记录从扫描二维码关注的用户 '''
        log     = QrCodeUser(qrcode_id=qr_key, open_id=open_id)
        try:
            db.session.add(log)
            db.session.commit()
            return log.id
        except Exception as e:
            db.session.rollback()
            import traceback
            traceback.print_exc()
            if SQL_DUPLICATE.search(str(e)):
                print 'duplicate qrcode user...'

    @staticmethod
    def check_user(phone, passwd):
        ''' 手机 密码 '''
        query  = and_(
            Promoter.phone==phone,
            Promoter.passwd==passwd,
            Promoter.status==1
            )
        user   = Promoter.query.filter(query).first()
        return user

    @staticmethod
    def create_promoter(phone, passwd, name, create_by=None, status=1):
        try:
            promoter    = Promoter(phone=phone, status=status, passwd=passwd, name=name, create_by=create_by)
            db.session.add(promoter)
            db.session.commit()
            return promoter.id
        except Exception as e:
            db.session.rollback()
            if SQL_DUPLICATE_PHONE.search(str(e)):
                assert 0, '手机号已存在'

    @staticmethod
    def get_paged_promoters(**kw):
        return get_page(Promoter, {}, **kw)

    @staticmethod
    def count_promoters(where=None):
        return count_items(Promoter, where)

    @staticmethod
    def create_promoter_qrcode(promoter_id, act_type=None):
        ''' 创建推广者二维码 先返回美分分存的二维码id
        然后下载图片 最终访问 都是用的七牛的链接
        '''
        qrcode      = Qrcode(promoter_id=promoter_id, act_type=act_type)
        db.session.add(qrcode)
        db.session.commit()
        return qrcode.id

    @staticmethod
    def get_promoter_by_phone(phone):
        ''' '''
        promoter    = Promoter.query.filter(Promoter.phone==phone).first()
        if promoter: return promoter

    @staticmethod
    @celery.task
    def download_promoter_qrcode(qrcode_id):
        ''' 异步创建qrcode '''
        ticket, response        = create_qrcode(qrcode_id)
        image_content           = response.content
        image_key               = 'promoter_qrcode_{}.jpg'.format(qrcode_id)
        upload_img(image_key, image_content)
        update_data             = {
            'ticket'               : ticket,
            'image'                : image_key
            }
        count                   = Qrcode.query.filter(Qrcode.id==qrcode_id).update(update_data)
        db.session.commit()
        return count

    @staticmethod
    def count_promoters(where=None):
        ''' 推广人员数 '''
        return count_items(Promoter, where)

    @staticmethod
    def incr_promote_follow_count(promoter_id):
        ''' 推广关注人加1 '''
        count           = Promoter.query.filter(Promoter.id==promoter_id).update({'follow_count':Promoter.follow_count+1})
        db.session.commit()
        return count

    @staticmethod
    def incr_promote_reg_count(promoter_id):
        ''' 推广注册人加1 '''
        count           = Promoter.query.filter(Promoter.id==promoter_id).update({'reg_count':Promoter.reg_count+1})
        db.session.commit()
        return count

    @staticmethod
    def log_wechat_location(open_id, lng, lat):
        ''' 定位 '''
        log             = WechatLocation(open_id=open_id, lng=lng, lat=lat)
        db.session.add(log)
        db.session.commit()
        return log.id

    @staticmethod
    def del_promoter(promoter_id):
        ''' 删除 '''
        count   = Promoter.query.filter(Promoter.id==promoter_id).update({'status':0})
        db.session.commit()
        return count

    @staticmethod
    @celery.task
    def set_user_sex(open_id):
        ''' 获取用户性别 '''
        try:
            from thirdparty.wechat import wechat
            info    = wechat.get_user_info(open_id)
            if info['subscribe']:
                sex = info['sex']
                city= info['city']
                nickname= info['nickname']
                headimgurl = info['headimgurl']
                data = {
                    'sex': sex,
                    'city': city,
                    'nickname': nickname,
                    'headimgurl': headimgurl
                    }
            else:
                print open_id, '未关注'
                return
            count   = QrCodeUser.query.filter(QrCodeUser.open_id==open_id).update(data)
            db.session.commit()
            return count
        except Exception as e:
            import traceback
            traceback.print_exc()
            wechat.refresh_wechat_token()


    @staticmethod
    def get_promoter_qrcodes_by_promoter_ids(promoter_ids):
        query   = Qrcode.promoter_id.in_(promoter_ids)
        rows    = Qrcode.query.filter(query).all()
        return [row.as_dict() for row in rows]

    @staticmethod
    def get_qrcode(qrcode_id):
        ''' '''
        return Qrcode.query.filter(Qrcode.id==qrcode_id).first()

    @staticmethod
    def get_qrcodeuser_by_open_id(open_id):
        return QrCodeUser.query.filter(QrCodeUser.open_id==open_id).first()

    @staticmethod
    def set_wechat_user_id(open_id, user_id):
        ''' 设置微信用户 美分分user_id'''
        count   = QrCodeUser.query.filter(QrCodeUser.open_id==open_id).update({'user_id':user_id})
        reg     = WechatReg(open_id=open_id, user_id=user_id)
        db.session.add(reg)
        db.session.commit()
        return count

    @staticmethod
    def add_fakeuser(user_id):
        fake_user = FakeUser(user_id=user_id)
        db.session.add(fake_user)
        db.session.commit()
        return fake_user.id

    @staticmethod
    def get_fakeuser_by_userid(user_id):
        ''' 判断是否是假用户 '''
        return FakeUser.query.filter(FakeUser.user_id==user_id).first()

    @staticmethod
    def count_promoter_admin_reg(promoter_ids):
        ''' 推广管理员手下人注册总数 '''
        query   = and_(
            Promoter.create_by.in_(promoter_ids),
            )
        rows    = db.session.query(
            Promoter.create_by, func.sum(Promoter.follow_count), func.sum(Promoter.reg_count)). \
            filter(query).group_by(Promoter.create_by).all()

        return rows

    @staticmethod
    def get_user_qrcodes_by_user_ids(user_ids):
        ''' 获取用户qrcode '''
        qrcode_users = QrCodeUser.query.filter(QrCodeUser.user_id.in_(user_ids)).all()
        return [i.as_dict() for i in qrcode_users]

    @staticmethod
    def get_promoter_user_id_suq(promoter_id):
        promoter_q      = or_(
            Promoter.create_by==promoter_id,
            Promoter.id==promoter_id
            )
        admin_promoters = Promoter.query.filter(promoter_q).all()
        promoter_ids  = [i.id for i in admin_promoters]
        qrcodes  = Qrcode.query.filter(Qrcode.promoter_id.in_(promoter_ids)).all()
        
        qrcode_ids =  [q.id for q in qrcodes]
        user_ids_suq = db.session.query(QrCodeUser.user_id).filter(QrCodeUser.qrcode_id.in_(qrcode_ids)).subquery()
        return user_ids_suq

    @staticmethod
    def get_qrcode_user_by_user_id(user_id):
        ''' '''
        qrcode_user     = QrCodeUser.query.filter(QrCodeUser.user_id==user_id).first()
        return qrcode_user

    @staticmethod
    def get_first_location(open_id):
        ''' 首次地址 '''
        loc     = WechatLocation.query.filter(WechatLocation.open_id==open_id).order_by(WechatLocation.id.asc()).first()
        if loc: return loc.as_dict()

    @staticmethod
    def set_first_location(open_id, lng, lat):
        try:
            lnglat = '{},{}'.format(lng, lat)
            location = convert_locaton(lnglat)
            name     = location['list'][0]['district']['name']
            print lnglat, name
            data    = {
                'location': name,
                'lnglat': lnglat
                }
            QrCodeUser.query.filter(QrCodeUser.open_id==open_id).update(data)
            db.session.commit()
        except Exception as e:
            import traceback
            traceback.print_exc()
            print 'convert location error...', lnglat

    @staticmethod
    def open_id_user_ids_suq(open_id):
        ''' '''
        query   = and_()
        query.append(WechatReg.open_id==open_id)
        suq     = db.session.query(WechatReg.user_id).filter(query).subquery()
        return suq

    @staticmethod
    def count_open_id_user_count(open_ids):
        query   = WechatReg.open_id.in_(open_ids)
        result  = db.session.query(WechatReg.open_id,func.count(WechatReg.id)).filter(query).group_by(WechatReg.open_id).all()
        return dict(result)

    @staticmethod
    def get_user_id_open_id_map(open_ids):
        rows    = WechatReg.query.filter(WechatReg.open_id.in_(open_ids)).all()
        from collections import defaultdict
        data    = {}
        for i in rows:
            data[i.user_id] = i.open_id
        return data

    @staticmethod
    def get_open_ids_by_user_ids(user_ids):
        rows    = WechatReg.query.filter(WechatReg.user_id.in_(user_ids)).all()
        return [i.open_id for i in rows]

    @staticmethod
    def get_qrcodeusers_by_open_ids(open_ids):
        ''' '''
        join_query = and_(
            QrCodeUser.open_id.in_(open_ids),
            QrCodeUser.qrcode_id==Qrcode.id
            )
        rows    = db.session.query(
            QrCodeUser.open_id, Qrcode.promoter_id).join(Qrcode, join_query).all()
        promoters = Promoter.query.all()
        promoter_parent_map = {}
        promoter_name_map   = {}
        for p in promoters:
            if p.create_by:
                promoter_parent_map[p.id] = p.create_by
            promoter_name_map[p.id] = p.name
        result = {}
        for i in rows:
            open_id     = i[0]
            promoter_id = i[1]
            promoter_parent_id = promoter_parent_map.get(promoter_id)
            if promoter_parent_id:
                tmp         = {
                    'promoter': {'id': promoter_id, 'name': promoter_name_map[promoter_id]},
                    'parent'  : {'id': promoter_parent_id, 'name': promoter_name_map[promoter_parent_id]}
                    }
                result[open_id] = tmp
        return result

    @staticmethod
    def set_user_open_id(user_id, open_id):
        count   = QrCodeUser.query.filter(QrCodeUser.open_id==open_id).update({'user_id':user_id})
        db.session.commit()
        return count

    @staticmethod
    def get_user_qrcode_id(user_id):
        user    = QrCodeUser.query.filter(QrCodeUser.user_id==user_id).first()
        if user: return user.qrcode_id




