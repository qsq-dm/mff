# -*- coding: utf-8 -*-

import requests

from util.sqlerr    import SQL_DUPLICATE_NAME

from models         import db
from models         import School
from models         import City
from models         import HelpCat
from models         import HelpEntry
from models         import ImageSize
from ops.utils      import get_items
from ops.utils      import get_page
from ops.utils      import count_items
from util.utils     import prefix_img_domain
from settings       import celery


class DataService(object):

    @staticmethod
    def create_school(name, link, city_name):
        try:
            school  = School(name=name, link=link, city_name=city_name)
            db.session.add(school)
            db.session.commit()
            return school.id
        except Exception as e:
            db.session.rollback()
            import traceback
            traceback.print_exc()

    @staticmethod
    def get_paged_schools(**kw):
        return get_page(School, {}, **kw)

    @staticmethod
    def get_schools():
        return School.query.all()

    @staticmethod
    def get_paged_cities(**kw):
        return get_page(City, {}, **kw)

    @staticmethod
    def create_city(name, city_code, amap_code):
        city    = City(name=name, amap_code=amap_code, city_code=city_code)
        db.session.add(city)
        db.session.commit()
        return city.id

    @staticmethod
    def update_city(city_id, **kw):
        count    = City.query.filter(City.id==city_id).update(kw)
        db.session.commit()
        return count

    @staticmethod
    def get_city_by_baidu_city_code(city_code):
        return City.query.filter(City.city_code==city_code).first()

    @staticmethod
    def count_schools(where=None):
        return count_items(School, where)

    @staticmethod
    def get_school_city_names():
        rows = db.session.query(School.city_name).distinct().all()
        return [i.city_name for i in rows]

    @staticmethod
    def create_help_cat(id, name):
        try:
            cat  = HelpCat(id=id, name=name)
            db.session.add(cat)
            db.session.commit()
            return cat.id
        except Exception as e:
            db.session.rollback()
            if SQL_DUPLICATE_NAME.search(str(e)):
                print 'duplicate entry name'

    @staticmethod
    def create_help_entry(cat_id, title, content):
        entry   = HelpEntry(cat_id=cat_id, title=title, content=content)
        db.session.add(entry)
        db.session.commit()

    @staticmethod
    def get_paged_helpcats(**kw):
        _sort_dir   = 'ASC'
        return get_page(HelpCat, {}, limit=1000, _sort_dir=_sort_dir, **kw)

    @staticmethod
    def get_paged_helpentries(**kw):
        _sort_dir   = 'ASC'
        return get_page(HelpEntry, {}, limit=1000, _sort_dir=_sort_dir, **kw)

    @staticmethod
    def get_helpentry_by_id(entry_id):
        entry   = HelpEntry.query.filter(HelpEntry.id==entry_id).first()
        if entry: return entry.as_dict()

    @staticmethod
    def get_paged_city_list(**kw):
        return get_page(City, {}, **kw)

    @staticmethod
    def get_city_dict_by_id(city_id):
        city    = City.query.filter(City.id==city_id).first()
        if city: return city.as_dict()

    @staticmethod
    @celery.task
    def set_img_size(key):
        ''' 设置图片宽高 '''
        full_url = prefix_img_domain(key)
        print full_url
        result   = requests.get('{}?imageInfo'.format(full_url))
        if result.status_code!=200:
            assert 0, '图片不存在'
        data     = result.json()
        width    = data['width']
        height   = data['height']
        try:
            img  = ImageSize(key=key, width=width, height=height)
            db.session.add(img)
            db.session.commit()
        except Exception as e:
            import traceback
            traceback.print_exc()
            db.session.rollback()

    @staticmethod
    def get_imgs_size_by_keys(keys):
        if isinstance(keys, (tuple, list)):
            query   = ImageSize.key.in_(keys)
        else:
            query   = ImageSize.key==keys
        sizes   = ImageSize.query.filter(query).all()
        return [ i.as_dict() for i in sizes]

