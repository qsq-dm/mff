# -*- coding: utf-8 -*-

from sqlalchemy         import and_
from sqlalchemy         import func
from models             import db
from models             import ItemComment
from models             import Item
from models             import Hospital
from ops.utils          import get_page
from ops.utils          import get_items
from util.utils         import format_rate


class CommentService(object):

    @staticmethod
    def comment_item(item_id, user_id, content, photos, rate, is_anonymous, order_id, is_re_comment=False):
        ''' 评价商品 '''
        comment     = ItemComment(
            item_id=item_id, user_id=user_id,
            content=content, photos=photos, rate=rate,
            order_id=order_id,
            is_anonymous=is_anonymous,
            is_re_comment=is_re_comment)
        db.session.add(comment)
        db.session.commit()
        return comment.id

    @staticmethod
    def count_comments(where):
        return db.session.query(func.count(ItemComment.id)).filter(where).scalar()

    @staticmethod
    def get_paged_comments(**kw):
        return get_page(ItemComment, **kw)

    @staticmethod
    def get_comments_by_item_ids(item_ids, user_id=None, **kw):
        query = and_(
            ItemComment.user_id==user_id,
            ItemComment.item_id.in_(item_ids)
            )
        rows    = ItemComment.query.filter(query).all()
        return [i.as_dict() for i in rows]

    @staticmethod
    def get_comments_by_order_ids(order_ids, user_id=None, **kw):
        query = and_(
            ItemComment.user_id==user_id,
            ItemComment.order_id.in_(order_ids)
            )
        rows    = ItemComment.query.filter(query).all()
        return [i.as_dict() for i in rows]

    @staticmethod
    def get_comment(where):
        return ItemComment.query.filter(where).first()

    @staticmethod
    def rerate_hospital(hospital_id):
        comment_id_suq     = db.session.query(Item.id).filter(Item.hospital_id==hospital_id).subquery()
        result             = db.session.query(func.count(), func.sum(ItemComment.rate)).filter(ItemComment.item_id.in_(comment_id_suq)).all()
        if result:
            rate           = format_rate(result[0][1]/result[0][0] if result[0][0] else 0)
        else:
            rate           = format_rate(rate)
        Hospital.query.filter(Hospital.id==hospital_id).update({'rate':rate})
        db.session.commit()
        return rate

        


