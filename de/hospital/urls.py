# -*- coding: utf-8 -*-

from flask              import request
from flask              import Blueprint, render_template, abort
from jinja2             import TemplateNotFound

from hospital.views         import index
from hospital.views         import book_surgery
from hospital.views         import confirm_surgery
from hospital.views         import cancel_book
from hospital.views         import cancel_surgery
from hospital.views         import finish_order
from hospital.views         import login_post
from hospital.views         import login
from hospital.views         import get_hospital_cats
from hospital.views         import get_orders
from hospital.views         import change_passwd_post
from hospital.views         import change_passwd
from hospital.views         import search_order_list
from hospital.views         import home
from hospital.views         import cat
from hospital.views         import reset_passwd
from hospital.views         import reset_passwd_post
from hospital.views         import cat_items
from hospital.views         import logout
from hospital.views         import get_paged_orders


hospital_api       = Blueprint('hospital_api', __name__,
                        template_folder='templates')


hospital_api.add_url_rule('/', 'index', index)

hospital_api.add_url_rule('/get_paged_orders', 'get_paged_orders', get_paged_orders)


hospital_api.add_url_rule('/book_surgery/', 'book_surgery', book_surgery, methods=['POST', 'GET'])
hospital_api.add_url_rule('/confirm_surgery/', 'confirm_surgery', confirm_surgery, methods=['POST', 'GET'])

hospital_api.add_url_rule('/cancel_book/', 'cancel_book', cancel_book, methods=['POST', 'GET'])
hospital_api.add_url_rule('/cancel_surgery/', 'cancel_surgery', cancel_surgery, methods=['POST', 'GET'])

hospital_api.add_url_rule('/finish_order/', 'finish_order', finish_order, methods=['POST', 'GET'])


hospital_api.add_url_rule('/login/', 'login', login)
hospital_api.add_url_rule('/login_post/', 'login_post', login_post, methods=['POST', 'GET'])


hospital_api.add_url_rule('/get_hospital_cats/', 'get_hospital_cats', get_hospital_cats, methods=['POST', 'GET'])
hospital_api.add_url_rule('/get_orders/', 'get_orders', get_orders, methods=['POST', 'GET'])


hospital_api.add_url_rule('/change_passwd_post/', 'change_passwd_post', change_passwd_post, methods=['POST', 'GET'])


hospital_api.add_url_rule('/search_order_list/', 'search_order_list', search_order_list, methods=['POST', 'GET'])

hospital_api.add_url_rule('/home/', 'home', home, methods=['POST', 'GET'])
hospital_api.add_url_rule('/cat/', 'cat', cat, methods=['POST', 'GET'])


hospital_api.add_url_rule('/reset_passwd/', 'reset_passwd', reset_passwd, methods=['POST', 'GET'])


hospital_api.add_url_rule('/reset_passwd_post/', 'reset_passwd_post', reset_passwd_post, methods=['POST', 'GET'])

hospital_api.add_url_rule('/cat_items/', 'cat_items', cat_items, methods=['POST', 'GET'])



hospital_api.add_url_rule('/logout/', 'logout', logout, methods=['POST', 'GET'])




