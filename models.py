# -*- coding: utf-8 -*-
'''
'''
from flask                  import Flask
from flask.ext.sqlalchemy   import SQLAlchemy
from flask.ext.script       import Manager
from flask.ext.migrate      import Migrate, MigrateCommand

from sqlalchemy              import TypeDecorator
from sqlalchemy              import UniqueConstraint
from sqlalchemy              import PrimaryKeyConstraint
from sqlalchemy.ext          import mutable
from sqlalchemy.sql.sqltypes import String
from sqlalchemy.sql.sqltypes import Text
from sqlalchemy.sql.sqltypes import Integer
from sqlalchemy.sql.sqltypes import UnicodeText
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.sql.sqltypes import Float
from sqlalchemy.sql.sqltypes import Boolean
from sqlalchemy.dialects.mysql import TINYINT,DECIMAL,CHAR,INTEGER
from sqlalchemy.sql.expression import cast

from util.utils              import prefix_http
from util.utils              import dt_obj
from util.utils              import format_price
from util.utils              import format_rate
from util.utils              import prefix_img_domain
from util.utils              import prefix_img_list
from util.utils              import prefix_img_list_thumb
from util.utils              import str_to_int_list
from util.utils              import comma_str_to_list
from util.utils              import imgs_to_list
from settings                import MAIN_MYSQL_URI
from settings                import DEFAULT_IMAGE
from constants               import CREDIT_STATUS


app   = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']    = MAIN_MYSQL_URI
db    = SQLAlchemy(app)



Column          = db.Column
Table           = db.Table
ForeignKey      = db.ForeignKey


class Model(db.Model):
    __abstract__       = True

    @staticmethod
    def show_status():
        return True


class MoneyField(TypeDecorator):
    impl = DECIMAL(10, 2)
    def column_expression(self, col):
        return cast(col, Float)
    def process_result_value(self, value, dialect):
        return float(value or 0)


class User(Model):
    ''' 用户 '''
    id                 = db.Column(Integer, primary_key=True)
    name               = db.Column(String(80), unique=True)
    avatar             = db.Column(String(1000))
    phone              = db.Column(String(80), unique=True)
    passwd             = db.Column(String(80))
    city_id            = Column(Integer, ForeignKey('city.id'))
    create_time        = Column(DateTime, default=dt_obj.now)

    def as_dict(self):
        return dict(
            id          = self.id,
            name        = self.name,
            avatar      = prefix_img_domain(self.avatar or DEFAULT_IMAGE),
            phone       = self.phone,
            create_time = self.create_time
        )


class Wechat(Model):
    __tablename__   = 'wechat' 
    __table_args__  = (
        PrimaryKeyConstraint('open_id'),
    )
    open_id         = Column(String(32), autoincrement=False)
    user_id         = Column(Integer, ForeignKey('user.id'), nullable=True)
    create_time     = Column(DateTime, default=dt_obj.now)
    status          = Column(TINYINT(1), nullable=False, default=0) #1已登录 0新注册未绑定user －1已退出


class Order(Model):
    '''
    提交订单时， 优惠券和额度都锁定
    credit_choice_id 下单时 就存下来
    直到真正付款成功了生成每一期的PeriodPayLog记录
    '''
    id                 = db.Column(Integer, primary_key=True)
    pay_method         = Column(TINYINT(1), nullable=False, default=0)#0没用付钱(可能是全部使用优惠券或信用额度) 1微信号 2微信app 3支付宝
    user_id            = Column(Integer, ForeignKey('user.id'), nullable=False)
    hospital_id        = Column(Integer, ForeignKey('hospital.id'), nullable=False)
    item_id            = Column(Integer, ForeignKey('item.id'), nullable=False)
    order_no           = db.Column(String(30), unique=True)
    transaction_id     = db.Column(String(100))
    credit_choice_id   = Column(Integer, ForeignKey('period_pay_choice.id'), nullable=True)#只用做订单支付预览显示
    coupon_id          = Column(Integer, ForeignKey('user_coupon.id'), nullable=True, unique=True)
    coupon_amount      = Column(MoneyField, nullable=False, default=0)#优惠券面值用量
    credit_amount      = Column(MoneyField, nullable=False, default=0)#信用额度使用量(分期总额＋分期费用)
    total_fee          = Column(MoneyField, nullable=False, default=0)#分期费用
    price              = Column(MoneyField, nullable=False, default=0)#订单实际付款的钱 不包括信用额度
    total              = Column(MoneyField, nullable=False, default=0)#订单总价 不使用优惠券时的价格
    create_time        = Column(DateTime, default=dt_obj.now)
    status             = Column(TINYINT(1), nullable=False, default=0) #0待支付 (额度已外金额付款状态)
    refund             = Column(TINYINT(1), nullable=False, default=0) #0为退款 1已退款
    credit_verified    = Column(TINYINT(1), nullable=False, default=0) #额度是否通过审核 0待审核 1通过审核 2被拒绝重新申请
    user_finished      = Column(Boolean, default=False) #用户已确认完成
    remark             = db.Column(String(300))

    def as_dict(self):
        return dict(
            id          = self.id,
            user_id     = self.user_id,
            item_id     = self.item_id,
            order_no    = self.order_no,
            transaction_id  = self.transaction_id,
            hospital_id = self.hospital_id,
            coupon_id   = self.coupon_id or 0,
            price       = format_price(self.price or 0),
            total_fee   = format_price(self.total_fee or 0),
            total       = format_price(self.total or 0),
            credit_amount       = format_price(self.credit_amount or 0),
            coupon_amount       = format_price(self.coupon_amount or 0),
            create_time = str(self.create_time),
            status      = self.status,
            credit_choice_id = self.credit_choice_id or 0,
            refund      = self.refund,
            credit_verified = self.credit_verified,
            user_finished   = self.user_finished,
            remark          = self.remark or ''
            )


class Coupon(Model):
    '''优惠券'''
    id                 = db.Column(Integer, primary_key=True)
    item_id            = Column(Integer, ForeignKey('item.id'), nullable=True)
    title              = Column(String(300), default='')
    price              = Column(MoneyField, nullable=False, default=0) #实付金额
    need               = Column(MoneyField, nullable=False, default=0) #需要满多少才能使用
    coupon_cat         = Column(TINYINT(1), nullable=False, default=0) #优惠券类型
    cat_id             = Column(Integer, ForeignKey('item_cat.id'), nullable=True)#0分类
    sub_cat_id         = Column(Integer, ForeignKey('item_sub_cat.id'), nullable=True)
    effective          = Column(Integer,nullable=False,default=0)
    remark             = Column(String(100), default='')
    is_trial           = Column(Boolean, default=False) #是否是试用券

    def as_dict(self):
        need_cat         = 1 if self.need else 2 #1满减券 2普通
        return dict(
            id          = self.id,
            coupon_cat  = self.coupon_cat,
            is_trial    = 1 if self.is_trial else 0,
            item_id     = self.item_id,
            need        = format_price(self.need),
            title       = self.title,
            price       = format_price(self.price),
            cat_id      = self.cat_id,
            need_cat    = need_cat,
            sub_cat_id  = self.sub_cat_id,
            effective   = self.effective,
            effective_days = self.effective/86400,
            remark      = self.remark,
            )



class UserCoupon(Model):
    ''' 用户优惠券 '''
    id                 = db.Column(Integer, primary_key=True)
    coupon_id          = Column(Integer, ForeignKey('coupon.id'), autoincrement=False)
    title              = Column(String(300), default='')
    user_id            = Column(Integer, ForeignKey('user.id'), nullable=False)
    item_id            = Column(Integer, ForeignKey('item.id'), nullable=True)
    need               = Column(MoneyField, nullable=False, default=0) #需要满多少才能使用
    coupon_cat         = Column(TINYINT(1), nullable=False, default=0) #优惠券类型 0全部 1cat分类 2子分类 3指定项目
    cat_id             = Column(Integer, ForeignKey('item_cat.id'), nullable=True)#0分类
    sub_cat_id         = Column(Integer, ForeignKey('item_sub_cat.id'), nullable=True)
    price              = Column(MoneyField, nullable=False, default=0)#实付金额
    status             = Column(TINYINT(1), nullable=False, default=0)#0未使用 1已使用
    end_time           = Column(DateTime, nullable=False)
    create_time        = Column(DateTime, nullable=False, default=dt_obj.now)
    remark             = Column(String(100), default='')
    is_trial           = Column(Boolean, default=False) #是否是试用券

    def as_dict(self):
        return dict(
            id              = self.id,
            coupon_cat      = self.coupon_cat,
            cat_id          = self.cat_id,
            is_trial        = 1 if self.is_trial else 0,
            title           = self.title,
            sub_cat_id      = self.sub_cat_id,
            user_id         = self.user_id,
            need            = format_price(self.need),
            item_id         = self.item_id,
            price           = format_price(self.price),
            status          = self.status,
            end_time        = str(self.end_time),
            create_time     = str(self.create_time),
            coupon_id       = self.coupon_id,
            remark          = self.remark,
            )


class PeriodPayChoice(Model):
    ''' 分期费率表 '''
    id                 = db.Column(Integer, primary_key=True)
    period_count       = Column(Integer, nullable=False, unique=True) #分期数
    period_fee         = Column(Float, nullable=False)              #分期税率

    def as_dict(self):
        return dict(
            id           = self.id,
            period_count = self.period_count,
            period_fee   = self.period_fee,
        )


class PeriodPayLog(Model):
    '''
    *滞纳金动态计算*
    每期还款额列表建模
    '''
    id                 = db.Column(Integer, primary_key=True)
    amount             = Column(MoneyField, nullable=False, default=0) #每期金额
    fee                = Column(MoneyField, nullable=False, default=0) #每期手续费用
    punish             = Column(MoneyField, nullable=False, default=0) #预期滞纳金
    user_id            = Column(Integer, ForeignKey('user.id'), nullable=False)
    order_id           = Column(Integer, ForeignKey('order.id'), nullable=True)
    period_pay_index   = Column(Integer, nullable=True)  #分期应该还的第几期
    period_count       = Column(Integer, nullable=True)  #分期总数
    create_time        = Column(DateTime, default=dt_obj.now)
    deadline           = Column(DateTime)#还款日
    repayment_time     = Column(DateTime)#实际还款日
    status             = Column(TINYINT(1), nullable=False, default=0)#0待还 1已还 2 已取消

    def as_dict(self):
        return dict(
            id          = self.id,
            amount      = format_price(self.amount or 0),
            punish      = format_price(self.punish or 0),
            period_count= self.period_count,
            fee         = float(self.fee or 0),
            user_id     = self.user_id,
            order_id    = self.order_id,
            period_pay_index = self.period_pay_index,
            deadline    = str(self.deadline),
            repayment_time = str(self.repayment_time or ''),
            create_time = self.create_time,
            status      = self.status,
        )


class PunishLog(Model):
    '''滞纳金产生 历史'''
    id                 = db.Column(Integer, primary_key=True)
    log_id             = Column(Integer, ForeignKey('period_pay_log.id'), nullable=True)
    amount             = Column(MoneyField, nullable=False, default=0)
    create_time        = Column(DateTime, default=dt_obj.now)


class CreditUseLog(Model):
    ''' 可用信用额度使用历史 '''
    id                 = db.Column(Integer, primary_key=True)
    user_id            = Column(Integer, ForeignKey('user.id'), nullable=False)
    amount             = Column(MoneyField, nullable=False, default=0)
    order_id           = Column(Integer, ForeignKey('order.id'), nullable=True)
    status             = Column(TINYINT(1), nullable=False, default=0)#额度当期状态
    create_time        = Column(DateTime, default=dt_obj.now)


class CreditChangeLog(Model):
    ''' 信用总额变更历史 '''
    id                 = db.Column(Integer, primary_key=True)
    user_id            = Column(Integer, ForeignKey('user.id'), nullable=False)
    amount             = Column(MoneyField, nullable=False, default=0)
    create_time        = Column(DateTime, default=dt_obj.now)


class UserCredit(Model):
    ''' 用户信用额度 '''
    id                 = db.Column(Integer, primary_key=True)
    user_id            = Column(Integer, ForeignKey('user.id'), nullable=False)
    total              = Column(MoneyField, nullable=False, default=0)#总额度
    used               = Column(MoneyField, nullable=False, default=0) #已使用额度
    status             = Column(TINYINT(1), nullable=False, default=CREDIT_STATUS.DEFAULT)#0默认 1审核中 2审核通过 3被拒

    def as_dict(self):
        return dict(
            id          = self.id,
            user_id     = self.user_id,
            total       = format_price(self.total or 0),
            used        = format_price(self.used or 0),
            status      = self.status
        )


class Hospital(Model):
    ''' 医院 '''
    id                 = db.Column(Integer, primary_key=True)
    name               = db.Column(String(100))
    city_id            = Column(Integer, ForeignKey('city.id'), nullable=True)
    image              = db.Column(String(100))
    phone              = db.Column(String(100))
    desc               = db.Column(String(10000))
    tags               = db.Column(String(1000)) #逗号分割的医院标签
    addr               = db.Column(String(300)) #地址
    working_time       = db.Column(String(100)) #工作时间
    long_lat           = db.Column(String(30)) #经纬度
    photos             = db.Column(String(1000))
    rate               = Column(Float, default=5) #评分
    sold_count         = db.Column(Integer, default=0) #已售数量
    status             = Column(TINYINT(1), nullable=False, default=0)#0下线 1上线

    def as_dict(self):
        return dict(
            id              = self.id,
            status          = self.status,
            city_id         = self.city_id,
            sold_count      = self.sold_count or 0,
            photo_list      = prefix_img_list(self.photos),
            image           = prefix_img_domain(self.image),
            photos          = self.photos,
            name            = self.name,
            rate            = format_rate(self.rate or 5),
            phone           = self.phone,
            desc            = self.desc,
            working_time    = self.working_time,
            tag_list        = comma_str_to_list(self.tags),
            tags            = self.tags,
            addr            = self.addr,
            long_lat        = self.long_lat,
            lng             = self.long_lat.split(',')[0] if self.long_lat else '',
            lat             = self.long_lat.split(',')[1] if self.long_lat else '',
            )



class ItemCat(Model):
    ''' 分类 '''
    id                 = db.Column(Integer, primary_key=True)
    name               = db.Column(String(100), unique=True)
    sort_order         = Column(Integer, default=0) #小的排在前面
    status             = Column(TINYINT(1), nullable=False, default=0)#0未上线 1已上线

    def as_dict(self):
        return dict(
            id          = self.id,
            name        = self.name,
            status      = self.status,
            sort_order  = self.sort_order
        )


class ItemSubCat(Model):
    ''' 子分类 '''
    id                 = db.Column(Integer, primary_key=True)
    name               = db.Column(String(100))
    desc               = db.Column(String(1000))
    icon               = db.Column(String(100))
    cat_id             = Column(Integer, ForeignKey('item_cat.id'), nullable=False)#父分类id
    cat_ids            = db.Column(String(500))
    status             = Column(TINYINT(1), nullable=False, default=0)#0未上线 1已上线

    def as_dict(self):
        return dict(
            id              = self.id,
            name            = self.name,
            desc            = self.desc,
            cat_ids         = self.cat_ids,
            cat_id_list     = str_to_int_list(self.cat_ids),
            icon            = prefix_img_domain(self.icon),
            cat_id          = self.cat_id,
            status          = self.status
            )


class Item(Model):
    ''' 商品 '''
    id                 = db.Column(Integer, primary_key=True)
    orig_price         = Column(MoneyField, nullable=False, default=0)
    price              = Column(MoneyField, nullable=False, default=0)
    sub_cat_id         = Column(Integer, ForeignKey('item_sub_cat.id'), nullable=False)#子分类id
    hospital_id        = Column(Integer, ForeignKey('hospital.id'), nullable=False)
    sub_cat_ids        = db.Column(String(100))
    image              = db.Column(String(300))
    photos             = db.Column(String(1000))
    title              = db.Column(String(500))
    item_no            = db.Column(String(100), index=True) #项目编号
    support_choices    = db.Column(String(50)) #支持的分期数选项
    sold_count         = db.Column(Integer, default=0) #已售数量
    has_fee            = Column(Boolean, default=True) #是否免息
    direct_buy         = Column(Boolean) #是否可以直接购买
    status             = Column(TINYINT(1), nullable=False, default=0)#0未上线 1已上线 2医院被下线
    surgery_desc       = Column(Text)
    doctor_desc        = Column(Text)
    create_time        = Column(DateTime, default=dt_obj.now)
    use_time           = db.Column(String(300))
    note               = db.Column(String(500)) #提示
    def as_dict(self):
        return dict(
            id              = self.id,
            sub_cat_id      = self.sub_cat_id,
            title           = self.title,
            sub_cat_ids     = self.sub_cat_ids,
            sub_cat_id_list = map(int, filter(bool, (self.sub_cat_ids or '').split(','))),
            direct_buy      = bool(self.direct_buy),
            price           = format_price(self.price or 0),
            orig_price      = format_price(self.orig_price or 0),
            photos          = self.photos,
            item_no         = str(self.id),
            hospital_id     = self.hospital_id,
            sold_count      = self.sold_count or 0,
            image           = prefix_img_domain(self.image),
            photo_list      = prefix_img_list(self.photos) if self.photos else [],
            support_choices     = self.support_choices,
            support_choice_list = str_to_int_list(self.support_choices),
            status          = self.status,
            surgery_desc    = self.surgery_desc,
            use_time        = self.use_time,
            note            = self.note,
            doctor_desc     = self.doctor_desc,
            has_fee         = bool(self.has_fee),
            create_time     = self.create_time,
        )


class ItemComment(Model):
    ''' 商品评价 '''
    id                 = db.Column(Integer, primary_key=True)
    item_id            = Column(Integer, ForeignKey('item.id'))
    user_id            = Column(Integer, ForeignKey('user.id'))
    order_id           = Column(Integer, ForeignKey('order.id'))
    photos             = db.Column(String(1000))
    content            = db.Column(String(10000))
    rate               = Column(Float, default=0) #评分
    is_anonymous       = Column(Boolean, default=False)
    is_re_comment      = Column(Boolean, default=False)
    create_time        = Column(DateTime, default=dt_obj.now)

    def as_dict(self):
        return dict(
            id              = self.id,
            is_anonymous    = self.is_anonymous,
            is_re_comment   = bool(self.is_re_comment),
            item_id         = self.item_id,
            order_id        = self.order_id,
            user_id         = self.user_id,
            rate            = self.rate or 0,
            photos          = self.photos,
            photo_list      = prefix_img_list(self.photos) if self.photos else [],
            thumb_photo_list= prefix_img_list_thumb(self.photos) if self.photos else [],
            content         = self.content,
            create_time     = str(self.create_time)
        )


class ItemFav(Model):
    ''' 心愿单 '''
    __table_args__  = (
        UniqueConstraint('user_id', 'item_id'),
    )
    id                 = db.Column(Integer, primary_key=True)
    item_id            = Column(Integer, ForeignKey('item.id'))
    user_id            = Column(Integer, ForeignKey('user.id'))
    create_time        = Column(DateTime, default=dt_obj.now)

    def as_dict(self):
        return dict(
            id          = self.id,
            item_id     = self.item_id,
            user_id     = self.user_id,
            create_time = str(self.create_time)
            )


class UserAdvice(Model):
    ''' 用户反馈 '''
    id                 = db.Column(Integer, primary_key=True)
    user_id            = Column(Integer, ForeignKey('user.id'), nullable=True)
    content            = db.Column(String(10000))
    contact            = db.Column(String(100))
    create_time        = Column(DateTime, default=dt_obj.now)
    remark             = db.Column(String(300))

    def as_dict(self):
        return dict(
            id          = self.id,
            user_id     = self.user_id,
            content     = self.content,
            contact     = self.contact,
            create_time = self.create_time,
            remark      = self.remark
            )


class ServiceCode(Model):
    ''' 预约服务码 '''
    id                 = db.Column(Integer, primary_key=True)
    order_id           = Column(Integer, ForeignKey('order.id'), unique=True)  
    code               = Column(String(100), index=True, unique=True) 
    status             = Column(TINYINT(1), nullable=False, default=0) #0未使用 1已预约 2已确认
    book_time          = Column(DateTime) #预约时间
    create_time        = Column(DateTime, default=dt_obj.now)

    def as_dict(self):
        return dict(
            id          = self.id,
            order_id    = self.order_id,
            code        = self.code,
            book_time   = self.book_time,
            status      = self.status
            )


class PayNotifyLog(Model):
    ''' 通知回调日志 '''
    id                 = db.Column(Integer, primary_key=True)
    pay_type           = Column(TINYINT(1), nullable=False, default=0) #1微信公众号 2微信app 3支付宝
    content            = db.Column(String(10000))
    create_time        = Column(DateTime, default=dt_obj.now)


class OrderLog(Model):
    ''' 订单状态变更日志 '''
    id                 = db.Column(Integer, primary_key=True)
    order_id           = Column(Integer, ForeignKey('order.id'))  
    status             = Column(TINYINT(1), nullable=False) #订单当前状态
    remark             = db.Column(String(100))
    create_time        = Column(DateTime, default=dt_obj.now)


class CreditApply(Model):
    ''' 额度申请 大学学生升到了研究生后，学历信息/毕业时间需要提醒她们更改 '''
    id                 = db.Column(Integer, primary_key=True)
    user_id            = Column(Integer, ForeignKey('user.id'), unique=True)
    name               = db.Column(String(100)) #姓名
    id_no              = db.Column(String(18)) #身份证号码
    school             = db.Column(String(100)) #学校名字
    enrollment_time    = Column(DateTime) #入学时间
    major              = db.Column(String(100)) #专业
    stu_no             = db.Column(String(20)) #学号
    stu_education      = db.Column(String(20)) #学历
    stu_years          = Column(Float, default=4) #学制
    addr               = db.Column(String(100)) #地址
    parent_contact     = db.Column(String(100)) #父母联系方式
    chsi_name          = db.Column(String(100)) #学信网账号
    chsi_passwd        = db.Column(String(100)) #学信网密码
    id_card_photo      = db.Column(String(100)) #身份证照
    stu_card_photo     = db.Column(String(100)) #学生证照
    body_choice_ids    = db.Column(String(100)) #部位id
    body_choice_text   = db.Column(String(100)) #其他内容
    create_time        = Column(DateTime, default=dt_obj.now)
    update_time        = Column(DateTime, default=dt_obj.now)
    graduate_time      = Column(DateTime)
    has_supply         = Column(Boolean, default=False) #资料已经从学信网补充
    reason             = db.Column(String(500)) #被拒原因
    status             = Column(TINYINT(1), nullable=False, default=1) #1第一步 2第二步 3通过 4被拒绝
    remark             = db.Column(String(500)) #备注
    remark_img         = db.Column(String(500)) #备注图片


    def as_dict(self):
        return dict(
            id          = self.id,
            id_no       = self.id_no or '',
            stu_education = self.stu_education,
            create_time = self.create_time,
            update_time = self.update_time,
            status      = self.status,
            name        = self.name or '',
            stu_no      = self.stu_no,
            user_id     = self.user_id,
            school      = self.school,
            enrollment_time = self.enrollment_time,
            major           = self.major,
            addr            = self.addr,
            graduate_time   = self.graduate_time,
            chsi_name       = self.chsi_name or '',
            chsi_passwd     = self.chsi_passwd or '',
            parent_contact  = self.parent_contact or '',
            stu_years       = self.stu_years,
            reason          = self.reason or '',
            id_card_photo   = prefix_img_domain(self.id_card_photo),
            stu_card_photo  = prefix_img_domain(self.stu_card_photo),
            id_card_photo_key = self.id_card_photo,
            stu_card_photo_key= self.stu_card_photo,
            has_supply        = self.has_supply,
            body_choice_ids   = self.body_choice_ids,
            body_choice_text  = self.body_choice_text,
            remark            = self.remark,
            remark_img        = prefix_img_domain(self.remark_img),
            )


class School(Model):
    ''' 学校 '''
    id                 = db.Column(Integer, primary_key=True)
    name               = db.Column(String(100), unique=True) #学校名字
    city_name          = db.Column(String(100)) #城市名字
    link               = db.Column(String(100)) #链接
    pics_count         = db.Column(Integer, default=0, index=True) #图片数量

    def as_dict(self):
        return dict(
            id          = self.id,
            name        = self.name,
            link        = prefix_http(self.link),
            city_name   = self.city_name,
            pics_count  = self.pics_count or 0
        )


class AdminUser(Model):
    ''' 管理员 '''
    id                 = db.Column(Integer, primary_key=True)
    name               = db.Column(String(100), unique=True)
    city_id            = Column(Integer, ForeignKey('city.id'))
    passwd             = db.Column(String(100))
    cat                = Column(TINYINT(1), nullable=False, default=0)#0所有权限 1编辑 2推广
    create_time        = Column(DateTime, default=dt_obj.now)


class City(Model):
    ''' 城市 '''
    id                 = db.Column(Integer, primary_key=True)
    name               = db.Column(String(100), unique=True)
    city_code          = db.Column(String(30), unique=True) #百度cityCode
    amap_code          = db.Column(String(30), unique=True) #高德地图cityCode

    def as_dict(self):
        return dict(
            id          = self.id,
            name        = self.name,
            amap_code   = self.amap_code,
            city_code   = self.city_code
            )


class Repayment(Model):
    ''' 还款订单 '''
    id                 = db.Column(Integer, primary_key=True)
    user_id            = Column(Integer, ForeignKey('user.id'))
    pay_method         = Column(TINYINT(1), nullable=False, default=0)#0没用付钱(可能是全部使用优惠券或信用额度) 1微信 2支付宝
    coupon_id          = Column(Integer, ForeignKey('user_coupon.id'), nullable=True, unique=True)
    price              = Column(MoneyField, nullable=False, default=0) #每期手续费用
    data               = db.Column(String(10000)) #还了哪些期 还款时的每期金额
    order_no           = db.Column(String(30), unique=True)
    transaction_id     = db.Column(String(100))
    create_time        = Column(DateTime, default=dt_obj.now)
    update_time        = Column(DateTime, default=dt_obj.now)
    status             = Column(TINYINT(1), nullable=False, default=0) #0待支付 1支付中 2支付成功

    def as_dict(self):
        ''' '''
        return dict(
            id          = self.id,
            pay_method  = self.pay_method,
            coupon_id   = self.coupon_id,
            data        = self.data,
            price       = format_price(self.price),
            order_no    = self.order_no,
            create_time = self.create_time,
            update_time = self.update_time,
            status      = self.status,
            transaction_id = self.transaction_id
            )


class HospitalUser(Model):
    ''' 医院管理员 '''
    id                 = db.Column(Integer, primary_key=True)
    hospital_id        = Column(Integer, ForeignKey('hospital.id'))
    name               = db.Column(String(100), unique=True)
    passwd             = db.Column(String(100))
    create_time        = Column(DateTime, default=dt_obj.now)

    def as_dict(self):
        return dict(
            id          = self.id,
            hospital_id = self.hospital_id,
            name        = self.name,
            create_time = self.create_time
            )


class HelpCat(Model):
    ''' 帮助分类 '''
    id                 = db.Column(Integer, primary_key=True)
    name               = db.Column(String(100), unique=True)

    def as_dict(self):
        return dict(
            id          = self.id,
            name        = self.name,
            )


class HelpEntry(Model):
    ''' 帮助条目 '''
    id                 = db.Column(Integer, primary_key=True)
    title              = db.Column(String(100))
    cat_id             = Column(Integer, ForeignKey('help_cat.id'))
    content            = db.Column(String(10000))

    def as_dict(self):
        return dict(
            id          = self.id,
            title       = self.title,
            cat_id      = self.cat_id,
            content     = self.content
            )


class Activity(Model):
    ''' 活动 '''
    id                 = db.Column(Integer, primary_key=True)
    title              = db.Column(String(300))
    city_id            = Column(Integer, ForeignKey('city.id'))
    desc               = db.Column(String(1000))
    start_time         = Column(DateTime)
    end_time           = Column(DateTime)
    create_time        = Column(DateTime, default=dt_obj.now)

    def as_dict(self):
        return dict(
            id          = self.id,
            title       = self.title,
            city_id     = self.city_id,
            desc        = self.desc,
            start_time  = self.start_time,
            end_time    = self.end_time,
            create_time = self.create_time
        )


class ActivityItem(Model):
    ''' 活动商品 '''
    id                 = db.Column(Integer, primary_key=True)
    activity_id        = Column(Integer, ForeignKey('activity.id'))
    item_id            = Column(Integer, ForeignKey('item.id'))
    sort_order         = Column(Integer, default=0) #小的排在前面
    price              = Column(MoneyField, nullable=False, default=0) #活动价格
    image              = db.Column(String(300))

    def as_dict(self):
        return dict(
            id          = self.id,
            image       = prefix_img_domain(self.image),
            activity_id = self.activity_id,
            item_id     = self.item_id,
            price       = format_price(self.price),
            sort_order  = self.sort_order
            )


class RecommendItem(Model):
    ''' 推荐商品 '''
    id                 = db.Column(Integer, primary_key=True)
    item_id            = Column(Integer, ForeignKey('item.id'), unique=True)
    sort_order         = Column(Integer, default=0) #小的排在前面
    image              = db.Column(String(300))
    desc               = db.Column(String(500))

    def as_dict(self):
        return dict(
            id          = self.id,
            sort_order  = self.sort_order,
            item_id     = self.item_id,
            image       = prefix_img_domain(self.image),
            desc        = self.desc
            )



class RecommendSubcat(Model):
    ''' 推荐商品子分类 '''
    id                 = db.Column(Integer, primary_key=True)
    sub_cat_id         = Column(Integer, ForeignKey('item_sub_cat.id'), unique=True)
    sort_order         = Column(Integer, default=0) #小的排在前面
    icon               = db.Column(String(300))

    def as_dict(self):
        return dict(
            id          = self.id,
            sort_order  = self.sort_order,
            sub_cat_id  = self.sub_cat_id,
            icon        = prefix_img_domain(self.icon)
            )


class EditNameLog(Model):
    ''' 名字修改记录 '''
    id                 = db.Column(Integer, primary_key=True)
    user_id            = Column(Integer, ForeignKey('user.id'))
    create_time        = Column(DateTime, default=dt_obj.now)

    def as_dict(self):
        return dict(
            id          = self.id,
            user_id     = self.user_id,
            create_time = self.create_time
            )


class PayLogOrderNo(Model):
    ''' 还款期记录对应 订单号
        还款后取消订单的操作是： 退换已还的款项， 将未还的log至为status 2
    '''
    id                 = db.Column(Integer, primary_key=True)
    order_no           = db.Column(String(30), index=True)
    period_pay_log_id  = Column(Integer, ForeignKey('period_pay_log.id'), unique=True)
    price              = Column(MoneyField, nullable=False, default=0) #还款金额
    total              = Column(MoneyField, nullable=False, default=0) #总还款金额
    create_time        = Column(DateTime, default=dt_obj.now)   



class QrCodeUser(Model):
    ''' 扫描二维码关注用户
    '''
    id                 = db.Column(Integer, primary_key=True)
    open_id            = db.Column(String(50), unique=True) #唯一索引
    qrcode_id          = Column(Integer, ForeignKey('qrcode.id'), nullable=True)
    user_id            = Column(Integer, ForeignKey('user.id'), nullable=True)
    sex                = Column(Integer, default=0)
    city               = db.Column(String(100))
    headimgurl         = db.Column(String(300))
    nickname           = db.Column(String(100))
    location           = db.Column(String(100))
    lnglat             = db.Column(String(100))
    create_time        = Column(DateTime, default=dt_obj.now)   
    status             = Column(TINYINT(1), default=1, index=True) #0取消关注 1已关注 -1未曾关注

    def as_dict(self):
        return dict(
            id      = self.id,
            open_id = self.open_id,
            qrcode_id = self.qrcode_id,
            user_id     = self.user_id,
            sex         = self.sex,
            headimgurl  = self.headimgurl or DEFAULT_IMAGE,
            city        = self.city,
            nickname    = self.nickname,
            location    = self.location,
            lnglat      = self.lnglat,
            create_time = self.create_time,
            status      = self.status,
            )


class Promoter(Model):
    ''' 推广员 '''
    id                 = db.Column(Integer, primary_key=True)
    phone              = db.Column(String(20), unique=True)
    name               = db.Column(String(50))
    passwd             = db.Column(String(50))
    follow_count       = Column(Integer, default=0, index=True) #关注数
    reg_count          = Column(Integer, default=0, index=True) #注册数
    dup_count          = Column(Integer, default=0, index=True) #重复注册数
    unfollow_count     = Column(Integer, default=0, index=True) #取消关注数
    create_time        = Column(DateTime, default=dt_obj.now)
    create_by          = Column(Integer, ForeignKey('promoter.id'), nullable=True)
    status             = Column(TINYINT(1), nullable=False, default=1) #0已下线 1可创建二维码 2不可创建二维码

    def as_dict(self):
        return dict(
            id          = self.id,
            dup_count   = self.dup_count,
            phone       = self.phone,
            name        = self.name,
            passwd      = self.passwd,
            create_by   = self.create_by,
            follow_count= self.follow_count,
            reg_count   = self.reg_count,
            unfollow_count= self.unfollow_count,
            status      = self.status
            )


class Qrcode(Model):
    ''' 二维码id '''
    id                 = db.Column(Integer, primary_key=True)
    ticket             = db.Column(String(100))
    image              = db.Column(String(300))
    act_type           = db.Column(Integer, default=0) #推广活动类型  9现金活动
    promoter_id        = Column(Integer, ForeignKey('promoter.id'), nullable=False)
    create_time        = Column(DateTime, default=dt_obj.now)

    def as_dict(self):
        return dict(
            id          = self.id,
            ticket      = self.ticket,
            image       = prefix_img_domain(self.image),
            promoter_id = self.promoter_id,
            create_time = self.create_time,
            act_type    = self.act_type
            )


class WechatLocation(Model):
    ''' 微信定位 '''
    id                 = db.Column(Integer, primary_key=True)
    open_id            = db.Column(String(50), index=True) #用户open_id
    lng                = db.Column(String(50))
    lat                = db.Column(String(50))
    create_time        = Column(DateTime, default=dt_obj.now)

    def as_dict(self):
        return dict(
            id          = self.id,
            open_id     = self.open_id,
            lng         = self.lng,
            lat         = self.lat,
            create_time = self.create_time
            )



class FakeUser(Model):
    ''' 假用户 '''
    id                 = db.Column(Integer, primary_key=True)
    user_id            = Column(Integer, ForeignKey('user.id'), nullable=False)


class Trial(Model):
    ''' 试用 '''
    id                 = db.Column(Integer, primary_key=True)
    title              = db.Column(String(300))
    image              = db.Column(String(300))     #图片
    cat                = Column(Integer, default=0) #试用类型 0免费礼品 1特定项目代金券
    coupon_id          = Column(Integer, ForeignKey('coupon.id'), nullable=True)
    total              = Column(Integer, default=0) #申请数
    sent               = Column(Integer, default=0) #已发放数
    sort_order         = Column(Integer, default=0) #试用排序
    apply_count        = Column(Integer, default=0) #人气
    rules              = db.Column(Text)            #试用规则
    process            = db.Column(Text)            #流程
    create_time        = Column(DateTime, default=dt_obj.now)
    start_time         = Column(DateTime)
    end_time           = Column(DateTime)

    def as_dict(self):
        return dict(
            id      = self.id,
            title   = self.title,
            image   = prefix_img_domain(self.image),
            cat     = self.cat,
            cat_str = '免费, 包邮' if self.cat==0 else '免费',
            total   = self.total,
            coupon_id       = self.coupon_id,
            sent            = self.sent,
            sort_order      = self.sort_order,
            apply_count     = self.apply_count,
            rules           = self.rules,
            process         = self.process,
            create_time     = self.create_time,
            end_time        = self.end_time,
            start_time      = self.start_time,
            )



class TrialApply(Model):
    ''' 试用申请 '''
    __table_args__  = (
        UniqueConstraint('user_id', 'trial_id'),
    )

    id                 = db.Column(Integer, primary_key=True)
    user_id            = Column(Integer, ForeignKey('user.id'), nullable=False)
    trial_id           = Column(Integer, ForeignKey('trial.id'), nullable=False)
    cat                = Column(Integer, default=0) #试用类型 0免费礼品 1特定项目代金券
    coupon_id          = Column(Integer, ForeignKey('user_coupon.id'), nullable=True)
    name               = db.Column(String(100))
    phone              = db.Column(String(30))
    school             = db.Column(String(100))
    sex                = Column(TINYINT(1), nullable=False, default=0) #0保密 1男 2女
    addr               = db.Column(String(100))
    content            = db.Column(String(1000))
    create_time        = Column(DateTime, default=dt_obj.now) #创建时间
    status             = Column(TINYINT(1), nullable=False, default=0) #0等待审核 1获得资格

    def as_dict(self):
        return dict(
            id          = self.id,
            sex         = self.sex,
            cat         = self.cat,
            coupon_id   = self.coupon_id,
            user_id     = self.user_id,
            trial_id    = self.trial_id,
            name        = self.name,
            phone       = self.phone,
            school      = self.school,
            addr        = self.addr,
            content     = self.content,
            create_time = self.create_time,
            status      = self.status
            )


class TrialComment(Model):
    ''' 体会评价 '''
    id                 = db.Column(Integer, primary_key=True)
    user_id            = Column(Integer, ForeignKey('user.id'), nullable=False)
    trial_id           = Column(Integer, ForeignKey('trial.id'), nullable=False)
    photos             = db.Column(String(1000))
    content            = db.Column(String(10000))
    create_time        = Column(DateTime, default=dt_obj.now) #创建时间

    def as_dict(self):
        return dict(
            id          = self.id,
            user_id     = self.user_id,
            trial_id    = self.trial_id,
            photos      = self.photos,
            content     = self.content,
            create_time = self.create_time,
            photo_list  = prefix_img_list(self.photos)
            )


class ImageSize(Model):
    __tablename__   = 'image_size' 
    __table_args__  = (
        PrimaryKeyConstraint('key'),
    )
    key             = Column(String(32))
    width           = Column(Integer, default=0)
    height          = Column(Integer, default=0)

    def as_dict(self):
        return dict(
            key     = self.key,
            width   = self.width,
            height  = self.height
            )


class WechatReg(Model):
    ''' 体会评价 '''
    id                 = db.Column(Integer, primary_key=True)
    user_id            = Column(Integer, ForeignKey('user.id'), nullable=False)
    open_id            = db.Column(String(100))
    create_time        = Column(DateTime, default=dt_obj.now) #创建时间


class RecommendBeautyItem(Model):
    ''' 美攻略推荐项目 '''
    id                 = db.Column(Integer, primary_key=True)
    item_id            = Column(Integer, ForeignKey('item.id'), nullable=False)
    create_time        = Column(DateTime, default=dt_obj.now) #创建时间

    def as_dict(self):
        return dict(
            id          = self.id,
            item_id     = self.item_id,
            create_time = self.create_time
            )


class BeautyEntry(Model):
    ''' 美攻略 '''
    id                 = db.Column(Integer, primary_key=True)
    title              = db.Column(String(100))
    icon               = db.Column(String(100)) #列表图
    image              = db.Column(String(100)) #首页图
    photo              = db.Column(String(100)) #详情页大图
    items              = db.Column(String(100))
    view_count         = Column(Integer, default=0)
    create_time        = Column(DateTime, default=dt_obj.now)
    status             = Column(TINYINT(1), nullable=False, default=0)#0未上线 1上线

    def as_dict(self):
        return dict(
            id          = self.id,
            icon        = prefix_img_domain(self.icon),
            view_count  = self.view_count,
            title       = self.title,
            image       = prefix_img_domain(self.image),
            photo       = prefix_img_domain(self.photo),
            items       = self.items,
            item_id_list= map(int, filter(bool, (self.items or '').split(','))),
            status      = self.status,
            create_time = self.create_time
            )


class DailyCoupon(Model):
    ''' 每日优惠券 '''
    id                 = db.Column(Integer, primary_key=True)
    coupon_id          = Column(Integer, ForeignKey('coupon.id'), nullable=False)
    start_time         = Column(DateTime)
    end_time           = Column(DateTime)
    total              = Column(Integer, default=0)
    sent               = Column(Integer, default=0)
    title              = db.Column(String(100))
    use_condition      = db.Column(String(100))
    use_time           = db.Column(String(100))
    create_time        = Column(DateTime, default=dt_obj.now)

    def as_dict(self):
        return dict(
            id          = self.id,
            title       = self.title,
            coupon_id   = self.coupon_id,
            start_time  = self.start_time,
            use_time    = self.use_time or '',
            use_condition = self.use_condition or '',
            end_time    = self.end_time,
            sent        = self.sent or 0,
            total       = self.total or 0,
            remain      = self.total-self.sent,
            create_time = self.create_time
            )


class DailyUser(Model):
    ''' 用户每日优惠券 '''
    __table_args__  = (
        UniqueConstraint('daily_id', 'user_id'),
    )

    id                 = db.Column(Integer, primary_key=True)
    user_id            = Column(Integer, ForeignKey('user.id'), nullable=False)
    daily_id           = Column(Integer, ForeignKey('daily_coupon.id'), nullable=False)
    create_time        = Column(DateTime, default=dt_obj.now)

    def as_dict(self):
        return dict(
            id      = self.id,
            user_id = self.user_id,
            daily_id= self.daily_id,
            create_time=self.create_time
            )


class AlipayOrderUser(Model):
    ''' 支付宝支付订单对应用户支付宝账号 '''
    id                 = db.Column(Integer, primary_key=True)
    order_no           = db.Column(String(100), unique=True)
    buyer_email        = db.Column(String(100), index=True)
    create_time        = Column(DateTime, default=dt_obj.now)



class RecommendHospital(Model):
    ''' 推荐医院 '''
    id                 = db.Column(Integer, primary_key=True)
    hospital_id        = Column(Integer, ForeignKey('hospital.id'), unique=True)
    sort_order         = Column(Integer, default=0) #小的排在前面
    tag                = db.Column(String(50))
    color              = db.Column(String(50))

    def as_dict(self):
        return dict(
            id          = self.id,
            hospital_id = self.hospital_id,
            sort_order  = self.sort_order,
            tag         = self.tag,
            color       = self.color
            )


class Article(Model):
    ''' 通知文章 '''
    id                 = db.Column(Integer, primary_key=True)
    title              = db.Column(String(300))
    desc               = db.Column(String(1000))
    image              = db.Column(String(300))
    link               = db.Column(String(300))
    create_time        = Column(DateTime, default=dt_obj.now)
    status             = Column(TINYINT(1), nullable=False, default=0) #0未上线 1上线

    def as_dict(self):
        return dict(
            id          = self.id,
            title       = self.title,
            desc        = self.desc,
            image       = self.image,
            link        = self.link,
            create_time = self.create_time,
            status      = self.status
            )
 

class Notification(Model):
    ''' 消息通知 '''
    id                 = db.Column(Integer, primary_key=True)
    article_id         = Column(Integer, ForeignKey('article.id'))
    user_id            = Column(Integer, ForeignKey('user.id'))
    create_time        = Column(DateTime, default=dt_obj.now)
    status             = Column(TINYINT(1), nullable=False, default=0) #0未读 1已读

    def as_dict(self):
        return dict(
            id          = self.id,
            user_id     = self.user_id,
            article_id  = self.article_id,
            create_time = self.create_time,
            status      = self.status
            )



class RoomDesignDetail(Model):
    ''' 寝室设计详情 '''
    id                  = Column(Integer, primary_key=True)
    room_name           = Column(String(30), unique=True)
    applyer_name        = Column(String(30))
    addr                = Column(String(30))
    phone               = Column(String(30), unique=True)
    user_id             = Column(Integer, ForeignKey('user.id'))
    school_id           = Column(Integer, ForeignKey('school.id'))
    apply_no            = Column(String(30), unique=True) #编号
    pics                = Column(String(500))
    vote_count          = db.Column(Integer, default=0) #投票数量数量
    pics_count          = db.Column(Integer, default=0, index=True) #图片数量
    create_time         = Column(DateTime, default=dt_obj.now)

    def as_dict(self):
        result = dict(
            id          = self.id,
            room_name   = self.room_name,
            apply_no    = self.apply_no,
            addr        = self.addr,
            phone       = self.phone,
            applyer_name= self.applyer_name,
            school_id   = self.school_id,
            vote_count  = self.vote_count,
            pics_count  = self.pics_count,
            user_id     = self.user_id,
            pics        = self.pics,
            orig_pics   = imgs_to_list(self.pics),
            create_time = self.create_time,
            pic_list    = prefix_img_list_thumb(self.pics, width=720),
            thumb_pic_list = prefix_img_list_thumb(self.pics),
        )
        if len(result['pic_list'])<4:
            for i in range(4-len(result['pic_list'])):
                result['pic_list'].append('')
        if len(result['thumb_pic_list'])<4:
            for i in range(4-len(result['thumb_pic_list'])):
                result['thumb_pic_list'].append('')
        return result


class RoomDesignVotePrivilege(Model):
    ''' 投票权限 '''
    id                 = Column(Integer, primary_key=True)
    user_id            = Column(Integer, ForeignKey('user.id'))
    status             = Column(TINYINT(1), nullable=False, default=0) #0未使用 1已使用
    source             = Column(TINYINT(1), nullable=False, default=0) #1完成申请额度(20票) 2完成一单(200票)
    create_time        = Column(DateTime, default=dt_obj.now)

    def as_dict(self):
        return dict(
            id      = self.id,
            user_id = self.user_id,
            status  = self.status,
            source  = self.source,
            create_time = self.create_time
            )


class RoomDesignVoteLog(Model):
    ''' 投票记录log '''
    id                  = Column(Integer, primary_key=True)
    user_id             = Column(Integer, ForeignKey('user.id'))
    room_id             = Column(Integer, ForeignKey('room_design_detail.id'))
    source              = Column(TINYINT(1), nullable=False, default=0) #1完成申请额度(20票) 2完成一单(200票)
    create_time         = Column(DateTime, default=dt_obj.now)

    def as_dict(self):
        return dict(
            id      = self.id,
            user_id = self.user_id,
            room_id = self.room_id,
            source  = self.source,
            create_time= self.create_time
        )



class RedpackQuestion(Model):
    ''' 红包推荐问题 '''
    id                  = Column(Integer, primary_key=True)
    content             = Column(String(1000))
    create_time         = Column(DateTime, default=dt_obj.now)
    status              = Column(TINYINT(1), nullable=False, default=0) #0下线 1上线

    def as_dict(self):
        return dict(
            id          = self.id,
            content     = self.content,
            create_time = self.create_time,
            status      = self.status
            )


class RedpackUserQuestion(Model):
    ''' 红包用户问答 '''
    id                  = Column(Integer, primary_key=True)
    qr_user_id          = Column(Integer, ForeignKey('qr_code_user.id'))
    question_id         = Column(Integer, ForeignKey('redpack_question.id'))
    price               = Column(MoneyField) #需支付价格
    question            = Column(String(1000))
    answer              = Column(String(1000))
    is_custom           = Column(TINYINT(1), nullable=False, default=0) #0美分分提供问题 1自定义问题
    is_random           = Column(TINYINT(1), nullable=False, default=0) #0不随机 1随机
    price               = Column(MoneyField) #需支付价格
    money               = Column(MoneyField, default=0) #总收到金额
    status              = Column(TINYINT(1), nullable=False, default=0) #0新下单 1支付中 2支付成功
    view_count          = db.Column(Integer, default=0) #查看数量
    create_time         = Column(DateTime, default=dt_obj.now)

    def as_dict(self):
        return dict(
            id          = self.id,
            view_count  = self.view_count or 0,
            qr_user_id  = self.qr_user_id,
            question_id = self.question_id,
            is_custom   = self.is_custom,
            is_random   = self.is_random,
            question    = self.question,
            answer      = self.answer,
            price       = format_price(self.price),
            money       = format_price(self.money),
            status      = self.status,
            create_time = self.create_time
            )


class RedpackPay(Model):
    ''' 红包支付纪录 '''
    id                  = Column(Integer, primary_key=True)
    qr_user_id          = Column(Integer, ForeignKey('qr_code_user.id'))
    user_question_id    = Column(Integer, ForeignKey('redpack_user_question.id'))
    order_no            = db.Column(String(30), unique=True)
    transaction_id      = db.Column(String(100))
    price               = Column(MoneyField) #需支付价格
    status              = Column(TINYINT(1), nullable=False, default=0) #0新下单 1支付中 2支付成功
    create_time         = Column(DateTime, default=dt_obj.now)

    def as_dict(self):
        return dict(
            id          = self.id,
            order_no    = self.order_no,
            qr_user_id  = self.qr_user_id,
            transaction_id   = self.transaction_id,
            user_question_id = self.user_question_id,
            price            = format_price(self.price),
            status           = self.status,
            create_time      = self.create_time
            )


class RedpackPayUser(Model):
    ''' 问题查看用户'''
    id                  = Column(Integer, primary_key=True)
    qr_user_id          = Column(Integer, ForeignKey('qr_code_user.id'))
    price               = Column(MoneyField) #需支付价格
    user_question_id    = Column(Integer, ForeignKey('redpack_user_question.id'))
    pay_id              = Column(Integer, ForeignKey('redpack_pay.id'))
    create_time         = Column(DateTime, default=dt_obj.now)

    def as_dict(self):
        return dict(
            id          = self.id,
            qr_user_id  = self.qr_user_id,
            price       = format_price(self.price),
            pay_id      = self.pay_id,
            user_question_id = self.user_question_id,
            create_time      = self.create_time,
            )


class UserDevice(Model):
    ''' 用户设备 '''
    id                  = Column(Integer, primary_key=True)
    user_id             = Column(Integer, ForeignKey('user.id'), nullable=True)
    device_id           = db.Column(String(50), unique=True)
    push_token          = db.Column(String(50))
    os_version          = db.Column(String(10))
    app_version         = db.Column(String(10))
    device_name         = db.Column(String(100))
    cat                 = Column(TINYINT(1), nullable=False, default=0) #1ios 2android
    create_time         = Column(DateTime, default=dt_obj.now)
    update_time         = Column(DateTime, default=dt_obj.now)

    def as_dict(self):
        ''' '''
        return dict(
            id          = self.id,
            user_id     = self.user_id,
            device_id   = self.device_id,
            push_token  = self.push_token,
            os_version  = self.os_version,
            app_version = self.app_version,
            device_name = self.device_name,
            cat         = self.cat,
            create_time = self.create_time,
            update_time = self.update_time
            )


class UserDeviceLog(Model):
    ''' 用户历史设备表 '''
    id                  = Column(Integer, primary_key=True)
    user_id             = Column(Integer, ForeignKey('user.id'), nullable=False)
    device_id           = db.Column(String(50), index=True)
    create_time         = Column(DateTime, default=dt_obj.now)

    def as_dict(self):
        ''' '''
        return dict(
            id          = self.id,
            user_id     = self.user_id,
            device_id   = self.device_id,
            create_time = self.create_time
            )


class RdUserQrcode(Model):
    ''' 现金用户分享二维码 '''
    __table_args__  = (
        UniqueConstraint('user_id', 'qrcode_id'),
    )
    id                 = db.Column(Integer, primary_key=True)
    user_id            = Column(Integer, ForeignKey('user.id'))
    qrcode_id          = Column(Integer, ForeignKey('qrcode.id'))
    follow_count       = Column(Integer, default=0)
    reg_count          = Column(Integer, default=0)
    create_time        = Column(DateTime, default=dt_obj.now)

    def as_dict(self):
        return dict(
            id          = self.id,
            qrcode_id   = self.qrcode_id,
            user_id     = self.user_id,
            follow_count= self.follow_count,
            reg_count   = self.reg_count,
            create_time = str(self.create_time)
            )


class RdQrcodeUser(Model):
    ''' 二维码注册用户 '''
    id                 = db.Column(Integer, primary_key=True)
    user_id            = Column(Integer, ForeignKey('user.id'))
    qrcode_id          = Column(Integer, ForeignKey('qrcode.id'))
    create_time        = Column(DateTime, default=dt_obj.now)

    def as_dict(self):
        return dict(
            id          = self.id,
            qrcode_id   = self.qrcode_id,
            user_id     = self.user_id,
            create_time = str(self.create_time)
            )


class RdMoneyPrize(Model):
    ''' 现金奖励金额 '''

    id                 = db.Column(Integer, primary_key=True)
    amount             = Column(Integer, default=0)
    sent               = Column(Integer, default=0)
    total              = Column(Integer, default=0)
    create_time        = Column(DateTime, default=dt_obj.now)

    def as_dict(self):
        return dict(
            id          = self.id,
            amount      = self.amount,
            sent        = self.sent,
            total       = self.total
            )



class RdDrawCounter(Model):
    ''' 现金奖励抽奖计数 '''

    id                 = db.Column(Integer, primary_key=True)
    user_id            = Column(Integer, ForeignKey('user.id'))
    used               = Column(Integer, default=0)
    total              = Column(Integer, default=0)
    create_time        = Column(DateTime, default=dt_obj.now)

    def as_dict(self):
        return dict(
            id          = self.id,
            user_id     = self.user_id,
            used        = self.used,
            total       = self.total
            )


class RdDrawCounterLog(Model):
    ''' 现金奖励抽奖机会变更历史 '''

    id                 = db.Column(Integer, primary_key=True)
    user_id            = Column(Integer, ForeignKey('user.id'))
    count              = Column(Integer, default=0)
    source             = Column(TINYINT(1), nullable=False, default=1) #1额度申请 2邀请 3完成订单
    create_time        = Column(DateTime, default=dt_obj.now)

    def as_dict(self):
        return dict(
            id          = self.id,
            user_id     = self.user_id,
            count       = self.count,
            source      = self.source
            )

















