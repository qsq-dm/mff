# -*- coding: utf-8 -*-
import re


SQL_DUPLICATE   = re.compile(r"Duplicate entry .*? for key")
_DUPLICATE_PRIMARY = re.compile(r"Duplicate entry '.*?' for key 'PRIMARY'")
class RegDup(object):
    @staticmethod
    def search(string):
        return bool(SQL_DUPLICATE.search(string)) and not(bool(_DUPLICATE_PRIMARY.search(string)))

SQL_REF_NOT_EXIST_ERR = re.compile("a foreign key constraint fails")

SQL_DUPLICATE_ENTRY   = RegDup

SQL_MONEY_NOT_ENOUGH  = re.compile('BIGINT UNSIGNED value is out of range in')

SQL_DUPLICATE_NAME    = re.compile(r"Duplicate entry '.*?' for key 'name'")

SQL_DUPLICATE_PHONE   = re.compile(r"Duplicate entry '.*?' for key 'phone'")

SQL_DUPLICATE_WECHAT  = re.compile(r"Duplicate entry '.*?' for key 'wx_id'")

SQL_DUPLICATE_BIND_WECHAT = re.compile(r"with identity key")


SQL_DUPLICATE_ORDER_NO          = re.compile(r"Duplicate entry '.*?' for key 'order_no'")

SQL_DUPLICATE_COUPON            = re.compile(r"Duplicate entry '.*?' for key 'coupon_id'")


SQL_REF_COUPON_NOT_EXIST        = re.compile("a foreign key constraint fails .*? FOREIGN KEY \(\`coupon_id")