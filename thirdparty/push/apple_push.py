# -*- coding: utf-8 -*-
import os
import logging
logging.basicConfig()
from apnsclient import *
import OpenSSL
OpenSSL.SSL.SSLv3_METHOD = OpenSSL.SSL.TLSv1_METHOD

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))


push_name = 'push_production'
pem_file = 'ck_production.pem'
con = Session().new_connection(push_name, cert_file=CURRENT_DIR+"/"+pem_file, passphrase='2016')
srv = APNs(con)

# Persistent connection for intensive messaging.
# Keep reference to session instance in some class static/global variable,
# otherwise it will be garbage collected and all connections will be closed.
#session = Session()
#con = session.get_connection("push_sandbox", cert_file="ck.pem")


def send_message(tokens, alert, badge=1, sound='bingbong.aiff', extra=None):
    message = Message(tokens, alert, badge=badge, sound=sound, extra=extra)
    print 'apns', alert, tokens, sound, extra
    try:
        res = srv.send(message)
    except:
        import traceback
        traceback.print_exc()
        print "Can't connect to APNs, looks like network is down"
    else:
        for token, reason in res.failed.items():
            code, errmsg = reason
            print "Device failed: {0}, reason: {1}".format(token, errmsg)

        for code, errmsg in res.errors:
            print "Error: {}".format(errmsg)
    
        # Check if there are tokens that can be retried
        if res.needs_retry():
            retry_message = res.retry()

try:
    from settings import celery
    send_message = celery.task(send_message)
except:
    pass



def send_push(token):
    ''' '''
    token = token.replace(' ', '')
    alert = "您有一条新消息"
    badge = 1
    sound='bingbong.aiff'
    send_message((token,), alert, badge, sound, extra={'a':2})


if __name__=='__main__':
    token = "bf33007c b3141c26 54658090 f7f57c51 210b7375 2985f237 6311aded 1b8d9b28".replace(' ', '')
    send_push(token)


