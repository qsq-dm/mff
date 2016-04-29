# -*- coding: utf-8 -*-

from flask              import request
from flask              import Blueprint, render_template, abort
from jinja2             import TemplateNotFound

from admin.views        import index
from admin.views        import get_city_list
from admin.views        import login
from admin.views        import logout
from admin.views        import new_city
from admin.views        import get_item_list
from admin.views        import item_edit
from admin.views        import get_item
from admin.views        import get_cat
from admin.views        import get_subcat
from admin.views        import hospital_edit
from admin.views        import get_school_list
from admin.views        import get_hospital
from admin.views        import get_hospital_list
from admin.views        import get_cat_list
from admin.views        import get_subcat_list
from admin.views        import set_subcat_status
from admin.views        import get_period_choice_list
from admin.views        import edit_itemcat
from admin.views        import edit_itemsubcat
from admin.views        import refresh_qntoken
from admin.views        import get_apply_list
from admin.views        import get_apply_detail
from admin.views        import apply_approve
from admin.views        import apply_reject
from admin.views        import set_item_status
from admin.views        import recommend_item
from admin.views        import get_user_list
from admin.views        import get_user_detail
from admin.views        import get_school_city_list
from admin.views        import get_order_list
from admin.views        import upload_image
from admin.views        import verify_chsi
from admin.views        import set_chsi_captcha
from admin.views        import refresh_captcha
from admin.views        import get_advice_list
from admin.views        import get_advice_detail
from admin.views        import admin_refund_order
from admin.views        import get_activity_list
from admin.views        import get_activity_items
from admin.views        import set_activity_items
from admin.views        import activity_edit
from admin.views        import get_activity
from admin.views        import top_recommend_item
from admin.views        import recommend_subcat
from admin.views        import top_recommend_subcat
from admin.views        import get_item_recommend
from admin.views        import item_recommend_edit
from admin.views        import get_item_activity
from admin.views        import item_activity_edit
from admin.views        import get_subcat_recommend
from admin.views        import subcat_recommend_edit
from admin.views        import set_recommend_order
from admin.views        import set_recommend_subcat_order
from admin.views        import new_period_pay_choice
from admin.views        import get_period_pay_log_list
from admin.views        import del_item_activity
from admin.views        import get_refund_detail
from admin.views        import get_coupon_list
from admin.views        import coupon_edit
from admin.views        import get_coupon
from admin.views        import trial_edit
from admin.views        import get_trial_list
from admin.views        import get_trial
from admin.views        import trial_applyer_list
from admin.views        import send_trial
from admin.views        import set_trial_order
from admin.views        import get_promoter_list
from admin.views        import add_promoter
from admin.views        import add_hospital_admin
from admin.views        import get_hospital_user_list
from admin.views        import to_supply
from admin.views        import supply_apply
from admin.views        import set_hospital_status
from admin.views        import get_daily_coupon_list
from admin.views        import daily_coupon_edit
from admin.views        import get_daily_coupon
from admin.views        import set_recommend_hospital_order
from admin.views        import hospital_recommend_edit
from admin.views        import get_hospital_recommend
from admin.views        import get_tutorial_list
from admin.views        import tutorial_edit
from admin.views        import get_tutorial
from admin.views        import set_tutorial_status
from admin.views        import get_user_vcode
from admin.views        import reset_user_vcode_sent
from admin.views        import send_user_coupon
from admin.views        import get_city
from admin.views        import city_edit
from admin.views        import recommend_hospital
from admin.views        import daily_applyer_list
from admin.views        import set_cats_order


admin_api       = Blueprint('admin_api', __name__,
                        template_folder='templates')


admin_api.add_url_rule('/', 'index', index)
admin_api.add_url_rule('/login/', 'login', login, methods=['POST', 'GET'])
admin_api.add_url_rule('/logout/', 'logout', logout, methods=['POST', 'GET'])
admin_api.add_url_rule('/get_city_list/', 'get_city_list', get_city_list)
admin_api.add_url_rule('/new_city/', 'new_city', city_edit, methods=['POST', 'GET'])
admin_api.add_url_rule('/city_edit/<int:item_id>/', 'city_edit', city_edit, methods=['POST', 'GET'])

admin_api.add_url_rule('/daily_applyer_list/', 'daily_applyer_list', daily_applyer_list, methods=['POST', 'GET'])
admin_api.add_url_rule('/get_item_list/', 'get_item_list', get_item_list, methods=['POST', 'GET'])
admin_api.add_url_rule('/new_item/', 'new_item', item_edit, methods=['POST', 'GET'])
admin_api.add_url_rule('/edit_item/<int:item_id>/', 'edit_item', item_edit, methods=['POST', 'GET'])

admin_api.add_url_rule('/new_tutorial/', 'new_tutorial', tutorial_edit, methods=['POST', 'GET'])
admin_api.add_url_rule('/tutorial_edit/<int:item_id>/', 'edit_tutorial', tutorial_edit, methods=['POST', 'GET'])

admin_api.add_url_rule('/new_item/', 'new_item', item_edit, methods=['POST', 'GET'])
admin_api.add_url_rule('/edit_item/<int:item_id>/', 'edit_item', item_edit, methods=['POST', 'GET'])
admin_api.add_url_rule('/get_item/', 'get_item', get_item, methods=['POST', 'GET'])
admin_api.add_url_rule('/get_cat/', 'get_cat', get_cat, methods=['POST', 'GET'])
admin_api.add_url_rule('/get_subcat/', 'get_subcat', get_subcat, methods=['POST', 'GET'])

admin_api.add_url_rule('/new_activity/', 'new_activity', activity_edit, methods=['POST', 'GET'])
admin_api.add_url_rule('/new_itemcat/', 'new_itemcat', edit_itemcat, methods=['POST', 'GET'])
admin_api.add_url_rule('/new_itemsubcat/', 'new_itemsubcat', edit_itemsubcat, methods=['POST', 'GET'])
admin_api.add_url_rule('/edit_itemcat/<int:cat_id>/', 'edit_itemcat', edit_itemcat, methods=['POST', 'GET'])
admin_api.add_url_rule('/edit_itemsubcat/<int:sub_cat_id>/', 'edit_itemsubcat', edit_itemsubcat, methods=['POST', 'GET'])
admin_api.add_url_rule('/edit_activity/<int:item_id>/', 'edit_activity', activity_edit, methods=['POST', 'GET'])

admin_api.add_url_rule('/get_school_list/', 'get_school_list', get_school_list, methods=['POST', 'GET'])

admin_api.add_url_rule('/get_order_list/', 'get_order_list', get_order_list, methods=['POST', 'GET'])

admin_api.add_url_rule('/get_city/', 'get_city', get_city, methods=['POST', 'GET'])


admin_api.add_url_rule('/get_cat_list/', 'get_cat_list', get_cat_list, methods=['POST', 'GET'])
admin_api.add_url_rule('/get_subcat_list/', 'get_subcat_list', get_subcat_list, methods=['POST', 'GET'])

admin_api.add_url_rule('/edit_hospital/<int:item_id>/', 'hospital_edit', hospital_edit, methods=['POST', 'GET'])
admin_api.add_url_rule('/new_hospital/', 'new_hospital', hospital_edit, methods=['POST', 'GET'])
admin_api.add_url_rule('/get_hospital/', 'get_hospital', get_hospital, methods=['POST', 'GET'])
admin_api.add_url_rule('/get_hospital_list/', 'get_hospital_list', get_hospital_list, methods=['POST', 'GET'])
admin_api.add_url_rule('/get_tutorial_list/', 'get_tutorial_list', get_tutorial_list)

admin_api.add_url_rule('/get_period_choice_list/', 'get_period_choice_list', get_period_choice_list, methods=['POST', 'GET'])

admin_api.add_url_rule('/subcat/set_status/', 'set_status', set_subcat_status, methods=['POST', 'GET'])

admin_api.add_url_rule('/refresh_qntoken/', 'refresh_qntoken', refresh_qntoken, methods=['POST', 'GET'])



admin_api.add_url_rule('/get_apply_list/', 'get_apply_list', get_apply_list, methods=['POST', 'GET'])
admin_api.add_url_rule('/get_apply_detail/', 'get_apply_detail', get_apply_detail, methods=['POST', 'GET'])
admin_api.add_url_rule('/apply_reject/', 'apply_reject', apply_reject, methods=['POST', 'GET'])
admin_api.add_url_rule('/apply_approve/', 'apply_approve', apply_approve, methods=['POST', 'GET'])


admin_api.add_url_rule('/set_item_status/', 'set_item_status', set_item_status, methods=['POST', 'GET'])
admin_api.add_url_rule('/recommend_item/', 'recommend_item', recommend_item, methods=['POST', 'GET'])
admin_api.add_url_rule('/recommend_hospital/', 'recommend_hospital', recommend_hospital, methods=['POST', 'GET'])
admin_api.add_url_rule('/recommend_subcat/', 'recommend_subcat', recommend_subcat, methods=['POST', 'GET'])


admin_api.add_url_rule('/get_user_list', 'get_user_list', get_user_list)
admin_api.add_url_rule('/get_user_detail', 'get_user_detail', get_user_detail)

admin_api.add_url_rule('/get_school_city_list/', 'get_school_city_list', get_school_city_list)
admin_api.add_url_rule('/get_advice_list/', 'get_advice_list', get_advice_list)
admin_api.add_url_rule('/get_advice_detail/', 'get_advice_detail', get_advice_detail)

admin_api.add_url_rule('/upload_image/', 'upload_image', upload_image, methods=['POST', 'GET'])

admin_api.add_url_rule('/verify_chsi/', 'verify_chsi', verify_chsi, methods=['POST', 'GET'])
admin_api.add_url_rule('/set_chsi_captcha/', 'set_chsi_captcha', set_chsi_captcha, methods=['POST', 'GET'])
admin_api.add_url_rule('/refresh_chsi_captcha/', 'refresh_chsi_captcha', refresh_captcha, methods=['POST', 'GET'])

admin_api.add_url_rule('/refund_order/', 'refund_order', admin_refund_order, methods=['POST', 'GET'])

admin_api.add_url_rule('/get_activity_list/', 'get_activity_list', get_activity_list, methods=['POST', 'GET'])
admin_api.add_url_rule('/get_activity_items/', 'get_activity_items', get_activity_items, methods=['POST', 'GET'])
admin_api.add_url_rule('/set_activity_items/', 'set_activity_items', set_activity_items, methods=['POST', 'GET'])
admin_api.add_url_rule('/get_activity/', 'get_activity', get_activity, methods=['POST', 'GET'])

admin_api.add_url_rule('/top_recommend_item/', 'top_recommend_item', top_recommend_item, methods=['POST', 'GET'])
admin_api.add_url_rule('/top_recommend_subcat/', 'top_recommend_subcat', top_recommend_subcat, methods=['POST', 'GET'])

admin_api.add_url_rule('/get_item_recommend/', 'get_item_recommend', get_item_recommend, methods=['POST', 'GET'])
admin_api.add_url_rule('/get_hospital_recommend/', 'get_hospital_recommend', get_hospital_recommend, methods=['POST', 'GET'])

admin_api.add_url_rule('/get_subcat_recommend/', 'get_subcat_recommend', get_subcat_recommend, methods=['POST', 'GET'])

admin_api.add_url_rule('/get_item_activity/', 'get_item_activity', get_item_activity, methods=['POST', 'GET'])

admin_api.add_url_rule('/item_recommend_edit/<int:item_id>/', 'item_recommend_edit', item_recommend_edit, methods=['POST', 'GET'])
admin_api.add_url_rule('/item_activity_edit/<int:item_id>/', 'item_activity_edit', item_activity_edit, methods=['POST', 'GET'])

admin_api.add_url_rule('/subcat_recommend_edit/<int:item_id>/', 'subcat_recommend_edit', subcat_recommend_edit, methods=['POST', 'GET'])
admin_api.add_url_rule('/hospital_recommend_edit/<int:item_id>/', 'hospital_recommend_edit', hospital_recommend_edit, methods=['POST', 'GET'])
admin_api.add_url_rule('/set_recommend_order/', 'set_recommend_order', set_recommend_order, methods=['POST', 'GET'])
admin_api.add_url_rule('/set_recommend_subcat_order/', 'set_recommend_subcat_order', set_recommend_subcat_order, methods=['POST', 'GET'])
admin_api.add_url_rule('/set_recommend_hospital_order/', 'set_recommend_hospital_order', set_recommend_hospital_order, methods=['POST', 'GET'])


admin_api.add_url_rule('/new_period_pay_choice/', 'new_period_pay_choice', new_period_pay_choice,  methods=['POST', 'GET'])

admin_api.add_url_rule('/get_period_pay_log_list/', 'get_period_pay_log_list', get_period_pay_log_list,  methods=['POST', 'GET'])

admin_api.add_url_rule('/del_item_activity/', 'del_item_activity', del_item_activity,  methods=['POST', 'GET'])

admin_api.add_url_rule('/get_refund_detail/', 'get_refund_detail', get_refund_detail)

admin_api.add_url_rule('/get_coupon_list/', 'get_coupon_list', get_coupon_list)

admin_api.add_url_rule('/coupon_edit/<int:item_id>/', 'coupon_edit', coupon_edit, methods=['POST', 'GET'])
admin_api.add_url_rule('/new_coupon/', 'new_coupon', coupon_edit, methods=['POST', 'GET'])

admin_api.add_url_rule('/get_coupon/', 'get_coupon', get_coupon)

admin_api.add_url_rule('/get_trial_list/', 'get_trial_list', get_trial_list)

admin_api.add_url_rule('/new_trial/', 'new_trial', trial_edit, methods=['POST', 'GET'])
admin_api.add_url_rule('/edit_trial/<int:item_id>/', 'trial_edit', trial_edit, methods=['POST', 'GET'])


admin_api.add_url_rule('/get_trial/', 'get_trial', get_trial)

admin_api.add_url_rule('/trial_applyer_list/', 'trial_applyer_list', trial_applyer_list)

admin_api.add_url_rule('/send_trial/', 'send_trial', send_trial, methods=['POST','GET'])

admin_api.add_url_rule('/set_trial_order/', 'set_trial_order', set_trial_order, methods=['POST','GET'])

admin_api.add_url_rule('/get_promoter_list/', 'get_promoter_list', get_promoter_list)

admin_api.add_url_rule('/add_promoter/', 'add_promoter', add_promoter, methods=['POST','GET'])


admin_api.add_url_rule('/get_hospital_user_list/', 'get_hospital_user_list', get_hospital_user_list)

admin_api.add_url_rule('/add_hospital_admin/', 'add_hospital_admin', add_hospital_admin, methods=['POST','GET'])

admin_api.add_url_rule('/to_supply/', 'to_supply', to_supply, methods=['POST','GET'])

admin_api.add_url_rule('/supply_apply/', 'supply_apply', supply_apply, methods=['POST','GET'])

admin_api.add_url_rule('/set_hospital_status/', 'set_hospital_status', set_hospital_status, methods=['POST','GET'])

admin_api.add_url_rule('/get_daily_coupon_list/', 'get_daily_coupon_list', get_daily_coupon_list, methods=['POST', 'GET'])
admin_api.add_url_rule('/daily_coupon_edit/<int:item_id>/', 'daily_coupon_edit', daily_coupon_edit, methods=['POST', 'GET'])
admin_api.add_url_rule('/new_daily_coupon/', 'new_daily_coupon', daily_coupon_edit, methods=['POST', 'GET'])
admin_api.add_url_rule('/get_daily_coupon/', 'get_daily_coupon', get_daily_coupon, methods=['POST', 'GET'])
admin_api.add_url_rule('/get_tutorial/', 'get_tutorial', get_tutorial)

admin_api.add_url_rule('/set_tutorial_status/', 'set_tutorial_status', set_tutorial_status, methods=['POST', 'GET'])

admin_api.add_url_rule('/get_user_vcode/', 'get_user_vcode', get_user_vcode, methods=['GET', 'POST'])

admin_api.add_url_rule('/reset_user_vcode/', 'reset_user_vcode', reset_user_vcode_sent, methods=['GET', 'POST'])

admin_api.add_url_rule('/send_user_coupon/', 'send_user_coupon', send_user_coupon, methods=['POST'])

admin_api.add_url_rule('/set_cats_order/', 'set_cats_order', set_cats_order, methods=['POST', 'GET'])

