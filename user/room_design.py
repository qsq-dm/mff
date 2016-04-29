# -*- coding: utf-8 -*-

from flask import request
from flask import redirect
from flask import render_template
from flask import send_from_directory

from sqlalchemy      import and_
from sqlalchemy      import or_
from models          import db
from models          import School
from models          import RoomDesignDetail
from util.utils      import jsonify_response
from util.utils      import random_str
from util.utils      import str_to_int_list
from util.utils      import comma_str_to_list
from util.decorators import wechat_loggin_dec
from util.validators import Optional
from util.validators import Inputs
from util.validators import MobileField
from util.validators import TextField
from util.validators import IdField
from util.validators import IntChoiceField
from util.sign       import sign_user
from util.sign       import set_cookie
from util.sign       import del_cookie
from ops.bulks       import fetch_user_refs
from ops.item        import ItemService
from ops.data        import DataService
from ops.user        import UserService
from ops.redpack     import RedpackService
from ops.promote     import PromoteService
from ops.cache       import RoomDesignVoteCounter
from ops.room_design import RoomDesignService
from constants       import ResponseCode
from thirdparty.sms  import send_sms
from thirdparty.sms  import gen_vcode
from thirdparty.wechat      import exchange_code_for_token
from settings               import MAX_TODAY_PASSWD_ATTEMPT
from settings               import MAX_TODAY_VCODE_ATTEMPT
from settings               import CONTACT
from constants              import VOTE_COUNT_SOURCE_MAP




def set_tip_msg(rank, is_myself=True):
    ''' 票数文案 '''
    rank_50     = RoomDesignVoteCounter.get_vote_by_rank(50) or 0
    vote        = RoomDesignVoteCounter.get_vote_by_rank(rank) or 0
    dif         = rank_50 - vote
    if not is_myself:
        dif     = (RoomDesignVoteCounter.get_vote_by_rank(rank-1) - vote) if rank >1 else 0
        if rank==1:
            return '第一名'
        else:
            return '距离上一名还差{}票'.format(dif)
    if rank>50:
        if dif < 500:
            return '您只差{}票就可以获得入围大礼包了哦，加油！'.format(dif)
        if dif > 500:
            vote_firends    = dif/50
            return '您距离入围大礼包只差{}-{}个好友来帮忙咯'.format(vote_firends, vote_firends*2)
    elif 21<rank<50:
        dif     = RoomDesignVoteCounter.get_vote_by_rank(rank-1) - vote
        if dif < 500:
            return '距您上一名还差{}票'.format(dif)
        if dif > 500:
            vote_firends    = dif/50
            return '您距离入围大礼包只差{}-{}个好友来帮忙咯'.format(vote_firends, vote_firends*2)
    else:
        dif     = RoomDesignVoteCounter.get_vote_by_rank(1) - vote
        if dif < 500:
            return '您距离2000元红包只差{}票了哦'.format(dif)
        if dif > 500:
            vote_firends    = dif/50
            return '您距离2000元红包只差{}-{}个好友来帮忙咯'.format(vote_firends, vote_firends*2)
        
        
        

room_detail_validator  = Inputs(
    {
     'room_id'    : IdField(msg='请输入寝室id'),
    }
)
@wechat_loggin_dec(required=False, validator=room_detail_validator, app=True)
def get_room_detail():
    ''' 获取寝室详情 '''
    room_id     = request.valid_data.get('room_id')
    user        = RedpackService.get_qruser_by_openid(request.open_id)
    has_followed= bool(user and user.nickname)
    privileges  = None
    if request.user_id:
        privileges  = RoomDesignService.get_user_vote_privilede(request.user_id)

    room        = RoomDesignService.get_room_dict_by_id(room_id)
    assert room, '寝室不存在'
    is_myself   = room['user_id'] == request.user_id
    vote_count  = RoomDesignVoteCounter.incr(room['id'], 0)
    rank        = RoomDesignVoteCounter.rank(room['id'])
    pre_diff    = RoomDesignVoteCounter.get_vote_by_rank(rank-1)-vote_count if rank>1 else 0
    room['rank']= rank
    where       = RoomDesignDetail.user_id==request.user_id
    has_attend  = bool(RoomDesignService.get_room(where))

    note        = set_tip_msg(rank, is_myself) if rank else ''
    result      = {
        'code'      : ResponseCode.SUCCESS,
        'msg'       : '寝室详情',
        'has_followed': has_followed,
        'room'      : room,
        'note'      : note,
        'vote_count': vote_count,
        'privileges': privileges,
        'pre_diff'  : pre_diff,
        'has_attend': has_attend,
        'is_myself' : is_myself
    }
    return jsonify_response(result)


apply_room_validator  = Inputs(
    {
     'school_id'    : IdField(msg='请选择学校'),
     'phone'        : MobileField(min_length=1, max_length=100, msg='请输入手机号'),
     'room_name'    : TextField(min_length=1, max_length=100, msg='请给您的寝室取一个独一无二的名字'),
     'applyer_name' : TextField(min_length=1, max_length=100, msg='请输入参赛者的名字'),
     'addr'         : TextField(min_length=1, max_length=100, msg='请输入地址'),
    }
)
@wechat_loggin_dec(required=True, validator=apply_room_validator, app=True)
def apply_room():
    phone       = request.valid_data.get('phone')
    school_id   = request.valid_data.get('school_id')
    room_name   = request.valid_data.get('room_name')
    applyer_name= request.valid_data.get('applyer_name')
    addr        = request.valid_data.get('addr')

    apply_no    = RoomDesignVoteCounter.incr_apply_no()
    pics        = None

    where       = RoomDesignDetail.user_id==request.user_id
    my_room     = RoomDesignService.get_room(where)
    
    has_attend  = bool(my_room)
    assert not has_attend, '您已参与过了'

    room_id     = RoomDesignService.create_room(request.user_id, room_name, applyer_name, apply_no, phone, addr, school_id, pics)
    RoomDesignVoteCounter.add_score(0)
    result      = {
        'code'     : ResponseCode.SUCCESS,
        'msg'      : '',
        'room_id'  : room_id
        }
    return jsonify_response(result)


room_list_validator = Inputs(
    {
     'school_id': Optional(IdField(msg='请选择学校')),
     'cat'      : IntChoiceField(choices=[1,2], msg='列表类型'), #1最新参与  2全部排名
     'offset'   : Optional(TextField(min_length=0, max_length=100, msg='请输入分页参数')),
    })
@wechat_loggin_dec(required=False, validator=room_list_validator, app=True)
def room_list():
    cat         = request.valid_data.get('cat')
    offset      = request.valid_data.get('offset')
    school_id   = request.valid_data.get('school_id')

    where       = None
    filters     = []
    if cat==1:
        _sort   = 'id'
        if offset: filters.append(RoomDesignDetail.id<offset)
    elif cat==2:
        _sort   = 'vote_count'
        if offset and len((offset or '').split('_'))==2: #挺烦的分页
            vote_count, offset_id = (offset or '').split('_')
            query                 = or_(
                and_(
                    RoomDesignDetail.vote_count==vote_count,
                    RoomDesignDetail.id<offset_id
                    ),
                and_(
                    RoomDesignDetail.vote_count<vote_count
                    )
                )
            filters.append(query)
    if school_id:
        filters.append(RoomDesignDetail.school_id==school_id)
    filters.append(RoomDesignDetail.pics_count>0)
    if filters: where = and_(*filters)
    has_more, rooms = RoomDesignService.get_paged_rooms(where=where, _sort=_sort) 
    for room in rooms:
        room['rank']    = RoomDesignVoteCounter.rank(room['id'])
        rank            = room['rank']
        vote_count      = RoomDesignVoteCounter.incr(room['id'], 0)
        pre_diff        = RoomDesignVoteCounter.get_vote_by_rank(rank-1)-vote_count if rank>1 else 0
        room['note']    = set_tip_msg(rank, is_myself=False)
        room['pre_diff']= pre_diff

    offset      = ''
    if rooms:
        if cat==1:
            offset  = str(rooms[-1]['id'])
        else:
            offset  = '{}_{}'.format(str(rooms[-1]['vote_count']), str(rooms[-1]['id']))

    result      = {
        'code'      : ResponseCode.SUCCESS,
        'msg'       : '',
        'infos'     : rooms,
        'has_more'  : has_more,
        'offset'    : offset
        }
    return jsonify_response(result)


add_room_pics_validators = Inputs(
    {
     'room_id'    : IdField(msg='请选择寝室'),
     'pics'      : TextField(min_length=1, max_length=100, msg='逗号分隔的图片链接字符串'), 
    })
@wechat_loggin_dec(required=True, validator=add_room_pics_validators)
def add_room_pics():
    ''' 添加寝室图片 '''
    pics    = request.valid_data.get('pics')
    room_id = request.valid_data.get('room_id')
    where   = RoomDesignDetail.id==room_id

    room    = RoomDesignService.get_room_dict_by_id(room_id)
    assert room, '寝室不存在'

    pic_list = comma_str_to_list(pics)
    assert len(pic_list), '请上传图片'
    #assert len(pic_list)==4, '必须上传4张图'
    pics_count=len(filter(bool, pic_list))
    count   = RoomDesignService.update_room(where, pics=pics, pics_count=pics_count)

    RoomDesignService.set_school_pics_count(room['school_id'])

    result  = {
        'code' : ResponseCode.SUCCESS,
        'msg'  : '添加成功'
    }
    return jsonify_response(result)



school_rooms_validator = Inputs(
    {
     'offset'      : Optional(TextField(min_length=0, max_length=100, msg='分页参数')), 
    })
@wechat_loggin_dec(required=False, validator=school_rooms_validator, app=True)
def school_rooms():
    ''' 学校风采 '''
    offset      = request.valid_data.get('offset')
    where       = and_(
        School.city_name=='上海',
        School.pics_count>0
        )

    limit               = 100
    fields              = ['id', 'name']
    has_more, schools   = DataService.get_paged_schools(where=where, fields=fields, limit=limit)

    for i in schools:
        i['count']      = RoomDesignService.count_school_pics(i['id'])
    offset      = ''
    if schools:
        offset  = str(schools[-1]['id'])
    result      = {
        'code'     : ResponseCode.SUCCESS,
        'msg'      : '',
        'infos'    : schools,
        'has_more' : has_more,
        'offset'   : offset
    }
    return jsonify_response(result)


vote_room_validator = Inputs(
    {
     'room_id'    : IdField(msg='请选择寝室'),
     'source'     : IntChoiceField(choices=[1,2,3], msg='投票类型'), #1申请额度通过 2成功完成一单 3普通投票
    })
@wechat_loggin_dec(required=True, validator=vote_room_validator, app=True)
def vote_room():
    ''' 投票 '''
    room_id         = request.valid_data.get('room_id')
    source          = request.valid_data.get('source')

    privileges      = RoomDesignService.get_user_vote_privilede(request.user_id)

    privilege_map   = {i['id']:i['status'] for i in privileges}

    assert privilege_map[source]!=1, '您已投过了'
    assert privilege_map[source]!=-1, '您没有投票机会，快去申请额度或下单吧'

    current_score   = RoomDesignVoteCounter.incr(room_id, 0)
    count           = 1
    if source!=3:
        count           = RoomDesignService.update_vote_privilege_status(request.user_id, source)
    vote_count      = VOTE_COUNT_SOURCE_MAP[source]

    if count:
        RoomDesignService.incr_room_vote(room_id, vote_count)
        RoomDesignVoteCounter.incr(room_id, vote_count)
        RoomDesignService.add_vote_log(room_id, request.user_id, source)

    if not RoomDesignVoteCounter.exists_score(current_score):
        if current_score>0: RoomDesignVoteCounter.remove_score(current_score)
    current_score   = RoomDesignVoteCounter.incr(room_id, 0)
    RoomDesignVoteCounter.add_score(current_score)
    result          = {
        'code'         : ResponseCode.SUCCESS,
        'msg'          : '投票成功'
    }
    return jsonify_response(result)


@wechat_loggin_dec(required=False)
def room_index():
    ''' 活动首页 '''
    limit       = 2
    first       = []
    second      = []
    third       = []

    user        = RedpackService.get_qruser_by_openid(request.open_id)
    has_followed= bool(user and user.nickname)

    where       = RoomDesignDetail.user_id==request.user_id
    my_room     = RoomDesignService.get_room(where)
    
    has_attend  = bool(my_room)
    if my_room: my_room = my_room.as_dict()
    _sort       = 'id'
    where       = RoomDesignDetail.pics_count>0
    has_more, first  = RoomDesignService.get_paged_rooms(_sort=_sort, limit=limit, where=where)
    _sort       = 'vote_count'
    has_more, second = RoomDesignService.get_paged_rooms(_sort=_sort, limit=limit, where=where) 

    where       = and_(
        School.city_name=='上海',
        School.pics_count>0
        )
    _, schools  = DataService.get_paged_schools(where=where, limit=4, fields=['id', 'name'])
    for i in schools:
        i['count'] = RoomDesignService.count_school_pics(i['id'])

    for room in first+second:
        room['rank']    = RoomDesignVoteCounter.rank(room['id'])
        rank            = room['rank']
        vote_count      = RoomDesignVoteCounter.incr(room['id'], 0)
        pre_diff        = RoomDesignVoteCounter.get_vote_by_rank(rank-1)-vote_count if rank>1 else 0
        room['note']    = set_tip_msg(rank, is_myself=False)
        room['pre_diff']= pre_diff
    result      = {
        'code'      : ResponseCode.SUCCESS,
        'msg'       : '',
        'has_followed': has_followed,
        'my_room'   : my_room,
        'first'     : first,
        'second'    : second,
        'third'     : schools,
        'has_attend': has_attend
        }
    return jsonify_response(result)



room_search_validator = Inputs(
    {
     'keyword'   : TextField(min_length=1, max_length=100, msg='请输入关键字'),
    })
@wechat_loggin_dec(required=False, validator=room_search_validator, app=True)
def room_search():
    ''' 搜索寝室 '''
    keyword     = request.valid_data.get('keyword')

    where       = or_(
        RoomDesignDetail.phone==keyword,
        RoomDesignDetail.room_name==keyword,
        RoomDesignDetail.apply_no==keyword
        )
    room        = RoomDesignService.get_room(where)
    room_id     = None
    if room: room_id = room.id
    room_exist  = bool(room)
    result      = {
        'code'      : ResponseCode.SUCCESS,
        'msg'       : '',
        'room_exist': room_exist,
        'room_id'   : room_id
        }
    return jsonify_response(result)


@wechat_loggin_dec(required=True)
def get_vote_priviledges():
    ''' 用户投票机会详情 '''
    user        = RedpackService.get_qruser_by_openid(request.open_id)
    has_followed= bool(user and user.nickname)

    privileges  = RoomDesignService.get_user_vote_privilede(request.user_id)

    result      = {
        'code'      : ResponseCode.SUCCESS,
        'msg'       : '',
        'has_followed': has_followed,
        'privileges': privileges,
    }
    return jsonify_response(result)





@wechat_loggin_dec(required=False, need_openid=True)
def room_about():
    print 'room_about'
    return send_from_directory('static', 'user/Activities/about.html')










