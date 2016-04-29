# -*- coding: utf-8 -*-

from sqlalchemy         import and_

from models             import db
from models             import Article
from models             import Notification

from util.utils         import dt_obj
from util.utils         import date_to_datetime
from ops.utils          import get_page
from ops.utils          import count_items
from ops.utils          import get_items


class NotificationService(object):
    ''' 通知 '''

    @staticmethod
    def create_article(title, image, desc, link):
        article     = Article(title=title, image=image, desc=desc, link=link)
        db.session.add(article)
        db.session.commit()
        return article.id

    @staticmethod
    def send_notification(article_id, user_id):
        notification = Notification(article_id=article_id, user_id=user_id)
        db.session.add(notification)
        db.session.commit()
        return notification.id

    @staticmethod
    def mark_read(notification_id):
        query    = and_(
            Notification.id==notification_id,
            Notification.status==0
            )
        count    = Notification.query.filter(query).update({'status':1})
        db.session.commit()
        return count

    @staticmethod
    def count_unread(user_id):
        ''' 未读消息计数 '''
        where   = and_(
            Notification.user_id==user_id,
            Notification.status==0
            )
        return count_items(Notification, where)

    @staticmethod
    def get_paged_notification_list(**kw):
        return get_page(Notification, {}, **kw)

    @staticmethod
    def get_articles_by_ids(article_ids):
        return get_items(Article, article_ids)
