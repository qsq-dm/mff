# -*- coding: utf-8 -*-
from app import app as s
from settings import celery
# 
# from celery import current_app
# result = current_app.AsyncResult("12212121")
# result.get()


@celery.task
def add_one():
    print 'add one test celery....'



@celery.task
def set_user(user):
    '''
    用户 直接传model实例 当session关闭后 离线任务会报错
    DetachedInstanceError: Instance <User at 0x10641de50> is not bound to a Session; attribute refresh operation cannot proceed
    '''
    user_id = user.id
    print user.id