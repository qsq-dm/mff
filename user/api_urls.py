# -*- coding: utf-8 -*-

from flask import request
from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

from user.api_views import user_index
from user.api_views import item_detail
from user.api_views import item_list
from user.api_views import item_filters
from user.api_views import item_comment_list
from user.api_views import user_fav_item
from user.api_views import user_advice
from user.api_views import user_order_list
from user.api_views import order_preview
from user.api_views import confirm_order
from user.api_views import order_pay
from user.api_views import repayment_pay
from user.api_views import wxapp_pay_callback
from user.api_views import wxapp_repayment_callback
from user.api_views import uploads
from user.api_views import order_detail
from user.api_views import comment_post
from user.api_views import my_period_bill
from user.api_views import user_home
from user.api_views import my_repayments
from user.api_views import item_cats
from user.api_views import my_favs
from user.api_views import my_coupons
from user.api_views import my_apply
from user.api_views import help
from user.api_views import repayment
from user.api_views import get_help_entry
from user.api_views import apply_credit_page
from user.api_views import project_doctor_description
from user.api_views import get_jssdk_js
from user.api_views import get_school_list
from user.api_views import hospital_detail
from user.api_views import get_city_list
from user.api_views import upload_image
from user.api_views import apply_credit_post
from user.api_views import apply_credit_photo
from user.api_views import edit_name
from user.api_views import my_item_comment_list
from user.api_views import my_order_bill
from user.api_views import hospital_item_list
from user.api_views import order_pay_success
from user.api_views import repayment_pay_success
from user.api_views import cancel_order
from user.api_views import finish_order
from user.api_views import hospital_location
from user.api_views import meifenfen_index
from user.api_views import meifenfen_city
from user.api_views import help_html
from user.api_views import alipay_order_pay_action
from user.api_views import wx_order_pay_action
from user.api_views import my_apply_result
from user.api_views import alipay_notify
from user.api_views import alipay_repayment_notify
from user.api_views import apply_credit
from user.api_views import alipay_repayment_pay_action
from user.api_views import wx_repayment_pay_action
from user.api_views import notification_list
from user.api_views import mark_read
from user.api_views import test_wx_app_pay
from user.api_views import test_alipay
from user.api_views import recommend_item_list
from user.api_views import check_update

from user.auth  import get_reg_vcode
from user.auth  import signup_post
from user.auth  import get_vcode
from user.auth  import reset_passwd
from user.auth  import signup
from user.auth  import user_login
from user.auth  import user_login_post
from user.auth  import auth_wechat
from user.auth  import logout


user_api       = Blueprint('user_app_api', __name__,
                        template_folder='templates')


user_api.add_url_rule('/', 'user', user_index)

user_api.add_url_rule('/recommend_item_list/', 'recommend_item_list', recommend_item_list, methods=['POST', 'GET'])

user_api.add_url_rule('/index/', 'meifenfen', meifenfen_index)
user_api.add_url_rule('/item_cats/', 'item_cats', item_cats)
user_api.add_url_rule('/item_list/', 'item_list', item_list, methods=['POST', 'GET'])
#user_api.add_url_rule('/hospital_item_list/', 'the_hospital_item_list', item_list, methods=['POST', 'GET'])
user_api.add_url_rule('/item_detail/', 'item_detail', item_detail, methods=['POST', 'GET'])

user_api.add_url_rule('/login_post/', 'user_login_post', user_login_post, methods=['POST'])
user_api.add_url_rule('/get_vcode/', 'get_vcode', get_vcode, methods=['POST', 'GET'])
user_api.add_url_rule('/get_reg_vcode/', 'get_reg_vcode', get_reg_vcode, methods=['POST', 'GET'])
user_api.add_url_rule('/signup_post/', 'signup_post', signup_post, methods=['POST', 'GET'])
user_api.add_url_rule('/reset_passwd/', 'reset_passwd', reset_passwd, methods=['POST', 'GET'])
user_api.add_url_rule('/logout/', 'logout', logout, methods=['POST', 'GET'])
user_api.add_url_rule('/item_filters/', 'item_filters', item_filters, methods=['POST', 'GET'])
user_api.add_url_rule('/home/', 'user_home', user_home, methods=['POST', 'GET'])


user_api.add_url_rule('/upload_image/', 'upload_image', upload_image, methods=['POST', 'GET'])

user_api.add_url_rule('/edit_name/', 'edit_name', edit_name, methods=['POST', 'GET'])

user_api.add_url_rule('/meifenfen_city/', 'meifenfen_city', meifenfen_city)
user_api.add_url_rule('/comment_list/', 'item_comment_list', item_comment_list, methods=['POST', 'GET'])

user_api.add_url_rule('/hospital_detail/', 'hospital_detail', hospital_detail, methods=['POST', 'GET'])

user_api.add_url_rule('/order_preview/', 'order_preview', order_preview, methods=['POST', 'GET'])
user_api.add_url_rule('/confirm_order/', 'confirm_order', confirm_order, methods=['POST', 'GET'])
user_api.add_url_rule('/order_pay/', 'order_pay', order_pay, methods=['POST', 'GET'])

user_api.add_url_rule('/comment_post/', 'item_comment_post', comment_post, methods=['POST', 'GET'])

user_api.add_url_rule('/order_detail/', 'order_detail', order_detail, methods=['POST', 'GET']) #


#0000000000
user_api.add_url_rule('/hospital_item_list/', 'hospital_item_list', hospital_item_list, methods=['POST', 'GET'])

user_api.add_url_rule('/help.html', 'help_html', help_html)


user_api.add_url_rule('/hospital_location/', 'hospital_location', hospital_location, methods=['POST', 'GET'])

user_api.add_url_rule('/comment_list/', 'item_comment_list', item_comment_list, methods=['POST', 'GET'])
user_api.add_url_rule('/my_item_comment_list/', 'my_item_comment_list', my_item_comment_list, methods=['POST', 'GET'])

user_api.add_url_rule('/my_favs/', 'my_favs', my_favs, methods=['POST', 'GET']) #我的心愿单
user_api.add_url_rule('/fav_item/', 'fav_item', user_fav_item, methods=['POST', 'GET']) #我的心愿单


#申请额度
user_api.add_url_rule('/apply_credit/', 'apply_credit', apply_credit, methods=['POST', 'GET']) #申请第一步
user_api.add_url_rule('/apply_credit_post/', 'apply_credit_post', apply_credit_post, methods=['POST', 'GET'])
user_api.add_url_rule('/apply_photo/', 'apply_photo', user_login_post, methods=['POST', 'GET']) #申请第二步
#user_api.add_url_rule('/apply_photo_post/', 'apply_photo_post', apply_credit_photo, methods=['POST', 'GET'])

user_api.add_url_rule('/repayment_pay/', 'repayment_pay', repayment_pay, methods=['POST', 'GET']) #选择支付方式 还款
user_api.add_url_rule('/order_pay_post/', 'order_pay_post', user_login_post, methods=['POST', 'GET'])

user_api.add_url_rule('/wx_order_pay_action/', 'wx_order_pay_action', wx_order_pay_action, methods=['POST', 'GET'])
user_api.add_url_rule('/wx_repayment_pay_action/', 'wx_repayment_pay_action', wx_repayment_pay_action, methods=['POST', 'GET'])
user_api.add_url_rule('/alipay_order_pay_action/', 'alipay_order_pay_action', alipay_order_pay_action, methods=['POST', 'GET'])
user_api.add_url_rule('/alipay_repayment_pay_action/', 'alipay_repayment_pay_action', alipay_repayment_pay_action, methods=['POST', 'GET'])
user_api.add_url_rule('/wxapp_pay_callback/', 'wxapp_pay_callback', wxapp_pay_callback, methods=['POST', 'GET']) #微信支付回调
user_api.add_url_rule('/wxapp_repayment_callback/', 'wxapp_repayment_callback', wxapp_repayment_callback, methods=['POST', 'GET']) #微信还款回调

user_api.add_url_rule('/alipay_notify/', 'alipay_notify', alipay_notify, methods=['POST', 'GET'])
user_api.add_url_rule('/alipay_repayment_notify/', 'alipay_repayment_notify', alipay_repayment_notify, methods=['POST', 'GET'])

#上传图片
user_api.add_url_rule('/uploads/', 'uploads', uploads, methods=['POST', 'GET']) #上传图片 

#个人接口
user_api.add_url_rule('/edit_profile/', 'edit_profile', user_login_post, methods=['POST', 'GET'])
user_api.add_url_rule('/my_period_bill/', 'my_period_bill', my_period_bill, methods=['POST', 'GET']) #当期账单
user_api.add_url_rule('/my_repayments/', 'my_repayments', my_repayments, methods=['POST', 'GET']) #还款历史
user_api.add_url_rule('/my_order_bill/', 'my_order_bill', my_order_bill, methods=['POST', 'GET']) #订单每期账单

user_api.add_url_rule('/my_apply/', 'my_apply', my_apply, methods=['POST', 'GET']) #审核进度
user_api.add_url_rule('/my_orders/', 'my_orders', user_order_list, methods=['POST', 'GET']) #
user_api.add_url_rule('/my_coupons/', 'my_coupons', my_coupons, methods=['POST', 'GET']) #
user_api.add_url_rule('/cancel_order/', 'cancel_order', cancel_order, methods=['POST', 'GET']) #

#帮助
user_api.add_url_rule('/help/', 'help', help, methods=['POST', 'GET'])
user_api.add_url_rule('/get_help_entry/', 'get_help_entry', get_help_entry, methods=['POST', 'GET'])
user_api.add_url_rule('/advice/', 'advice', user_advice, methods=['POST', 'GET'])


user_api.add_url_rule('/apply_credit_page/', 'apply_credit_page', apply_credit_page, methods=['POST', 'GET'])

user_api.add_url_rule('/project_doctor_description/', 'project_doctor_description', project_doctor_description, methods=['POST', 'GET'])

user_api.add_url_rule('/get_school_list/', 'get_school_list', get_school_list, methods=['POST', 'GET'])

user_api.add_url_rule('/repayment/', 'repayment', repayment, methods=['POST', 'GET'])

user_api.add_url_rule('/get_city_list/', 'get_city_list', get_city_list, methods=['POST', 'GET'])

user_api.add_url_rule('/my_apply_result/', 'my_apply_result', my_apply_result, methods=['POST', 'GET'])

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

user_api.add_url_rule('/notification_list/', 'notification_list', notification_list)

user_api.add_url_rule('/mark_read/', 'mark_read', mark_read, methods=['POST', 'GET'])

#user_api.add_url_rule('/test_wx_app_pay/', 'test_wx_app_pay', test_wx_app_pay)

#user_api.add_url_rule('/test_alipay/', 'test_alipay', test_alipay, methods=['POST','GET'])

user_api.add_url_rule('/check_update/', 'check_update', check_update, methods=['POST','GET'])

from user.api_views import upload_device_info

user_api.add_url_rule('/upload_device_info/', 'upload_device_info', upload_device_info, methods=['POST','GET'])



from user.api_views import hospital_list
from user.api_views import hospital_filters
from user.api_views import mei_tutorials
from user.api_views import tutorial_detail
from user.api_views import daily_coupons
from user.api_views import resend_user_coupon
from user.api_views import receive_coupon

user_api.add_url_rule('/hospital_list/', 'hospital_list', hospital_list, methods=['POST','GET'])
user_api.add_url_rule('/hospital_filters/', 'hospital_filters', hospital_filters, methods=['POST','GET'])

user_api.add_url_rule('/mei_tutorials/', 'mei_tutorials', mei_tutorials, methods=['POST','GET'])

user_api.add_url_rule('/tutorial_detail/', 'tutorial_detail', tutorial_detail, methods=['POST','GET'])

user_api.add_url_rule('/daily_coupons/', 'daily_coupons', daily_coupons, methods=['POST','GET'])

user_api.add_url_rule('/resend_user_coupon/', 'resend_user_coupon', resend_user_coupon, methods=['POST','GET'])

user_api.add_url_rule('/receive_coupon/', 'receive_coupon', receive_coupon, methods=['POST','GET'])


from user.api_views import meifenfen_new_index

user_api.add_url_rule('/meifenfen_new_index/', 'meifenfen_new_index', meifenfen_new_index, methods=['POST','GET'])



