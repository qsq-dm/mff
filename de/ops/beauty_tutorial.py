# -*- coding: utf-8 -*-

from sqlalchemy         import and_
from sqlalchemy         import func
from models             import db
from models             import RecommendBeautyItem
from models             import BeautyEntry
from models             import DailyUser
from models             import DailyCoupon
from ops.utils          import get_page
from ops.utils          import get_items
from ops.utils          import count_items
from util.utils         import format_rate


class TutorialService(object):

    @staticmethod
    def create_tutorial_entry(title, icon, image, photo, items):
        ''' '''
        entry   = BeautyEntry(title=title, icon=icon, image=image, photo=photo, items=items)
        db.session.add(entry)
        db.session.commit()
        return entry.id

    @staticmethod
    def update_tutorial_entry(item_id, **kw):
        count   = BeautyEntry.query.filter(BeautyEntry.id==item_id).update(kw)
        db.session.commit()
        db.session.commit()

    @staticmethod
    def set_tutorial_status(item_id, status):
        count   = BeautyEntry.query.filter(BeautyEntry.id==item_id).update({'status':status})
        db.session.commit()
        return count

    @staticmethod
    def get_daily_coupon(daily_id):
        ''' '''
        daily   = DailyCoupon.query.filter(DailyCoupon.id==daily_id).first()
        if daily: return daily.as_dict()

    @staticmethod
    def create_daily_coupon(title, coupon_id, start_time, end_time, total, use_time, use_condition):
        daily   = DailyCoupon(
            title=title,
            coupon_id=coupon_id,
            start_time=start_time,
            end_time=end_time,
            total=total,
            use_time=use_time,
            use_condition=use_condition
            )
        db.session.add(daily)
        db.session.commit()
        return daily.id

    @staticmethod
    def update_daily_coupon(daily_id, **kw):
        ''' '''
        count   = DailyCoupon.query.filter(DailyCoupon.id==daily_id).update(kw)
        db.session.commit()
        return count

    @staticmethod
    def get_paged_tutorial_entries(**kw):
        return get_page(BeautyEntry, {}, **kw)

    @staticmethod
    def get_paged_daily_coupons(**kw):
        return get_page(DailyCoupon, {}, **kw)

    @staticmethod
    def count_daily_coupons(where=None):
        return count_items(DailyCoupon, where=where)

    @staticmethod
    def count_tutorials(where=None):
        return count_items(BeautyEntry, where=where)

    @staticmethod
    def get_tutorial(item_id):
        tutorial    = BeautyEntry.query.filter(BeautyEntry.id==item_id).first()
        if tutorial: return tutorial.as_dict()

    @staticmethod
    def send_daily_coupon(user_id, daily_id):
        '''  '''
        try:
            log     = DailyUser(user_id=user_id, daily_id=daily_id)
            db.session.add(log)
            db.session.commit()
            return log.id
        except Exception as e:
            import traceback
            traceback.print_exc()
            db.session.rollback()

    @staticmethod
    def get_user_daily_by_ids(user_id, daily_ids):
        query       = and_(
            DailyUser.user_id==user_id,
            DailyUser.daily_id.in_(daily_ids)
            )
        rows        = DailyUser.query.filter(query).all()
        return { i.daily_id:i.user_id for i in rows}

    @staticmethod
    def get_user_daily(user_id, daily_id):
        query       = and_(
            DailyUser.user_id==user_id,
            DailyUser.daily_id==daily_id
            )
        daily   = DailyUser.query.filter(query).first()
        if daily: return daily

    @staticmethod
    def incr_daily_coupon_received(daily_id):
        ''' '''
        query = and_(
            DailyCoupon.id==daily_id,
            DailyCoupon.total>=DailyCoupon.sent+1
            )
        count = DailyCoupon.query.filter(query).update({'sent':DailyCoupon.sent+1})
        db.session.commit()
        return count

    @staticmethod
    def incr_tutorial_view_count(tutorial_id):
        count   = BeautyEntry.query.filter(
                BeautyEntry.id==tutorial_id).update({"view_count":BeautyEntry.view_count+1})
        db.session.commit()
        return count

    @staticmethod
    def get_daily_user_ids(**kw):
        return get_page(DailyUser, {}, **kw)

    @staticmethod
    def count_daily_users(where):
        return count_items(DailyUser, where)





