# -*- coding: utf-8 -*-

from sqlalchemy     import and_

from util.sqlerr    import SQL_DUPLICATE_NAME
from util.sqlerr    import SQL_DUPLICATE_PHONE

from models         import db
from models         import Item
from ops.utils      import get_items
from ops.utils      import count_items
from ops.utils      import get_page
from models         import HospitalUser


class HospitalService(object):

    @staticmethod
    def check_user(name, passwd):
        admin       = HospitalUser.query.filter(HospitalUser.name==name).first()
        return admin and admin.passwd==passwd

    @staticmethod
    def create_user(name, passwd, hospital_id):
        try:
            admin   = HospitalUser(name=name, passwd=passwd, hospital_id=hospital_id)
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
    def change_passwd(name, new_passwd):
        ''' 修改密码 '''
        count   = HospitalUser.query.filter(HospitalUser.name==name).update({'passwd':new_passwd})
        db.session.commit()
        return count

    @staticmethod
    def get_hospital_sub_cat_ids(hospital_id):
        result  = db.session.query(Item.sub_cat_id).filter(Item.hospital_id==hospital_id).distinct().all()
        return [i.sub_cat_id for i in result]

    @staticmethod
    def get_user_by_name(name):
        return HospitalUser.query.filter(HospitalUser.name==name).first()

    @staticmethod
    def get_paged_hospital_admin_users(**kw):
        return get_page(HospitalUser, {}, **kw)

    @staticmethod
    def count_admin(where=None):
        return count_items(HospitalUser, where=where)




