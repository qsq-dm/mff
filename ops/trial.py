# -*- coding: utf-8 -*-

from sqlalchemy     import and_
from sqlalchemy     import func
from util.sqlerr    import SQL_DUPLICATE
from util.sqlerr    import SQL_DUPLICATE_PHONE
from util.utils     import dt_obj

from models         import db
from models         import Trial
from models         import TrialApply
from models         import TrialComment
from ops.utils      import get_items
from ops.utils      import get_page
from ops.utils      import count_items
from thirdparty.wechat import wechat
from thirdparty.wechat import create_qrcode
from thirdparty.qn   import upload_img
from settings        import celery




class TrialService(object):

    @staticmethod
    def get_trial(trial_id):
        ''' '''
        trial   = Trial.query.filter(Trial.id==trial_id).first()
        if trial: return trial.as_dict()

    @staticmethod
    def get_user_apply(user_id, trial_id):
        ''' '''
        query   = and_(
            TrialApply.user_id==user_id,
            TrialApply.trial_id==trial_id)
        apply   = TrialApply.query.filter(query).first()
        if apply: return apply.as_dict()

    @staticmethod
    def get_trial_applies_by_user_ids(trial_id, user_ids):
        ''' 使用申请 '''
        query   = and_(
            TrialApply.trial_id==trial_id,
            TrialApply.user_id.in_(user_ids)
            )
        applies = TrialApply.query.filter(query).all()
        return [ i.as_dict() for i in applies]

    @staticmethod
    def create_trial(title, image, cat, total, start_time, end_time, rules, process, coupon_id=None):
        ''' 创建试用 '''
        trial   = Trial(
            process=process,
            title=title, image=image, cat=cat, total=total, start_time=start_time, end_time=end_time, rules=rules, coupon_id=coupon_id
            )
        db.session.add(trial)
        db.session.commit()
        return trial.id

    @staticmethod
    def update_trial(item_id, **kw):
        ''' 更新试用 '''
        count       = Trial.query.filter(Trial.id==item_id).update(kw)
        db.session.commit()
        return count

    @staticmethod
    def add_apply(user_id, name, phone, school, trial_id, content, sex, addr):
        try:
            trial   = Trial.query.filter(Trial.id==trial_id).first()
            assert trial, '试用商品不存在'
            cat     = trial.cat
            apply   = TrialApply(
                addr=addr, cat=cat, user_id=user_id, name=name, phone=phone, school=school, trial_id=trial_id, content=content, sex=sex)
            db.session.add(apply)
            db.session.commit()
            return apply.id
        except Exception as e:
            import traceback
            traceback.print_exc()
            db.session.rollback()
            if SQL_DUPLICATE.search(str(e)):
                assert 0, '您已提交过申请'
            assert 0, '申请失败'

    @staticmethod
    def comment(trial_id, user_id, content, photos):
        ''' 试用体会 '''
        comment     = TrialComment(trial_id=trial_id, user_id=user_id, content=content, photos=photos)
        db.session.add(comment)
        db.session.commit()
        return comment.id

    @staticmethod
    def get_paged_trial_comments(**kw):
        return get_page(TrialComment, {}, **kw)

    @staticmethod
    def get_paged_trials(**kw):
        ''' 试用列表 '''
        return get_page(Trial, {}, **kw)

    @staticmethod
    def count_trial(where=None):
        ''' '''
        return count_items(Trial, where)

    @staticmethod
    def count_apply(where=None):
        return count_items(TrialApply, where)

    @staticmethod
    def incr_trial_apply_count(trial_id):
        ''' 试用人气加1 '''
        count = Trial.query.filter(Trial.id==trial_id).update({'apply_count':Trial.apply_count+1})
        db.session.commit()
        return count

    @staticmethod
    def get_paged_apply_user_list(**kw):
        ''' 申请用户列表 '''
        return get_page(TrialApply, {}, **kw)

    @staticmethod
    def update_apply_status(where, to_status):
        ''' 申请状态 '''
        count   = TrialApply.query.filter(where).update({'status':to_status})
        db.session.commit()
        return count

    @staticmethod
    def update_apply(where, **kw):
        ''' '''
        count   = TrialApply.query.filter(where).update(kw)
        db.session.commit()
        return count

    @staticmethod
    def incr_trial_sent_count(trial_id):
        ''' 试用发放数加1 '''
        count   = Trial.query.filter(Trial.id==trial_id).update({'sent':Trial.sent+1})
        db.session.commit()
        return count

    @staticmethod
    def get_apply(apply_id):
        apply   = TrialApply.query.filter(TrialApply.id==apply_id).first()
        if apply: return apply.as_dict()

    @staticmethod
    def get_trial_apply(user_id, trial_id):
        query       = and_(
            TrialApply.user_id==user_id,
            TrialApply.trial_id==trial_id
            )
        apply       = TrialApply.query.filter(query).first()
        if apply: return apply.as_dict()

    @staticmethod
    def get_trial_comment(trial_id, user_id):
        ''' '''
        query       = and_(
            TrialComment.trial_id==trial_id,
            TrialComment.user_id==user_id
            )
        return TrialComment.query.filter(query).first()

    @staticmethod
    def count_user_apply(user_ids, status=None):
        query   = and_()
        query.append(TrialApply.user_id.in_(user_ids))
        if status:
            query.append(TrialApply.status==status)
        rows    = db.session.query(TrialApply.user_id, func.count(TrialApply.id)).filter(query).group_by(TrialApply.user_id).all()
        print rows
        return dict(rows)

    @staticmethod
    def check_exist_order(sort_order):
        query   = and_(
            Trial.sort_order==sort_order,
            Trial.end_time>=dt_obj.now()
            )
        return db.session.query(Trial).filter(query).first()

    @staticmethod
    def get_latest_apply(user_id):
        ''' 获取用户最近一次申请 '''
        apply   = TrialApply.query.filter(TrialApply.user_id==user_id).order_by(TrialApply.id.desc()).first()
        if apply: return apply.as_dict()

    @staticmethod
    def get_trial_apply_by_user_ids(user_ids):
        ''' '''
        applys  = TrialApply.query.filter(TrialApply.user_id.in_(user_ids)).all()
        return [i.as_dict() for i in applys]




