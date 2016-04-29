# -*- coding: utf-8 -*-

from flask              import request
from flask              import Blueprint, render_template, abort
from jinja2             import TemplateNotFound

from promote.views      import index
from promote.views      import login
from promote.views      import create_promoter
from promote.views      import get_promoter_list
from promote.views      import login_post
from promote.views      import logout
from promote.views      import del_promoter


promote_api       = Blueprint('promote_api', __name__,
                        template_folder='templates')


promote_api.add_url_rule('/', 'get_promoter_list', get_promoter_list)

promote_api.add_url_rule('/login/', 'login', login)
promote_api.add_url_rule('/logout/', 'logout', logout)
promote_api.add_url_rule('/create_promoter/', 'create_promoter', create_promoter, methods=['POST','GET'])

promote_api.add_url_rule('/get_promoter_list/', 'get_promoter_list', get_promoter_list)

promote_api.add_url_rule('/login_post/', 'login_post', login_post, methods=['GET', 'POST'])

promote_api.add_url_rule('/del_promoter/', 'del_promoter', del_promoter, methods=['GET', 'POST'])