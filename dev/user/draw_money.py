# -*- coding: utf-8 -*-

from flask import request
from flask import redirect
from flask import render_template

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
from util.drawgift   import draw_prize
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





@wechat_loggin_dec(required=False)
def draw_index():
    ''' '''
    if request.user_id and not PromoteService.get_rd_user(request.user_id):
        PromoteService.create_rd_user(request.user_id)

    user        = RedpackService.get_qruser_by_openid(request.open_id)
    has_followed= bool(user and user.nickname)
    invite_count    = PromoteService.get_reg_count(request.user_id)
    priviledges     = PromoteService.get_draw_logs(request.user_id)
    draw_count      = PromoteService.get_user_can_draw_count(request.user_id)
    result      = {
        'code'      : ResponseCode.SUCCESS,
        'msg'       : '',
        'has_followed': has_followed,
        'invite_count': invite_count,
        'draw_count'    : draw_count,
        'priviledges'   : priviledges
        }
    return jsonify_response(result)



@wechat_loggin_dec(required=True, app=True)
def draw_money():
    ''' 抽奖 '''
    prize_list  = PromoteService.get_prize_left()
    prize_map   = dict(prize_list)
    prize_id    = draw_prize(prize_list)
    if not prize_id:
        result  = {
            'code': ResponseCode.SERVER_ERROR,
            'msg': '奖品已被抽完'
        }
        return jsonify_response(result)

    prize       = PromoteService.get_prize(prize_id)
    current_count = prize_map[prize_id]
    count       = PromoteService.incr_draw_used(request.user_id)
    if not count:
        assert 0, '您没有抽奖机会了'
    count       = PromoteService.incr_prized(prize_id, current_count)
    if not count:
        remain  = PromoteService.get_prize_remain(prize_id)
        if not remain:
            result  = {
                'code': ResponseCode.SERVER_ERROR,
                'msg': '奖品已被抽完'
            }
            return jsonify_response(result)
        else:
            result  = {
                'code': ResponseCode.SERVER_ERROR,
                'msg': '服务器忙'
            }
            return jsonify_response(result)
    result      = {
        'code'      : ResponseCode.SUCCESS,
        'msg'       : '',
        'prize_id'  : prize_id,
        'amount'    : prize.amount
        }
    return jsonify_response(result)






