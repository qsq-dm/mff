# -*- coding: utf-8 -*-

from sqlalchemy         import or_
from sqlalchemy         import and_
from sqlalchemy         import func

from util.utils         import dt_obj
from util.utils         import day_delta
from models             import db
from models             import UserCoupon
from models             import Coupon
from ops.utils          import get_page
from ops.utils          import count_items


class CouponService(object):

    @staticmethod
    def create_coupon(coupon_cat, cat_id, title, price, effective, item_id=None, sub_cat_id=None, is_trial=False, need=0):
        coupon      = Coupon(
            item_id=item_id, sub_cat_id=sub_cat_id, title=title, coupon_cat=coupon_cat,
            cat_id=cat_id, price=price, effective=effective, is_trial=is_trial, need=need
            )
        db.session.add(coupon)
        db.session.commit()
        return coupon.id

    @staticmethod
    def update_coupon(coupon_id, **kw):
        count       = Coupon.query.filter(Coupon.id==coupon_id).update(kw)
        db.session.commit()
        return count

    @staticmethod
    def send_user_coupon(user_id, coupon_id):
        now         = dt_obj.now()
        coupon      = Coupon.query.filter(Coupon.id==coupon_id).first()

        price       = coupon.price
        effective   = coupon.effective
        coupon_cat  = coupon.coupon_cat
        cat_id      = coupon.cat_id
        sub_cat_id  = coupon.sub_cat_id
        item_id     = coupon.item_id
        title       = coupon.title
        need        = coupon.need
        is_trial    = coupon.is_trial
        user_coupon = UserCoupon(
            title                   =   title,
            is_trial                =   is_trial,
            remark                  =   coupon.remark,
            user_id                 =   user_id,
            price                   =   price,
            need                    =   need,
            cat_id                  =   cat_id,
            coupon_cat              =   coupon_cat,
            item_id                 =   item_id,
            sub_cat_id              =   sub_cat_id,
            coupon_id               =   coupon_id,
            end_time                =   now + day_delta*(effective/86400),
            create_time             =   now,
            )
        db.session.add(user_coupon)
        db.session.commit()
        return user_coupon.id

    @staticmethod
    def cat_query(cat_id_list):
        cat_query   = or_()
        for cat_id in cat_id_list or []:
            tmp     = and_(
                UserCoupon.cat_id==cat_id,
                UserCoupon.coupon_cat==1
                )
            cat_query.append(tmp)
        return cat_query

    @staticmethod
    def sub_cat_query(sub_cat_id_list):
        sub_cat_query = or_()
        for sub_cat_id in sub_cat_id_list or []:
            tmp     = and_(
                UserCoupon.sub_cat_id==sub_cat_id,
                UserCoupon.coupon_cat==2
                )
            sub_cat_query.append(tmp)
        return sub_cat_query

    @staticmethod
    def get_user_coupon(user_coupon_id, user_id=None, item_id=None, cat_id_list=None, sub_cat_id_list=None, item_price=None):
        ''' '''
        cat_query       = CouponService.cat_query(cat_id_list)
        sub_cat_query   = CouponService.sub_cat_query(sub_cat_id_list)        

        query = and_()
        if item_id:
            or_query    = or_(
                UserCoupon.coupon_cat==0,
                sub_cat_query,
                cat_query,
                and_(
                    UserCoupon.coupon_cat==3,
                    UserCoupon.item_id==item_id
                    )
                )
        else:
            or_query    = None
        query.append(and_(
            UserCoupon.id==user_coupon_id,
            UserCoupon.status==0,
            UserCoupon.end_time>dt_obj.now(),
            ))
        if or_query is not None:
            query.append(or_query)
        if user_id: query.append(UserCoupon.user_id==user_id)
        where           = or_(
            and_(
                query,
                UserCoupon.need==0
                ),
            and_(
                query,
                UserCoupon.need<=item_price
                )
            )
        return UserCoupon.query.filter(where).first()

    @staticmethod
    def get_user_coupon_by_id(user_coupon_id):
        coupon  = UserCoupon.query.filter(UserCoupon.id==user_coupon_id).first()
        if coupon: return coupon.as_dict()

    @staticmethod
    def get_paged_user_coupons(**kw):
        return get_page(UserCoupon, {}, **kw)

    @staticmethod
    def count_coupon(where):
        return db.session.query(func.count(UserCoupon.id)).filter(where).scalar()

    @staticmethod
    def update_user_coupon_status(where, status):
        count       = UserCoupon.query.filter(where).update({'status':status})
        db.session.commit()
        return count

    @staticmethod
    def get_paged_coupons(**kw):
        return get_page(Coupon, {}, **kw)

    @staticmethod
    def count(where):
        return count_items(Coupon, where)

    @staticmethod
    def get_coupon(coupon_id):
        ''' '''
        coupon      = Coupon.query.filter(Coupon.id==coupon_id).first()
        if coupon:
            return coupon.as_dict()

    @staticmethod
    def get_coupon_by_ids(coupon_ids):
        ''' '''
        coupons     = Coupon.query.filter(Coupon.id.in_(coupon_ids)).all()
        return [ i.as_dict() for i in coupons]

    @staticmethod
    def resend_user_coupon(from_id, to_id, user_coupon_id):
        ''' 转赠优惠券 '''
        query       = and_(
            UserCoupon.user_id==from_id,
            UserCoupon.id==user_coupon_id,
            UserCoupon.status==0
            )
        coupon      = UserCoupon.query.filter(query).first()
        assert coupon, '优惠券不存在'
        assert coupon.status==0 and coupon.end_time>=dt_obj.now(), '优惠券已使用或已过期'

        count       = UserCoupon.query.filter(query).update({'status':1})
        db.session.commit()
        assert count, '优惠券已使用或已过期'

        copy_coupon    = coupon.as_dict()
        copy_coupon['user_id'] = to_id
        copy_coupon['status']  = 0
        copy_coupon.pop('id')
        new_coupon     = UserCoupon(**copy_coupon)
        db.session.add(new_coupon)
        db.session.commit()
        return count

