# -*- coding: utf-8 -*-

from sqlalchemy         import and_

from models             import db
from models             import ActivityItem
from models             import Activity

from util.utils         import dt_obj
from util.utils         import date_to_datetime
from ops.utils          import get_page
from ops.utils          import count_items
from ops.utils          import get_items


class ActivityService(object):
    ''' 活动 '''

    @staticmethod
    def create_activity(title, desc, start, end):
        start_time  = date_to_datetime(start, '%Y-%m-%d %H:%M')
        end_time    = date_to_datetime(end, '%Y-%m-%d %H:%M')
        activity    = Activity(title=title, desc=desc, start_time=start_time, end_time=end_time)
        db.session.add(activity)
        db.session.commit()
        return activity.id

    @staticmethod
    def del_item_activitys(item_id, activity_id):
        count       = ActivityItem.query.filter(
            and_(
                ActivityItem.item_id==item_id,
                ActivityItem.activity_id!=activity_id
            )).delete()
        db.session.commit()
        return count

    @staticmethod
    def exists_activity_time(begin_time, end_time, ignore_activity_id=None):
        ''' 判断活动是否存在
        返回：
        true  时间重复
        false 时间可以
        '''
        begin_time      = date_to_datetime(begin_time[:16], '%Y-%m-%d %H:%M')
        end_time        = date_to_datetime(end_time[:16], '%Y-%m-%d %H:%M')
        if not ignore_activity_id:
            all_activitys   = Activity.query.all()
        else:
            all_activitys   = Activity.query.filter(Activity.id!=ignore_activity_id).all()
        for act in all_activitys:
            if act.start_time<=begin_time<=act.end_time:
                return True
            if act.start_time<=end_time<=act.end_time:
                return True
        return False

    @staticmethod
    def update_activity(activity_id, **kw):
        count       = Activity.query.filter(Activity.id==activity_id).update(kw)
        db.session.commit()
        return count

    @staticmethod
    def add_activity_item(activity_id, item_id):
        activity_item   = ActivityItem(activity_id=activity_id, item_id=item_id)
        db.session.add(activity_item)
        db.session.commit()

    @staticmethod
    def set_activity_items(activity_id, ids):
        rows        = db.session.query(ActivityItem.item_id).filter(ActivityItem.activity_id==activity_id).all()
        item_ids    = [ i.item_id for i in rows]
        to_del_ids  = set(item_ids) - set(ids)
        to_add_ids  = set(ids) - set(item_ids)
        query       = and_(
            ActivityItem.activity_id==activity_id,
            ActivityItem.item_id.in_(list(to_del_ids))
            )
        if to_del_ids: ActivityItem.query.filter(query).delete(synchronize_session=False)
        db.session.commit()
        for item_id in to_add_ids:
            i   = ActivityItem(item_id=item_id, activity_id=activity_id)
            db.session.add(i)
        db.session.commit()

    @staticmethod
    def get_activity_dict_by_id(item_id):
        activity    = Activity.query.filter(Activity.id==item_id).first()
        if activity: return activity.as_dict()

    @staticmethod
    def rm_activity_item(activity_id, item_id):
        query           = and_(
            ActivityItem.activity_id==activity_id,
            ActivityItem.item_id==item_id
            )
        count           = ActivityItem.query.filter(query).delete()
        db.session.commit()
        return count

    @staticmethod
    def get_paged_activity_items(**kw):
        return get_page(ActivityItem, {}, **kw)

    @staticmethod
    def get_paged_activitys(**kw):
        return get_page(Activity, {}, **kw)

    @staticmethod
    def count_activitys(where=None):
        return count_items(Activity, where=where)

    @staticmethod
    def get_activitys_by_ids(activity_ids):
        return get_items(Activity, activity_ids)

    @staticmethod
    def get_current_activity():
        current_time    = dt_obj.now()
        query           = and_(
            Activity.start_time<current_time,
            Activity.end_time>=current_time
            )
        activity = Activity.query.filter(query).first()
        if activity: return activity.as_dict()
    
    






