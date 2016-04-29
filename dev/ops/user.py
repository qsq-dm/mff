# -*- coding: utf-8 -*-
import os

from util.sqlerr    import SQL_DUPLICATE_NAME
from util.sqlerr    import SQL_DUPLICATE_PHONE

from models         import db
from models         import User
from models         import Wechat
from models         import CreditApply
from models         import UserAdvice
from models         import EditNameLog
from ops.utils      import get_items
from ops.utils      import get_page
from ops.utils      import count_items


class UserService(object):

    @staticmethod
    def create_user(name, phone, passwd):
        ''' 创建用户 '''
        try:
            user        = User(name=name, phone=phone, passwd=passwd)
            db.session.add(user)
            db.session.commit()
            return user.id
        except Exception as e:
            db.session.rollback()
            if SQL_DUPLICATE_NAME.search(str(e)):
                assert False, '用户名已存在'
            elif SQL_DUPLICATE_PHONE.search(str(e)):
                assert False, '手机号码已存在'
            else:
                import traceback
                traceback.print_exc()
                raise(e)

    @staticmethod
    def update_user(user_id, **kw):
        count   = User.query.filter(User.id==user_id).update(kw)
        db.session.commit()

    @staticmethod
    def get_users_by_ids(user_ids, **kw):
        return get_items(User, user_ids, **kw)

    @staticmethod
    def update_passwd(phone, passwd):
        count   = User.query.filter(User.phone==phone).update({'passwd':passwd})
        db.session.commit()
        return count

    @staticmethod
    def get_user_by_phone(phone):
        user    = User.query.filter(User.phone==phone).first()
        return user

    @staticmethod
    def advice(user_id, content, contact):
        advice  = UserAdvice(user_id=user_id, content=content, contact=contact)
        db.session.add(advice)
        db.session.commit()
        return advice.id
    @staticmethod
    def get_advice_dict_by_id(advice_id):
        advice  = UserAdvice.query.filter(UserAdvice.id==advice_id).first()
        if advice: return advice.as_dict()
    @staticmethod
    def get_paged_user_advices(**kw):
        return get_page(UserAdvice, {}, **kw)
    @staticmethod
    def count_advices(where=None):
        return count_items(UserAdvice, where)

    @staticmethod
    def get_userwechat_by_openid(open_id):
        wechat  = Wechat.query.filter(Wechat.open_id==open_id).first()
        return wechat

    @staticmethod
    def add_wechat(open_id):
        try:
            wechat  = Wechat(open_id=open_id, status=0)
            db.session.add(wechat)
            db.session.commit()
        except Exception as e:
            import traceback
            traceback.print_exc()
            db.session.rollback()

    @staticmethod
    def update_wechat_user(open_id, user_id):
        ''' 登录 '''
        query       = Wechat.open_id==open_id
        count       = Wechat.query.filter(query).update({'status':1, 'user_id':user_id})
        db.session.commit()
        return count

    @staticmethod
    def logout_wechat_user(open_id):
        ''' 退出登录 '''
        query       = Wechat.open_id==open_id
        count       = Wechat.query.filter(query).update({'status':-1})
        db.session.commit()
        return count

    @staticmethod
    def get_user_by_id(user_id):
        ''' '''
        user        = User.query.filter(User.id==user_id).first()
        return user

    @staticmethod
    def get_credit_applies_by_ids(item_ids, **kw):
        where       = CreditApply.user_id.in_(item_ids)
        return get_page(CreditApply, {}, limit=10000, where=where, **kw)[1]

    @staticmethod
    def get_paged_user(**kw):
        return get_page(User, {}, **kw)

    @staticmethod
    def count_user(where=None):
        return count_items(User, where=where)

    @staticmethod
    def update_name(user_id, name):
        ''' 修改名字 '''
        log   = UserService.get_edit_name_log(user_id)
        if os.environ.get('APP_ENV')=='production':
            assert not log, '名字只能修改一次'
        try:
            count = User.query.filter(User.id==user_id).update({'name':name})
            db.session.commit()
            return count
        except Exception as e:
            db.session.rollback()
            if SQL_DUPLICATE_NAME.search(str(e)):
                assert 0, '用户名字已存在'

    @staticmethod
    def get_edit_name_log(user_id):
        return EditNameLog.query.filter(EditNameLog.user_id==user_id).first()

    @staticmethod
    def add_edit_name_log(user_id):
        log         = EditNameLog(user_id=user_id)
        db.session.add(log)
        db.session.commit()




