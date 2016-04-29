# -*- coding: utf-8 -*-

from flask import request
from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

from user.views import user_index
from user.views import item_detail
from user.views import item_list
from user.views import item_filters
from user.views import item_comment_list
from user.views import user_fav_item
from user.views import user_advice
from user.views import user_order_list
from user.views import order_preview
from user.views import confirm_order
from user.views import order_pay
from user.views import repayment_pay
from user.views import wx_pay_callback
from user.views import wx_repayment_callback
from user.views import uploads
from user.views import order_detail
from user.views import comment_post
from user.views import my_period_bill
from user.views import user_home
from user.views import my_repayments
from user.views import item_cats
from user.views import my_favs
from user.views import my_coupons
from user.views import my_apply
from user.views import help
from user.views import repayment
from user.views import get_help_entry
from user.views import apply_credit_page
from user.views import project_doctor_description
from user.views import get_jssdk_js
from user.views import get_school_list
from user.views import hospital_detail
from user.views import get_city_list
from user.views import upload_image
from user.views import apply_credit_post
from user.views import apply_credit_photo
from user.views import edit_name
from user.views import my_item_comment_list
from user.views import item_list_html
from user.views import menu_credit_apply
from user.views import my_order_bill
from user.views import hospital_item_list
from user.views import order_pay_success
from user.views import repayment_pay_success
from user.views import cancel_pay
from user.views import cancel_order
from user.views import finish_order
from user.views import hospital_location
from user.views import meifenfen_index
from user.views import meifenfen_city
from user.views import help_html
from user.views import hospital_list_html
from user.views import hospital_list
from user.views import mei_tutorials
from user.views import daily_coupons
from user.views import tutorial_detail
from user.views import receive_coupon
from user.views import meifenfen_new_index
from user.views import hospital_filters
from user.views import resend_user_coupon

from user.auth  import get_reg_vcode
from user.auth  import signup_post
from user.auth  import get_vcode
from user.auth  import reset_passwd
from user.auth  import signup
from user.auth  import user_login
from user.auth  import user_login_post
from user.auth  import auth_wechat
from user.auth  import logout


user_api       = Blueprint('user_api', __name__,
                        template_folder='templates')

user_api.add_url_rule('/', 'user', user_index)

user_api.add_url_rule('/index/', 'meifenfen', meifenfen_new_index)
user_api.add_url_rule('/new/', 'meifenfen_new', meifenfen_new_index)

user_api.add_url_rule('/meifenfen_city/', 'meifenfen_city', meifenfen_city, methods=['POST', 'GET'])

user_api.add_url_rule('/item_cats/', 'item_cats', item_cats)
user_api.add_url_rule('/hospital_filters/', 'hospital_filters', hospital_filters)
user_api.add_url_rule('/item_filters/', 'item_filters', item_filters, methods=['POST', 'GET'])
user_api.add_url_rule('/item_list/', 'item_list', item_list, methods=['POST', 'GET'])
user_api.add_url_rule('/hospital_item_list/', 'hospital_item_list', hospital_item_list, methods=['POST', 'GET'])
user_api.add_url_rule('/item_list.html', 'item_list_html', item_list_html)
user_api.add_url_rule('/hospital_list.html', 'hospital_list_html', hospital_list_html)
user_api.add_url_rule('/hospital_list/', 'hospital_list', hospital_list, methods=['POST', 'GET'])

user_api.add_url_rule('/help.html', 'help_html', help_html)


user_api.add_url_rule('/item_detail/', 'item_detail', item_detail, methods=['POST', 'GET'])
user_api.add_url_rule('/hospital_detail/', 'hospital_detail', hospital_detail, methods=['POST', 'GET'])
user_api.add_url_rule('/hospital_location/', 'hospital_location', hospital_location, methods=['POST', 'GET'])

user_api.add_url_rule('/comment_list/', 'item_comment_list', item_comment_list, methods=['POST', 'GET'])
user_api.add_url_rule('/my_item_comment_list/', 'my_item_comment_list', my_item_comment_list, methods=['POST', 'GET'])

user_api.add_url_rule('/comment_post/', 'item_comment_post', comment_post, methods=['POST', 'GET'])

#申请额度
user_api.add_url_rule('/apply_credit/', 'apply_credit', user_login_post, methods=['POST', 'GET']) #申请第一步
user_api.add_url_rule('/apply_credit_post/', 'apply_credit_post', apply_credit_post, methods=['POST', 'GET'])
user_api.add_url_rule('/apply_photo/', 'apply_photo', user_login_post, methods=['POST', 'GET']) #申请第二步
#user_api.add_url_rule('/apply_photo_post/', 'apply_photo_post', apply_credit_photo, methods=['POST', 'GET'])

user_api.add_url_rule('/order_preview/', 'order_preview', order_preview, methods=['POST', 'GET'])
user_api.add_url_rule('/confirm_order/', 'confirm_order', confirm_order, methods=['POST', 'GET'])
user_api.add_url_rule('/order_pay/', 'order_pay', order_pay, methods=['POST', 'GET'])
user_api.add_url_rule('/repayment_pay/', 'repayment_pay', repayment_pay, methods=['POST', 'GET']) #选择支付方式 还款
user_api.add_url_rule('/order_pay_post/', 'order_pay_post', user_login_post, methods=['POST', 'GET'])
user_api.add_url_rule('/wx_pay_callback/', 'wx_pay_callback', wx_pay_callback, methods=['POST', 'GET']) #微信支付回调
user_api.add_url_rule('/wx_repayment_callback/', 'wx_repayment_callback', wx_repayment_callback, methods=['POST', 'GET']) #微信还款回调

#上传图片
user_api.add_url_rule('/uploads/', 'uploads', uploads, methods=['POST', 'GET']) #上传图片 

#个人接口
user_api.add_url_rule('/home/', 'user_home', user_home, methods=['POST', 'GET'])
user_api.add_url_rule('/edit_profile/', 'edit_profile', user_login_post, methods=['POST', 'GET'])
user_api.add_url_rule('/my_period_bill/', 'my_period_bill', my_period_bill, methods=['POST', 'GET']) #当期账单
user_api.add_url_rule('/my_repayments/', 'my_repayments', my_repayments, methods=['POST', 'GET']) #还款历史
user_api.add_url_rule('/my_order_bill/', 'my_order_bill', my_order_bill, methods=['POST', 'GET']) #订单每期账单

user_api.add_url_rule('/my_apply/', 'my_apply', my_apply, methods=['POST', 'GET']) #审核进度
user_api.add_url_rule('/my_orders/', 'my_orders', user_order_list, methods=['POST', 'GET']) #
user_api.add_url_rule('/my_coupons/', 'my_coupons', my_coupons, methods=['POST', 'GET']) #
user_api.add_url_rule('/order_detail/', 'order_detail', order_detail, methods=['POST', 'GET']) #
user_api.add_url_rule('/cancel_order/', 'cancel_order', cancel_order, methods=['POST', 'GET']) #
user_api.add_url_rule('/cancel_pay/', 'cancel_pay', cancel_pay, methods=['POST', 'GET']) #
user_api.add_url_rule('/my_favs/', 'my_favs', my_favs, methods=['POST', 'GET']) #我的心愿单
user_api.add_url_rule('/fav_item/', 'fav_item', user_fav_item, methods=['POST', 'GET']) #我的心愿单


user_api.add_url_rule('/login/', 'user_logn', user_login)
user_api.add_url_rule('/login_post/', 'user_login_post', user_login_post, methods=['POST'])
user_api.add_url_rule('/get_vcode/', 'get_vcode', get_vcode, methods=['POST', 'GET'])
user_api.add_url_rule('/get_reg_vcode/', 'get_reg_vcode', get_reg_vcode, methods=['POST', 'GET'])
user_api.add_url_rule('/signup/', 'signup', signup, methods=['GET'])
user_api.add_url_rule('/signup_post/', 'signup_post', signup_post, methods=['POST', 'GET'])
user_api.add_url_rule('/reset_passwd/', 'reset_passwd', reset_passwd, methods=['POST', 'GET'])
user_api.add_url_rule('/logout/', 'logout', logout, methods=['POST', 'GET'])
user_api.add_url_rule('/auth', 'auth_wechat', auth_wechat, methods=['POST', 'GET'])

#帮助
user_api.add_url_rule('/help/', 'help', help, methods=['POST', 'GET'])
user_api.add_url_rule('/get_help_entry/', 'get_help_entry', get_help_entry, methods=['POST', 'GET'])
user_api.add_url_rule('/advice/', 'advice', user_advice, methods=['POST', 'GET'])


user_api.add_url_rule('/apply_credit_page/', 'apply_credit_page', apply_credit_page, methods=['POST', 'GET'])

user_api.add_url_rule('/project_doctor_description/', 'project_doctor_description', project_doctor_description, methods=['POST', 'GET'])

user_api.add_url_rule('/jssdk.js', 'get_jssdk_js', get_jssdk_js, methods=['POST', 'GET'])

user_api.add_url_rule('/get_school_list/', 'get_school_list', get_school_list, methods=['POST', 'GET'])

user_api.add_url_rule('/repayment/', 'repayment', repayment, methods=['POST', 'GET'])

user_api.add_url_rule('/get_city_list/', 'get_city_list', get_city_list, methods=['POST', 'GET'])


user_api.add_url_rule('/upload_image/', 'upload_image', upload_image, methods=['POST', 'GET'])

user_api.add_url_rule('/edit_name/', 'edit_name', edit_name, methods=['POST', 'GET'])

user_api.add_url_rule('/menu_credit_apply/', 'menu_credit_apply', menu_credit_apply, methods=['POST', 'GET'])


user_api.add_url_rule('/order_pay_success/', 'order_pay_success', order_pay_success)
user_api.add_url_rule('/repayment_pay_success/', 'repayment_pay_success', repayment_pay_success)

user_api.add_url_rule('/finish_order/', 'finish_order', finish_order, methods=['POST', 'GET'])



from user.trial import trial_list
from user.trial import my_trial_list
from user.trial import comment_trial
from user.trial import apply_trial
from user.trial import trial_applyers
from user.trial import trial_comment_list

from user.trial import get_trial_detail
from user.trial import get_history_apply

#试用
user_api.add_url_rule('/trial_list/', 'trial_list', trial_list, methods=['POST', 'GET'])

user_api.add_url_rule('/my_trial_list/', 'my_trial_list', my_trial_list, methods=['POST', 'GET'])

user_api.add_url_rule('/comment_trial/', 'comment_trial', comment_trial, methods=['POST', 'GET'])

user_api.add_url_rule('/apply_trial/', 'apply_trial', apply_trial, methods=['POST', 'GET'])

user_api.add_url_rule('/trial_applyers/', 'trial_applyers', trial_applyers, methods=['POST', 'GET'])

user_api.add_url_rule('/trial_comment_list/', 'trial_comment_list', trial_comment_list, methods=['POST', 'GET'])

user_api.add_url_rule('/get_trial_detail/', 'get_trial_detail', get_trial_detail, methods=['POST', 'GET'])

user_api.add_url_rule('/get_history_apply/', 'get_history_apply', get_history_apply, methods=['POST', 'GET'])

user_api.add_url_rule('/mei_tutorials/', 'mei_tutorials', mei_tutorials, methods=['POST', 'GET'])

user_api.add_url_rule('/daily_coupons/', 'daily_coupons', daily_coupons, methods=['POST','GET'])

user_api.add_url_rule('/tutorial_detail/', 'tutorial_detail', tutorial_detail, methods=['POST','GET'])

user_api.add_url_rule('/receive_coupon/', 'receive_coupon', receive_coupon, methods=['POST','GET'])

user_api.add_url_rule('/resend_user_coupon/', 'resend_user_coupon', resend_user_coupon, methods=['POST','GET'])


from user.room_design import get_room_detail
from user.room_design import apply_room
from user.room_design import room_list
from user.room_design import vote_room
from user.room_design import room_search
from user.room_design import room_index
from user.room_design import add_room_pics
from user.room_design import school_rooms
from user.room_design import get_vote_priviledges
from user.room_design import room_about

user_api.add_url_rule('/get_room_detail/', 'get_room_detail', get_room_detail, methods=['POST','GET'])
user_api.add_url_rule('/apply_room/', 'apply_room', apply_room, methods=['POST','GET'])
user_api.add_url_rule('/vote_room/', 'vote_room', vote_room, methods=['POST','GET'])
user_api.add_url_rule('/room_list/', 'room_list', room_list, methods=['POST','GET'])
user_api.add_url_rule('/room_search/', 'room_search', room_search, methods=['POST','GET'])
user_api.add_url_rule('/room_index/', 'room_index', room_index, methods=['POST','GET'])

user_api.add_url_rule('/add_room_pics/', 'add_room_pics', add_room_pics, methods=['POST','GET'])

user_api.add_url_rule('/school_rooms/', 'school_rooms', school_rooms, methods=['POST','GET'])

user_api.add_url_rule('/get_vote_priviledges/', 'get_vote_priviledges', get_vote_priviledges, methods=['POST','GET'])
user_api.add_url_rule('/room_about/', 'room_about', room_about, methods=['POST','GET'])




from user.redpack import new_question
from user.redpack import new_question_post
from user.redpack import my_questions
from user.redpack import question_viewers
from user.redpack import question_detail
from user.redpack import redpack_pay
from user.redpack import wx_redpack_callback
from user.redpack import redpack_index
from user.redpack import question_list


user_api.add_url_rule('/redpack_index/', 'redpack_index', redpack_index, methods=['POST', 'GET'])

user_api.add_url_rule('/my_questions/', 'my_questions', my_questions, methods=['POST', 'GET'])

user_api.add_url_rule('/new_question/', 'new_question', new_question, methods=['POST', 'GET'])

user_api.add_url_rule('/question_detail/', 'question_detail', question_detail, methods=['POST', 'GET'])

user_api.add_url_rule('/new_question_post/', 'new_question_post', new_question_post, methods=['POST', 'GET'])

user_api.add_url_rule('/redpack_pay/', 'redpack_pay', redpack_pay, methods=['POST', 'GET'])

user_api.add_url_rule('/question_viewers/', 'question_viewers', question_viewers, methods=['POST', 'GET'])

user_api.add_url_rule('/wx_redpack_callback/', 'wx_redpack_callback', wx_redpack_callback, methods=['POST','GET'])

user_api.add_url_rule('/question_list/', 'question_list', question_list, methods=['POST','GET'])

from user.views import set_open_id

user_api.add_url_rule('/set_open_id/', 'set_open_id', set_open_id, methods=['POST','GET'])


from user.draw_money import draw_index
from user.draw_money import draw_money

user_api.add_url_rule('/draw_money/', 'draw_money', draw_money, methods=['POST','GET'])
user_api.add_url_rule('/draw_index/', 'draw_index', draw_index, methods=['POST','GET'])




