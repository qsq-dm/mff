# -*- coding: utf-8 -*-
import math
from collections import defaultdict
from sqlalchemy import and_
from sqlalchemy import or_

from flask import request
from flask import redirect
from flask import Blueprint
from flask import render_template
from flask import make_response

from util.utils      import jsonify_response
from util.utils      import template_response
from util.utils      import abbreviated_pages
from util.sign       import gen_promote_token
from util.sign       import del_cookie
from util.sign       import set_cookie
from util.decorators import hospital_dec
from util.decorators import promote_dec
from util.validators import Optional
from util.validators import Inputs
from util.validators import MobileField
from util.validators import TextField
from util.validators import IdField
from util.validators import IntChoiceField
from util.validators import MobileField
from models          import db
from models          import Order
from models          import User
from models          import ItemCat
from models          import Item
from models          import ItemSubCat
from models          import ServiceCode
from models          import Promoter
from ops.promote     import PromoteService
from ops.data        import DataService
from ops.item        import ItemService
from ops.comment     import CommentService
from ops.user        import UserService
from ops.order       import OrderService
from ops.bulks       import fetch_credit_refs
from ops.bulks       import fetch_user_refs
from ops.bulks       import fetch_item_refs
from ops.bulks       import fetch_servicecode_refrence
from constants       import ResponseCode
from constants       import ORDER_STATUS
from constants       import SERVICE_STATUS
from thirdparty.wechat  import create_qrcode


@promote_dec(required=True)
def index():
    ''' 首页 '''
    return 'promote'

@promote_dec(required=False)
def login():
    ''' 登录 '''
    return render_template('promote/login.html')


login_post_validator  = Inputs(
    {
     'name'         : TextField(min_length=1, max_length=100, msg='请输入账号'),
     'passwd'       : TextField(min_length=1, max_length=100, msg='请输入密码')
    }
    )
@promote_dec(required=False, validator=login_post_validator)
def login_post():
    ''' 登录 '''
    name   = request.valid_data.get('name')
    passwd = request.valid_data.get('passwd')
    if PromoteService.check_user(name, passwd):
        response    = jsonify_response({'code':ResponseCode.SUCCESS}, with_response=True)
        token       = gen_promote_token(name)
        set_cookie(response, 'promote_sign', token, 86400*30)
        return response
    assert 0, '用户名或密码错误'



create_promoter_validator  = Inputs(
    {
     'name'         : TextField(min_length=1, max_length=100, msg='请输入用户名'),
     'phone'        : TextField(min_length=1, max_length=100, msg='手机号码')
    }
    )
@promote_dec(required=True, validator=create_promoter_validator)
def create_promoter():
    ''' 创建推广员 '''
    name            = request.valid_data.get('name')
    phone           = request.valid_data.get('phone')
    passwd          = ''
    creator         = PromoteService.get_promoter_by_phone(request.name)
    assert creator, '请登录'
    create_by       = creator.id
    status          = 2
    promoter_id     = PromoteService.create_promoter(phone, passwd, name, create_by, status=status)
    assert promoter_id, '创建失败'
    qrcode_id       = PromoteService.create_promoter_qrcode(promoter_id)
    PromoteService.download_promoter_qrcode.delay(qrcode_id)

    result          = {
        'code'          : ResponseCode.SUCCESS,
        'msg'           : '创建成功'
        }
    return jsonify_response(result)



@promote_dec(required=True)
def get_promoter_list():
    ''' 推广人员列表 '''
    creator         = PromoteService.get_promoter_by_phone(request.name)
    assert creator, '请登录'
    phone         = request.args.get('phone')
    sort_type     = int(request.args.get('sort_type') or 0)
    _sort_dir     = int(request.args.get('_sort_dir') or 0)
    sort_map      = {
        1         : 'follow_count',
        2         : 'reg_count'
    }
    _sort         = sort_map.get(sort_type)
    if _sort_dir:
        _sort_dir = 'ASC' #升序
    else:
        _sort_dir = 'DESC' #降序

    print phone, 'phone'
    page          = int(request.args.get('page', 1) or 1)
    limit         = 5
    start         = (page-1)*limit
    where         = None
    filters       = [Promoter.create_by==creator.id]
    filters.append(Promoter.status!=0) #过滤掉已被删除的
    if phone:
        filters.append(Promoter.phone==phone)
    if filters: where = and_(*filters)

    total         = PromoteService.count_promoters(where)
    page_info     = abbreviated_pages(int(math.ceil(total/(limit*1.0))), page)
    has_more, item_list = PromoteService.get_paged_promoters(
        _sort=_sort, _sort_dir=_sort_dir, limit=limit, start=start, where=where)

    promoter_ids    = [i['id'] for i in item_list]
    qrcodes         = PromoteService.get_promoter_qrcodes_by_promoter_ids(promoter_ids)
    promoter_map    = {i['promoter_id']:i['image'] for i in qrcodes}
    for item in item_list:
        item['image']    = promoter_map.get(item['id']) or ''
    result               = {
        'infos'             : item_list,
        'page_info'         : page_info,
        'total'             : total,
        'creator'           : creator,
        'phone'             : phone,
        'page'              : page,
        'sort_type'         : sort_type,
        '_sort_dir'         : _sort_dir
        }

    if request.args.get('json'):
        return jsonify_response(result)
    return render_template('promote/index.html',**result)



def logout():
    try:
        response = redirect('/promote/login/')
        del_cookie(response, 'promote_sign')
        return response
    except:
        import traceback
        traceback.print_exc()
        return 'server error'




del_promoter_validator  = Inputs(
    {
     'promoter_id'         : IdField(msg='请输入推广员id'),
    }
    )
@promote_dec(required=True, validator=del_promoter_validator)
def del_promoter():
    ''' 删除推广员 '''
    promoter_id     = request.valid_data.get('promoter_id')
    count           = PromoteService.del_promoter(promoter_id)

    msg             = '删除成功'
    result          = {
        'code'  : ResponseCode.SUCCESS,
        'msg'   : msg
        }

    return jsonify_response(result)



