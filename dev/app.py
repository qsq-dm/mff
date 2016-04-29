# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask import Flask
from flask import request
from flask import render_template
from flask import send_from_directory
from flask.ext.sqlalchemy import SQLAlchemy

from models import db
from util.utils         import jsonify_response
from thirdparty.views   import server_verify
from thirdparty.wechat  import wechat
from ops.cache          import WechatTokenCache
wechat.set_cache(WechatTokenCache)#设置token缓存属性 
from user.urls          import user_api
from user.api_urls      import user_api as user_app_api

from admin.urls         import admin_api
from hospital.urls      import hospital_api
from promote.urls       import promote_api
from constants          import ResponseCode


app = Flask(__name__)
close_session = lambda response: db.session.close() or response
app.after_request(close_session) #当请求结束关闭session


#微信回调
app.register_blueprint(server_verify, url_prefix='/wx_callback')
#用户端
app.register_blueprint(user_api, url_prefix='/user')
#用户端app接口
app.register_blueprint(user_app_api, url_prefix='/api')
#管理端
app.register_blueprint(admin_api, url_prefix='/admin')
#医院端
app.register_blueprint(hospital_api, url_prefix='/hospital')
#推广
app.register_blueprint(promote_api, url_prefix='/promote')
from user.views import login_link
from user.views import wechat_room_link

app.add_url_rule('/static/user/login.html', 'login_link', login_link, methods=['POST','GET'])
app.add_url_rule('/static/user/Activities/home.html', 'wechat_room_link', wechat_room_link, methods=['POST','GET'])

@app.errorhandler(500)
def internal_error(exception):
    ''' 服务器异常 '''
    print '-'*80
    print(exception), 'internal_error'
    print '-'*80
    import traceback
    traceback.print_exc()
    if getattr(request, 'is_app', False):
        return jsonify_response({'msg':'服务器异常', 'code': ResponseCode.SERVER_ERROR})
    else:
        return render_template('server_error.html'), 500


@app.route('/',methods=['POST','GET'])
def pc_index():
    ''' 首页 '''
    return send_from_directory('static/pc/', 'home.html')
    return render_template('meifenfen.html')


@app.route('/mobile/',methods=['POST','GET'])
def mobile_index():
    ''' 移动端首页 '''
    return send_from_directory('static/pc/', 'home.html')
    return render_template('meifenfen.html')



if __name__ == "__main__":
    from settings import RUN_PORT
    from werkzeug.serving import run_simple
    print RUN_PORT
    run_simple('0.0.0.0', RUN_PORT, app, use_reloader=True, use_debugger=True)


