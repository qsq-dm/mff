# -*- coding: utf-8 -*-
import os
from datetime import timedelta

from celery.schedules import crontab
from settings         import MAIN_MYSQL_URI
from settings         import REDIS_PORT
from celery import platforms
platforms.C_FORCE_ROOT = True

BROKER_URL  = 'amqp://monitor:monitor@127.0.0.1:5672/'
if os.environ.get('APP_ENV')=='local':
    from setting.local import *
elif os.environ.get('APP_ENV')=='dev':
    from setting.dev import *
elif os.environ.get('APP_ENV')=='production':
    from setting.production import *
else:
    from setting.local import *


print BROKER_URL

CELERYD_CONCURRENCY         =   3
CELERYD_MAX_TASKS_PER_CHILD =   1

CELERYBEAT_SCHEDULE = {
    'refresh_access_token': {
        'task': 'thirdparty.wechat.refresh_access_token',
        'schedule': timedelta(seconds=3200),
        'args': (),
    },
}

#CELERY_RESULT_BACKEND = 'db+'+MAIN_MYSQL_URI
CELERY_IGNORE_RESULT   = True
#CELERY_RESULT_BACKEND = 'amqp://'
CELERY_RESULT_BACKEND  = BROKER_URL

# BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 86400*7}
# 
# CELERY_DEFAULT_QUEUE = "default_klbb" # 默认的队列，如果一个消息不符合其他的队列就会放在默认队列里面
# 
# CELERY_QUEUES = {
#     "default_klbb": { # 这是上面指定的默认队列
#         "exchange": "default_klbb",
#         "exchange_type": "direct",
#         "routing_key": "default_klbb"
#     },
#     "topicqueue": { # 这是一个topic队列 凡是topictest开头的routing key都会被放到这个队列
#         "routing_key": "topictest.#",
#         "exchange": "topic_exchange",
#         "exchange_type": "topic",
#     },
#     "test": { # test和test2是2个fanout队列,注意他们的exchange相同
#         "exchange": "broadcast_tasks",
#         "exchange_type": "fanout",
#         "binding_key": "broadcast_tasks",
#     }
# }
# 
# class MyRouter(object):
# 
#     def route_for_task(self, task, args=None, kwargs=None):
# 
#         if task.startswith('topictest'):
#             return {
#                 'queue': 'topicqueue',
#             }
#         # 我的dongwm.tasks文件里面有2个任务都是test开头
#         elif task.startswith('klbb.tasks.test'):
#             return {
#                 "exchange": "broadcast_tasks",
#             }
#         # 剩下的其实就会被放到默认队列
#         else:
#             return None
# 
# # CELERY_ROUTES本来也可以用一个大的含有多个字典的字典,但是不如直接对它做一个名称统配
# CELERY_ROUTES = (MyRouter(), )

