# -*- coding: utf-8 -*-
import os
import time


class ORDER_STATUS:
    NEW_ORDER       = 0
    TO_PAY          = 1
    PAY_SUCCESS     = 2
    PAY_ERROR       = 3
    BOOKED          = 4 #已预约 不存在这个状态 须读表service_code
    FINISH          = 5
    TO_COMMENT      = 6 #待评论 表中status不存这个状态，根据另一个字段来判断
    CANCELED        = 7
    VERIFYING       = 8
    CONFIRMED       = 9 #服务码已确认
    CANCEL_BEFORE_PAY = 10 #支付前取消
    REJECTED        = 11 #额度申请被拒绝
    PAY_TIMEOUT     = 12 #支付超时关闭


class REPAYMENT_STATUS:
    NEW             = 0 #准备还款
    TO_PAY          = 1 #还款中
    PAY_SUCCESS     = 2 #还款成功
    PAY_ERROR       = 3



class REDPACK_PAY_STATUS:
    NEW             = 0 #准备还款
    TO_PAY          = 1 #还款中
    PAY_SUCCESS     = 2 #还款成功
    PAY_ERROR       = 3



class PAY_METHOD:
    WECHAT_WEB      = 1 #公众号
    WECHAT_APP      = 2 #微信app
    ALIPAY          = 3 #支付宝


ORDER_STATUS_LABEL  = {
    ORDER_STATUS.NEW_ORDER      : '待支付',
    ORDER_STATUS.TO_PAY         : '待支付',
    ORDER_STATUS.PAY_SUCCESS    : '待服务',
    ORDER_STATUS.BOOKED         : '已预约',
    ORDER_STATUS.PAY_ERROR      : '支付异常',
    ORDER_STATUS.TO_COMMENT     : '待评价',
    ORDER_STATUS.FINISH         : '服务完成',
    ORDER_STATUS.CANCELED       : '已取消',
    ORDER_STATUS.VERIFYING      : '额度审核中',
    ORDER_STATUS.CONFIRMED      : '服务码已确认',
    ORDER_STATUS.CANCEL_BEFORE_PAY      : '支付前取消',
    ORDER_STATUS.REJECTED       : '额度申请被拒绝',
    ORDER_STATUS.PAY_TIMEOUT    : '支付超时关闭',
    }

VOTE_COUNT_SOURCE_MAP = {
    1: 20,
    2: 200,
    3: 1
    }


BODY_LABEL  = {
    1          : '眼部',
    2          : '鼻部',
    3          : '祛痣',
    4          : '美白',
    5          : '脱毛',
    6          : '牙齿',
    7          : '嘴唇',
    8          : '脸型',
    9          : '胸部',
    10         : '其他',
    11         : '整体都满意',
    }


class ORDER_ADMIN_STATUS:
    TO_PAY              = 1
    TO_SERVE            = 2
    FINISH              = 3
    CANCELD             = 4
    TO_REFUND           = 5
    CREDIT_VERIFY       = 6
    REFUNDED            = 7

ORDER_ADMIN_STATUS_MAP        = {
    ORDER_ADMIN_STATUS.TO_PAY           : '支付中',
    ORDER_ADMIN_STATUS.FINISH           : '已完成',
    ORDER_ADMIN_STATUS.TO_REFUND        : '待退款',
    ORDER_ADMIN_STATUS.CANCELD          : '已取消',
    ORDER_ADMIN_STATUS.CREDIT_VERIFY    : '额度待审核',
    ORDER_ADMIN_STATUS.TO_SERVE         : '待服务',
    ORDER_ADMIN_STATUS.REFUNDED         : '已退款'
    }


ADMIN_ORDER_STATUS_CHOICES    = sorted([ {"id":k, "title":v} for k,v in ORDER_ADMIN_STATUS_MAP.items()], key=lambda i:i['id'])


class CREDIT_STATUS:
    ''' 额度状态 '''
    DEFAULT             = 0
    VERIFYING           = 1
    VERIFIED            = 2
    REJECTED            = 3


class APPLY_STATUS:
    ''' 额度申请状态 '''
    FIRST_STEP          = 1 #第一步
    SECOND_STEP         = 2 #第二步
    VERIFIED            = 3 #通过审核
    REJECTED            = 4 #被拒绝


class SERVICE_STATUS:
    ''' 服务码状态 '''
    STANDBY             = 0 #待服务
    BOOKED              = 1 #已预约
    VERIFYED            = 2 #已验证


class ResponseCode:
    ''' 请求返回码 '''

    SUCCESS                     = 0
    NEED_LOGIN                  = 1
    INVALID_VCODE               = 2 #验证码错误
    INVALID_USERNAME_OR_PASSWD  = 3 #用户名或密码错误
    SERVER_ERROR                = 10000









