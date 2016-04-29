# -*- coding: utf-8 -*-


from util.sqlerr    import SQL_DUPLICATE_NAME
from util.sqlerr    import SQL_DUPLICATE_PHONE

from models         import db
from ops.utils      import get_items
from models         import AdminUser


class AdminService(object):

    @staticmethod
    def check_admin(name, passwd):
        admin       = AdminUser.query.filter(AdminUser.name==name).first()
        return admin and admin.passwd==passwd

    @staticmethod
    def create_admin(name, passwd, cat):
        try:
            admin   = AdminUser(name=name, passwd=passwd, cat=cat)
            db.session.add(admin)
            db.session.commit()
            return admin.id
        except Exception as e:
            db.session.rollback()
            if SQL_DUPLICATE_NAME.search(str(e)):
                assert 0, '用户名已存在'
            else:
                import traceback
                traceback.print_exc()

    @staticmethod
    def get_admin(name):
        return AdminUser.query.filter(AdminUser.name==name).first()

    @staticmethod
    def update(where, **kw):
        ''' '''
        count   = AdminUser.query.filter(where).update(kw, synchronize_session='fetch')
        db.session.commit()
        return count









