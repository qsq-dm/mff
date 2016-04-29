# -*- coding: utf-8 -*-
from functools  import wraps

from sqlalchemy import func
from util.utils import keep_fields_from_list
from models     import db


def get_page(model, condition=None, offset=None, \
             limit=10, fields=None, \
             start=None, end=None, where=None, \
             join=None, order_by=None, \
             extra=None, order_by_case=None, \
             _sort='id', _sort_dir='DESC', no_limit=False):
    if extra:
        query = db.session.query(model,extra).outerjoin(extra)
    else:
        query = db.session.query(model)
    if join is not None: query = query.join(join)
    if order_by is not None:
        if isinstance(order_by, (tuple,list)):
            query = query.order_by(*order_by)
        else:
            query = query.order_by(order_by)
    elif _sort and _sort!='id' and getattr(model, _sort, None): #order by 第一个column为主排序column
        if _sort_dir=='ASC': order_by  = getattr(model, _sort).asc()
        if _sort_dir=='DESC': order_by = getattr(model, _sort).desc()
        if order_by_case is None: query = query.order_by(order_by)
        if order_by_case is None: query = query.order_by(model.id.desc())
    else:
        query = query.order_by(model.id.asc()) if _sort_dir=='ASC' else query.order_by(model.id.desc())
    if condition: query = query.filter_by(**condition)
    if where is not None: query = query.filter(where)
    if offset: query = query.filter(getattr(model, _sort)< offset) if _sort_dir=='DESC' else query.filter(getattr(model, _sort) > offset)
    if start:query = query.offset(start)
    if end:  query = query.limit(end-start)
    items = []

    if order_by_case is not None:
        query = query.order_by(order_by_case)
    data = query.limit(limit+1).all() if not (start or end or no_limit) else query.all()
    extras = None
    if extra is not None:
        extras = [i[1] for i in data if i[1]]
        data   = [i[0] for i in data]
    items[:] = tuple(row.as_dict() for row in (data if no_limit else data[:limit]))
    is_more = len(data)>limit

    if fields: keep_fields_from_list(items, fields)
    if extra:
        return is_more, items, extras
    return is_more, items


def get_items(model, ids=None, fields=None, all=False):
    query = model.query

    if getattr(model, 'status', None) and not(all):
        query = query.filter(model.show_status())
    data    = []
    if not ids: return data
    data[:] = query.filter(model.id.in_(ids)).all()
    data[:] = tuple(i.as_dict() for i in data)
    if fields: keep_fields_from_list(data, fields)
    return data


def get_fields_column(model, fields):
    return tuple(getattr(model, field) for field in fields)


def count_items(model, where=None, field='id'):
    query   = db.session.query(func.count(getattr(model, field)))
    if where is not None: query = query.filter(where)

    return query.scalar()



