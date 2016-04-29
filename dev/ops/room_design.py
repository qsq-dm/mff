# -*- coding: utf-8 -*-

from sqlalchemy     import and_
from sqlalchemy     import or_
from sqlalchemy     import func
from util.sqlerr    import SQL_DUPLICATE
from util.sqlerr    import SQL_DUPLICATE_PHONE
from util.utils     import convert_locaton
from util.utils     import dt_obj

from models         import db
from models         import School
from models         import RoomDesignDetail
from models         import RoomDesignVotePrivilege
from models         import RoomDesignVoteLog
from ops.utils      import get_items
from ops.utils      import get_page
from ops.utils      import count_items
from ops.cache      import RoomDesignVoteCounter
from thirdparty.qn  import upload_img
from settings       import celery



class RoomDesignService(object):

    @staticmethod
    def create_room(user_id, room_name, applyer_name, apply_no, phone, addr, school_id, pics):
        try:
            room    = RoomDesignDetail(
                user_id=user_id, room_name=room_name, applyer_name=applyer_name, 
                apply_no=apply_no,
                phone=phone, addr=addr,
                school_id=school_id, pics=pics or None
                )
            db.session.add(room)
            db.session.commit()
            RoomDesignVoteCounter.init(room.id)
            return room.id
        except Exception as e:
            import traceback
            traceback.print_exc()
            db.session.rollback()
            if SQL_DUPLICATE.search(str(e)):
                assert 0, '寝室名或者手机号码或申请编号已存在'

    @staticmethod
    def get_room_dict_by_id(room_id):
        room        = RoomDesignDetail.query.filter(RoomDesignDetail.id==room_id).first()
        if room: return room.as_dict()

    @staticmethod
    def update_room(where, **kw):
        count   = RoomDesignDetail.query.filter(where).update(kw)
        db.session.commit()
        return count

    @staticmethod
    def get_room(where):
        room        = RoomDesignDetail.query.filter(where).first()
        return room

    @staticmethod
    def incr_room_vote(room_id, count):
        ''' 提高投票数 '''
        data        = {
            'vote_count': RoomDesignDetail.vote_count+count
            }
        count       = RoomDesignDetail.query.filter(RoomDesignDetail.id==room_id).update(data)
        db.session.commit()
        return count

    @staticmethod
    def get_paged_rooms(**kw):
        return get_page(RoomDesignDetail, {}, **kw)

    @staticmethod
    def get_user_vote_privilede(user_id):
        privileges  = RoomDesignVotePrivilege.query.filter(RoomDesignVotePrivilege.user_id==user_id).all()
        data        = []
        privileges_id_map = {i.source:i for i in privileges}
        query       = and_(
            RoomDesignVoteLog.user_id==user_id,
            RoomDesignVoteLog.source==3
            )
        vote        = RoomDesignVoteLog.query.filter(query).order_by(RoomDesignVoteLog.id.desc()).first()
        for i in range(1,3):
            privilede = privileges_id_map.get(i)
            if privilede:
                privilege_id    = privilede.id
                privilege_status= privilede.status
            else:
                privilege_id    = i
                privilege_status= -1
            data.append({
                'id'     : i,
                'status' : privilege_status
                })
        if vote and str(vote.create_time)[:10]==str(dt_obj.now())[:10]:
            data.append({
                'id'     : 3,
                'status' : 1
            })
        else:
            data.append({
                'id'     : 3,
                'status' : 0
            })
        return data

    @staticmethod
    def add_user_vote_privilege(user_id, source):
        ''' 给予用户投票特权
        source 1额度投票 2完成订单投票 3普通投票
        '''
        query       = and_(
            RoomDesignVotePrivilege.user_id==user_id,
            RoomDesignVotePrivilege.source==source
            )
        exists      = RoomDesignVotePrivilege.query.filter(query).first()
        if exists: return
        privilege   = RoomDesignVotePrivilege(user_id=user_id, source=source)
        db.session.add(privilege)
        db.session.commit()
        return privilege.id

    @staticmethod
    def update_vote_privilege_status(user_id, source):
        query       = and_(
            RoomDesignVotePrivilege.user_id==user_id,
            RoomDesignVotePrivilege.source==source,
            RoomDesignVotePrivilege.status==0
            )
        count       = RoomDesignVotePrivilege.query.filter(query).update({'status': 1})
        db.session.commit()
        return count

    @staticmethod
    def add_vote_log(room_id, user_id, source):
        log         = RoomDesignVoteLog(room_id=room_id, user_id=user_id, source=source)
        db.session.add(log)
        db.session.commit()
        return log.id

    @staticmethod
    def count_school_pics(school_id):
        where   = and_(
            RoomDesignDetail.school_id==school_id,
            RoomDesignDetail.pics!=None
            )
        return count_items(RoomDesignDetail, where)*4

    @staticmethod
    def count_rooms(where=None):
        ''' '''
        return count_items(RoomDesignDetail, where)
        
    @staticmethod
    def today_voted(user_id):
        ''' '''
        query       = and_(
            RoomDesignVoteLog.user_id==user_id,
            RoomDesignVoteLog.source==3
            )
        vote        = RoomDesignVoteLog.query.filter(query).order_by(RoomDesignVoteLog.id.desc()).first()
        return vote and str(vote.create_time)[:10]==str(dt_obj.now())[:10]

    @staticmethod
    def count_school_pics(school_id):
        ''' '''
        result  = db.session.query(func.sum(RoomDesignDetail.pics_count)).filter(RoomDesignDetail.school_id==school_id).scalar()
        return int(result or 0)

    @staticmethod
    def set_school_pics_count(school_id):
        ''' 参与数'''
        result  = db.session.query(func.sum(RoomDesignDetail.pics_count)).filter(RoomDesignDetail.school_id==school_id).scalar()
        pics_count = int(result or 0)
        data        = {
            'pics_count': pics_count
            }
        count       = School.query.filter(School.id==school_id).update(data)
        db.session.commit()
        return count



