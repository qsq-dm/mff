# -*- coding: utf-8 -*-
from collections        import defaultdict

from sqlalchemy         import func
from sqlalchemy         import and_
from sqlalchemy.sql     import exists
from models             import db
from models             import Item
from models             import Hospital
from models             import ItemCat
from models             import ItemSubCat
from models             import RecommendItem
from models             import RecommendSubcat
from models             import RecommendHospital
from models             import ItemFav
from models             import Activity
from models             import ActivityItem
from util.utils         import dt_obj
from util.utils         import format_price
from util.sqlerr        import SQL_DUPLICATE_NAME
from ops.utils          import get_page
from ops.utils          import get_items
from ops.utils          import count_items


class ItemService(object):

    @staticmethod
    def create_item(title, hospital_id, sub_cat_id, sub_cat_ids, price, orig_price, \
             item_no, support_choices, photos, surgery_desc, doctor_desc, image, has_fee, direct_buy, \
             use_time, note):
        ''' 创建商品 '''
        item    = Item(
            title=title,
            item_no=item_no,
            hospital_id=hospital_id,
            sub_cat_id=sub_cat_id,
            price=price,
            orig_price=orig_price,
            support_choices=support_choices,
            photos=photos,
            doctor_desc=doctor_desc,
            image=image,
            surgery_desc=surgery_desc,
            direct_buy=direct_buy,
            has_fee=has_fee,
            use_time=use_time,
            note=note
            )
        db.session.add(item)
        db.session.commit()
        return item.id

    @staticmethod
    def update_item(item_id, **kw):
        count       = Item.query.filter(Item.id==item_id).update(kw)
        db.session.commit()
        return count

    @staticmethod
    def offline_item(item_id):
        ActivityItem.query.filter(ActivityItem.item_id==item_id).delete()
        RecommendItem.query.filter(RecommendItem.item_id==item_id).delete()
        db.session.commit()

    @staticmethod
    def offline_subcat(subcat_id):
        RecommendSubcat.query.filter(RecommendSubcat.sub_cat_id==subcat_id).delete()
        db.session.commit()

    @staticmethod
    def set_hospital_status(hospital_id, status):
        count   = Hospital.query.filter(Hospital.id==hospital_id).update({'status':status})
        db.session.commit()
        return count
    @staticmethod
    def set_hospital_item_status(where, item_status):
        count   = Item.query.filter(where).update({'status':item_status})
        db.session.commit()

    @staticmethod
    def update_hospital(item_id, **kw):
        count       = Hospital.query.filter(Hospital.id==item_id).update(kw)
        db.session.commit()
        return count

    @staticmethod
    def create_hospital(**kw):
        hospital = Hospital(**kw)
        db.session.add(hospital)
        db.session.commit()
        return hospital.id

    @staticmethod
    def create_cat(name):
        try:
            cat     = ItemCat(name=name)
            db.session.add(cat)
            db.session.commit()
            return cat.id
        except Exception as e:
            db.session.rollback()
            if SQL_DUPLICATE_NAME.search(str(e)):
                assert 0, '分类名已存在'

    @staticmethod
    def update_cat(cat_id, **kw):
        count   = ItemCat.query.filter(ItemCat.id==cat_id).update(kw)
        db.session.commit()
        return count

    @staticmethod
    def update_subcat(sub_cat_id, **kw):
        count   = ItemSubCat.query.filter(ItemSubCat.id==sub_cat_id).update(kw)
        db.session.commit()
        return count

    @staticmethod
    def create_sub_cat(cat_id, name, icon, desc, cat_ids):
        try:
            sub_cat = ItemSubCat(name=name, cat_id=cat_id, cat_ids=cat_ids, icon=icon, desc=desc)
            db.session.add(sub_cat)
            db.session.commit()
            return sub_cat.id
        except Exception as e:
            db.session.rollback()
            if SQL_DUPLICATE_NAME.search(str(e)):
                assert 0, '小类名已存在'

    @staticmethod
    def get_the_paged_items(**kw):
        return get_page(Item, {}, **kw)

    @staticmethod
    def get_paged_items(**kw):

        current_time    = dt_obj.now()
        query           = and_(
            Activity.start_time<current_time,
            Activity.end_time>=current_time
            )
        activity = Activity.query.filter(query).first()
        activity_id = None
        if activity:
            activity_id = activity.id
        join     = None#ActivityItem.activity_id==activity_id
        has_more, items, extras = get_page(Item, {}, extra=ActivityItem, **kw)
        item_activity_price_map = {i.item_id:float(i.price) for i in extras}
        for i in items:
            if item_activity_price_map.get(i['id']):
                #i['old_price'] = i['price']
                i['price'] = int(item_activity_price_map.get(i['id']))
        return has_more, items

    @staticmethod
    def get_item_cats():
        return ItemCat.query.order_by(ItemCat.sort_order.asc()).all()

    @staticmethod
    def get_item_subcats(**kw):
        condition   = {}
        where       = ItemSubCat.status==1
        kw.setdefault('where', where)
        kw.setdefault('no_limit', True)
        kw.setdefault('fields', ['id', 'name', 'icon', 'cat_id', 'cat_id_list'])
        has_more, infos = get_page(ItemSubCat, condition, **kw)
        return infos

    @staticmethod
    def get_item_dict_by_id(item_id, fields=None):
        ''' '''
        item = Item.query.filter(Item.id==item_id).first()
        if item:
            item_dict = item.as_dict()
            if fields:
                for k, v in item_dict.items():
                    if k not in fields: item_dict.pop(k, '')
            return item_dict

    @staticmethod
    def get_cat_dict_by_id(cat_id, fields=None):
        ''' '''
        item = ItemCat.query.filter(ItemCat.id==cat_id).first()
        if item:
            item_dict = item.as_dict()
            if fields:
                for k, v in item_dict.items():
                    if k not in fields: item_dict.pop(k, '')
            return item_dict

    @staticmethod
    def get_subcat_dict_by_id(sub_cat_id, fields=None):
        ''' '''
        item = ItemSubCat.query.filter(ItemSubCat.id==sub_cat_id).first()
        if item:
            item_dict = item.as_dict()
            if fields:
                for k, v in item_dict.items():
                    if k not in fields: item_dict.pop(k, '')
            return item_dict

    @staticmethod
    def get_item_cat_choices():
        items       = ItemCat.query.all()
        sub_items   = ItemSubCat.query.all()
        result      = []
        for cat in items:
            name    = cat.name
            cat_id  = cat.id
            cat_subs= [i for i in sub_items if i.cat_id==cat_id]
            tmp     = {
                'id'    : cat_id,
                'name'  : name,
                'sub_cats': [{'id':i.id, 'name':i.name} for i in cat_subs]
                }
            result.append(tmp)
        return result

    @staticmethod
    def fav_item(user_id, item_id):
        ''' 添加商品到心愿单 '''
        try:
            fav         = ItemFav(user_id=user_id, item_id=item_id)
            db.session.add(fav)
            db.session.commit()
            return fav.id
        except Exception as e:
            db.session.rollback()

    @staticmethod
    def unfav_item(user_id, item_id):
        ''' 从心愿单移除商品 '''
        query        = and_(
            ItemFav.user_id==user_id,
            ItemFav.item_id==item_id
            )
        count        = ItemFav.query.filter(query).delete()
        db.session.commit()
        return count

    @staticmethod
    def has_fav(item_id, user_id):
        query        = and_(
            ItemFav.user_id==user_id,
            ItemFav.item_id==item_id
            )
        return ItemFav.query.filter(query).first()

    @staticmethod
    def get_paged_cats(**kw):
        return get_page(ItemCat, {}, **kw)

    @staticmethod
    def get_paged_sub_cats(**kw):
        return get_page(ItemSubCat, {}, **kw)

    @staticmethod
    def get_paged_hospitals(**kw):
        return get_page(Hospital, {}, **kw)

    @staticmethod
    def get_paged_fav_items(**kw):
        return get_page(ItemFav, {}, **kw)

    @staticmethod
    def get_items_by_ids(item_ids, **kw):
        return get_items(Item, item_ids, **kw)

    @staticmethod
    def get_hospitals_by_ids(item_ids, **kw):
        return get_items(Hospital, item_ids, **kw)

    @staticmethod
    def get_cats_by_ids(item_ids, **kw):
        return get_items(ItemCat, item_ids, **kw)

    @staticmethod
    def get_subcats_by_ids(item_ids, **kw):
        return get_items(ItemSubCat, item_ids, **kw)

    @staticmethod
    def get_hospital_dict_by_id(hospital_id, **kw):
        items    = get_items(Hospital, (hospital_id, ), **kw)
        if items: return items[0]

    @staticmethod
    def count_items(where=None):
        query           = db.session.query(func.count(Item.id))
        if where is not None: query     = query.filter(where)
        return query.scalar()

    @staticmethod
    def count_hospitals(where=None):
        return count_items(Hospital, where=where)

    @staticmethod
    def set_subcat_status(subcat_id, status):
        count       = ItemSubCat.query.filter(ItemSubCat.id==subcat_id).update({'status':status})
        db.session.commit()
        return count

    @staticmethod
    def count_sub_cat_items(hospital_id=None):
        return db.session.query(Item.sub_cat_id, func.count(Item.id)).filter(Item.hospital_id==hospital_id).group_by(Item.sub_cat_id).all()

    @staticmethod
    def add_recommend_item(item_id, sort_order, image, desc):
        recommend   = RecommendItem(item_id=item_id, sort_order=sort_order, image=image, desc=desc)
        db.session.add(recommend)
        db.session.commit()

    @staticmethod
    def update_recommend_item(item_id, **kw):
        count       = RecommendItem.query.filter(RecommendItem.item_id==item_id).update(kw)
        db.session.commit()
        return count

    @staticmethod
    def rm_recommend_item(item_id):
        count       = RecommendItem.query.filter(RecommendItem.item_id==item_id).delete()
        db.session.commit()
        return count
    @staticmethod
    def rm_recommend_hospital(item_id):
        count       = RecommendHospital.query.filter(RecommendHospital.hospital_id==item_id).delete()
        db.session.commit()
        return count

    @staticmethod
    def exists_recommend_item_ids(item_ids):
        rows    = db.session.query(RecommendItem).filter(RecommendItem.item_id.in_(item_ids)).all()
        return {i.item_id:i.sort_order for i in rows}
    @staticmethod
    def exists_recommend_hospital_ids(item_ids):
        rows    = db.session.query(RecommendHospital).filter(RecommendHospital.hospital_id.in_(item_ids)).all()
        return {i.hospital_id:i.sort_order for i in rows}

    @staticmethod
    def exists_recommend_subcat_map(subcat_ids):
        rows    = db.session.query(RecommendSubcat).filter(RecommendSubcat.sub_cat_id.in_(subcat_ids)).all()
        return {i.sub_cat_id:i.sort_order for i in rows}

    @staticmethod
    def top_recommend_item(item_id):
        ''' 推荐置顶 '''
        item    = RecommendItem.query.filter(RecommendItem.item_id==item_id).first()
        if not item: return

        query   = and_(
            RecommendItem.item_id!=item_id,
            RecommendItem.sort_order<=item.sort_order
            )
        count   = RecommendItem.query.filter(query) \
            .update({'sort_order':RecommendItem.sort_order+1})
        RecommendItem.query.filter(RecommendItem.item_id==item_id).update({'sort_order':0})
        db.session.commit()
        return count

    @staticmethod
    def top_recommend_subcat(sub_cat_id):
        ''' 推荐子分类置顶 '''
        item    = RecommendSubcat.query.filter(RecommendSubcat.sub_cat_id==sub_cat_id).first()
        if not item: return

        query   = and_(
            RecommendSubcat.sub_cat_id!=sub_cat_id,
            RecommendSubcat.sort_order<=item.sort_order
            )
        count   = RecommendSubcat.query.filter(query) \
            .update({'sort_order':RecommendSubcat.sort_order+1})
        RecommendSubcat.query.filter(RecommendSubcat.sub_cat_id==sub_cat_id).update({'sort_order':0})
        db.session.commit()
        return count

    @staticmethod
    def exists_recommend_subcat_ids(subcat_ids):
        rows    = db.session.query(RecommendSubcat.sub_cat_id).filter(RecommendSubcat.sub_cat_id.in_(subcat_ids)).all()
        return [i.item_id for i in rows]


    @staticmethod
    def add_recommend_subcat(sub_cat_id, sort_order, icon):
        recommend   = RecommendSubcat(sub_cat_id=sub_cat_id, sort_order=sort_order, icon=icon)
        db.session.add(recommend)
        db.session.commit()

    @staticmethod
    def update_recommend_subcat(sub_cat_id, **kw):
        count       = RecommendSubcat.query.filter(RecommendSubcat.sub_cat_id==sub_cat_id).update(kw)
        db.session.commit()
        return count

    @staticmethod
    def add_recommend_hospital(hospital_id, sort_order, color, tag):
        recommend   = RecommendHospital(hospital_id=hospital_id, sort_order=sort_order, color=color, tag=tag)
        db.session.add(recommend)
        db.session.commit()
    @staticmethod
    def update_recommend_hospital(hospital_id, **kw):
        count       = RecommendHospital.query.filter(RecommendHospital.hospital_id==hospital_id).update(kw)
        db.session.commit()
        return count

    @staticmethod
    def rm_recommend_subcat(sub_cat_id):
        count       = RecommendSubcat.query.filter(RecommendSubcat.sub_cat_id==sub_cat_id).delete()
        db.session.commit()
        return count

    @staticmethod
    def get_item_recommend(item_id):
        recommend  = RecommendItem.query.filter(RecommendItem.item_id==item_id).first()
        if recommend: return recommend.as_dict()

    @staticmethod
    def get_subcat_recommend(sub_cat_id):
        recommend  = RecommendSubcat.query.filter(RecommendSubcat.sub_cat_id==sub_cat_id).first()
        if recommend: return recommend.as_dict()

    @staticmethod
    def get_hospital_recommend(hospital_id):
        recommend  = RecommendHospital.query.filter(RecommendHospital.hospital_id==hospital_id).first()
        if recommend: return recommend.as_dict()

    @staticmethod
    def get_item_activity(item_id, activity_id=None):
        query       = and_()
        query.append(ActivityItem.item_id==item_id)
        if activity_id: query.append(ActivityItem.activity_id==activity_id)
        activity    = ActivityItem.query.filter(query).first()
        if activity: return activity.as_dict()

    @staticmethod
    def add_activity_item(item_id, sort_order, activity_id, price, image):
        activity    = ActivityItem(item_id=item_id, sort_order=sort_order, activity_id=activity_id, price=price, image=image)
        db.session.add(activity)
        db.session.commit()

    @staticmethod
    def update_activity_item(item_id, **kw):
        count       = ActivityItem.query.filter(ActivityItem.item_id==item_id).update(kw)
        db.session.commit()
        return count

    @staticmethod
    def get_paged_recommend_subcats(**kw):
        return get_page(RecommendSubcat, **kw)

    @staticmethod
    def get_paged_recommend_hospitals(**kw):
        return get_page(RecommendHospital, **kw)

    @staticmethod
    def get_paged_activity_items(**kw):
        return get_page(ActivityItem, **kw)

    @staticmethod
    def get_paged_recommend_items(**kw):
        return get_page(RecommendItem, **kw)

    @staticmethod
    def check_exist_order(sort_order):
        query   = and_(
            RecommendItem.sort_order==sort_order
            )
        return db.session.query(RecommendItem).filter(query).first()

    @staticmethod
    def check_exist_subcat_order(sort_order):
        query   = and_(
            RecommendSubcat.sort_order==sort_order
            )
        return db.session.query(RecommendSubcat).filter(query).first()

    @staticmethod
    def check_exist_hospital_order(sort_order):
        query   = and_(
            RecommendHospital.sort_order==sort_order
            )
        return db.session.query(RecommendHospital).filter(query).first()

    @staticmethod
    def incr_item_count(item_id, amount=1):
        ''' 商品已售数加1 医院已售数加1 '''
        item    = Item.query.filter(Item.id==item_id).first()
        count   = Item.query.filter(Item.id==item_id).update({'sold_count':Item.sold_count+amount}, synchronize_session=False)
        if item:
            Hospital.query.filter(Hospital.id==item.hospital_id).update({'sold_count':Hospital.sold_count+amount}, synchronize_session=False)
        db.session.commit()

    @staticmethod
    def get_activity_items_by_item_ids(item_ids):
        return ActivityItem.query.filter(ActivityItem.item_id.in_(item_ids)).all()

    @staticmethod
    def count_hospital_items(hospital_ids):
        ''' 医院商品计数 '''
        query   = and_(
            Item.status==1,
            Item.hospital_id.in_(hospital_ids)
            )
        result  = db.session.query(
                Item.hospital_id,func.count(Item.id)).filter(query).group_by(Item.hospital_id).all()
        return dict(result)

    @staticmethod
    def get_hospital_item_cats(hospital_ids):
        rows    = db.session.query(
            Item.sub_cat_ids, Item.hospital_id
            ).filter(Item.hospital_id.in_(hospital_ids)).all()
        data    = defaultdict(set)
        for row in rows:
            sub_cat_ids, hospital_id     = row
            sub_cat_id_list              = map(int, sub_cat_ids.split(','))
            for i in sub_cat_id_list: data[hospital_id].add(i)
        return data

    @staticmethod
    def get_sub_cat_id_name(sub_cat_ids, all_sub_cats=None, all_cats=None):
        ''' 子分类id列表对应分类列表 '''
        sub_cats    = filter(lambda i:i['id'] in sub_cat_ids, all_sub_cats)
        cat_ids     = [i['cat_id'] for i in sub_cats]
        cats        = filter(lambda i:i['id'] in cat_ids, all_cats)
        return cats

    @staticmethod
    def set_item_cat_order(cat_id, sort_order):
        count       = ItemCat.query.filter(ItemCat.id==cat_id).update(
            {'sort_order':sort_order},
            synchronize_session=False
            )
        db.session.commit()

    @staticmethod
    def get_activity_prices(item_ids, activity_id=None):
        ''' '''
        query   = and_(
            ActivityItem.item_id.in_(item_ids),
            ActivityItem.activity_id==activity_id
            )
        items   = ActivityItem.query.filter(query).all()
        price_map   = {i.item_id:format_price(i.price) for i in items}
        return price_map


        




