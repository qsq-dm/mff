# -*- coding: utf-8 -*-

from sqlalchemy     import and_
from sqlalchemy     import or_
from sqlalchemy     import func
from util.sqlerr    import SQL_DUPLICATE
from util.sqlerr    import SQL_DUPLICATE_PHONE
from util.utils     import convert_locaton
from util.utils     import dt_obj

from models         import db
from models         import RedpackQuestion
from models         import RedpackUserQuestion
from models         import RedpackPay
from models         import QrCodeUser
from models         import RedpackPayUser
from ops.utils      import get_items
from ops.utils      import get_page
from ops.utils      import count_items
from ops.cache      import RoomDesignVoteCounter
from thirdparty.qn  import upload_img
from settings       import celery



class RedpackService(object):
    ''' '''

    @staticmethod
    def get_qruser_by_openid(open_id):
        ''' '''
        return QrCodeUser.query.filter(QrCodeUser.open_id==open_id).first()

    @staticmethod
    def create_question(content):
        ''' '''
        question    = RedpackQuestion(content=content)
        db.session.add(question)
        db.session.commit()
        return question.id

    @staticmethod
    def create_user_question(qr_user_id, question_id, question, answer, is_custom, is_random, price):
        ''' '''
        question    = RedpackUserQuestion(
            qr_user_id=qr_user_id, question_id=question_id, question=question, answer=answer, is_custom=is_custom,
            is_random=is_random, price=price)
        db.session.add(question)
        db.session.commit()
        return question.id

    @staticmethod
    def get_user_question_by_id(user_question_id):
        question = RedpackUserQuestion.query.filter(RedpackUserQuestion.id==user_question_id).first()
        if question: return question.as_dict()

    @staticmethod
    def get_question_by_id(question_id):
        question = RedpackQuestion.query.filter(RedpackQuestion.id==question_id).first()
        if question: return question.as_dict()

    @staticmethod
    def count_user_question(qr_user_id):
        where   = RedpackUserQuestion.qr_user_id==qr_user_id
        return count_items(RedpackUserQuestion, where)

    @staticmethod
    def count_redpack(where=None):
        return count_items(RedpackPayUser, where)

    @staticmethod
    def get_paged_user_question(**kw):
        return get_page(RedpackUserQuestion, {}, **kw)

    @staticmethod
    def get_questions_by_ids(question_ids, **kw):
        where    = RedpackQuestion.id.in_(question_ids)
        _, infos = RedpackService.get_paged_redpack_questions(where=where, limit=len(question_ids))
        return infos

    @staticmethod
    def get_pay_by_orderno(order_no):
        ''' '''
        return RedpackPay.query.filter(RedpackPay.order_no==order_no).first()

    @staticmethod
    def update_redpack_pay(where, **kw):
        ''' '''
        count   = RedpackPay.query.filter(where).update(kw, synchronize_session=False)
        db.session.commit()
        return count

    @staticmethod
    def add_redpack_user(pay_id, qr_user_id, user_question_id, price):
        user        = RedpackPayUser(pay_id=pay_id, qr_user_id=qr_user_id, user_question_id=user_question_id, price=price)
        db.session.add(user)
        db.session.commit()
        return user.id

    @staticmethod
    def incr_question_view_count(user_question_id):
        ''' '''
        where       = RedpackUserQuestion.id==user_question_id
        data        = {
            'view_count': RedpackUserQuestion.view_count+1
            }
        count       = RedpackUserQuestion.query.filter(where).update(data)
        db.session.commit()
        return count

    @staticmethod
    def get_question_viewers(**kw):
        ''' 问题答案发红包查看用户列表 '''
        return get_page(RedpackPayUser, {}, **kw)

    @staticmethod
    def add_pay(qr_user_id, user_question_id, order_no, price):
        pay         = RedpackPay(
            qr_user_id=qr_user_id,
            user_question_id=user_question_id,
            order_no=order_no,
            price=price
            )
        db.session.add(pay)
        db.session.commit()
        return pay.id

    @staticmethod
    def get_user_question_viewer(user_question_id, qr_user_id):
        query       = and_(
            RedpackPayUser.user_question_id==user_question_id,
            RedpackPayUser.qr_user_id==qr_user_id
            )
        return RedpackPayUser.query.filter(query).first()

    @staticmethod
    def update_redpack_status(question_id, status):
        ''' '''
        query       = and_(
            RedpackQuestion.id==question_id
            )
        data        = {
            'status':status           
            }
        count       = RedpackQuestion.query.filter(query).update(data, synchronize_session=False)
        db.session.commit()
        return count

    @staticmethod
    def get_paged_redpack_questions(**kw):
        ''' '''
        return get_page(RedpackQuestion, {}, **kw)

    @staticmethod
    def count_redpack_question():
        return count_items(RedpackQuestion, None)
    @staticmethod
    def count_redpack_user_question(where=None):
        return count_items(RedpackUserQuestion, where)

    @staticmethod
    def get_question_viewers(**kw):
        return get_page(RedpackPayUser, {}, **kw)

    @staticmethod
    def get_qr_user_by_ids(qr_user_ids, **kw):
        ''' '''
        where   = QrCodeUser.id.in_(qr_user_ids)
        _, infos = get_page(QrCodeUser, {}, where=where, **kw)
        return infos

    @staticmethod
    def total_money():
        total = db.session.query(
            func.sum(RedpackPayUser.price)
            ).scalar() or 0
        return float(total)

    @staticmethod
    def total_money_group_by_question(question_ids=None):
        query   = db.session.query(RedpackPayUser.user_question_id, func.sum(RedpackPayUser.price))
        if question_ids:
            where = RedpackPayUser.user_question_id.in_(question_ids)
            query = query.filter(where)
        result  = query.group_by(RedpackPayUser.user_question_id).all()
        return dict([(i[0], float(i[1]))for i in result])

    @staticmethod
    def incr_user_question_money(user_question_id, price):
        data   = {
            'money': RedpackUserQuestion.money+price
            }
        count  = RedpackUserQuestion.query.filter(RedpackUserQuestion.id==user_question_id).update(data)
        db.session.commit()
        return count



