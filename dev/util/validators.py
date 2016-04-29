# -*- coding: utf-8 -*-
import re
import json
import urllib2

from util.utils import union_dict



phoneprefix       = [
    '130','131','132','133','134','135','136','137','138','139',
    '150','151','152','153','154','155','156','157','158','159',
    '170','171','172','173','174','175','176','177','178','179',
    '180','181','182','183','184','185','186','187','188','189'
    ]
phone_prefix_pattern = re.compile('^(%s)\d{8}$' % '|'.join(phoneprefix))
fake_phone           = re.compile(r'1000000(\d){4}')
def valid_phone(phone):
    return (bool(phone_prefix_pattern.search(phone)) or bool(fake_phone.search(phone))) and phone



def Optional(field):
    field.optional = True
    return field


class Field(object):
    ''' '''
    def __init__(self, msg=None, **kw):
        self.optional  = False
        self.msg       = msg

    def validate(self, data):
        is_valid    = False
        result      = '请实现此方法'
        return is_valid, result


class TextField(Field):

    def __init__(self, min_length=None, max_length=None, **kw):
        super(TextField, self).__init__(**kw)
        self.min_length = min_length;
        self.max_length = max_length

    def validate(self, data):
        is_valid    = isinstance(data, (str, unicode)) and \
            (self.min_length<=len(data) if self.min_length is not None else True) and \
            (self.max_length>=len(data) if self.max_length is not None else True)
        result      = data
        return is_valid, result


class IntChoiceField(Field):

    def __init__(self, choices=None, **kw):
        super(IntChoiceField, self).__init__(**kw)
        self.choices = choices or set()

    def validate(self, data):
        is_valid    = str(str(data) or '').isdigit() and \
               int(data) in self.choices
        result      = int(data) if is_valid else None
        return is_valid, result


class BoolChoiceField(Field):

    def __init__(self, choices=None, **kw):
        super(BoolChoiceField, self).__init__(**kw)
        self.choices = choices or set()

    def validate(self, data):
        is_valid    = True
        result      = bool(data)
        return is_valid, result


class BoolIntChoiceField(Field):

    def __init__(self, **kw):
        super(BoolIntChoiceField, self).__init__(**kw)

    def validate(self, data):
        is_valid      = True
        try:
            data      = bool(int(data))
        except:
            is_valid  = False
        return is_valid, data



class ChoiceField(Field):

    def __init__(self, choices=None, **kw):
        super(ChoiceField, self).__init__(**kw)
        self.choices = choices or set()

    def validate(self, data):
        result          = None
        is_valid        = False
        try:
            if data in self.choices:
                is_valid    = True
                result      = data
        except Exception as e:
            print str(e)

        return is_valid, result


class IntChoicesField(Field):

    def __init__(self, choices=None, all=False, **kw):
        super(IntChoicesField, self).__init__(**kw)
        self.choices = choices or set()

    def validate(self, data):
        result          = None
        is_valid        = False
        try:
            result      = map(int, data)
            if not all:
                is_valid    = all(int(i) in self.choices for i in result) if self.choices else False
            else:
                is_valid    = True
        except Exception as e:
            print str(e)

        return is_valid, result


class MobileField(Field):

    def validate(self, data):
        is_valid    = valid_phone(data)
        result      = data
        return is_valid, result


class FloatField(Field):

    def validate(self, data):
        is_valid        = False
        result          = None
        try:
            result      = float(data)
            is_valid    = True
        except Exception as e:
            pass
        return is_valid, result


class IntField(Field):

    def validate(self, data):
        is_valid        = False
        result          = None
        try:
            result      = int(data)
            is_valid    = True
        except Exception as e:
            pass
        return is_valid, result


class JsonField(Field):

    def validate(self, data):
        is_valid        = False
        result          = None
        try:
            result      = json.loads(urllib2.unquote(data)) if data else []
            is_valid    = True
        except Exception as e:
            pass
        return is_valid, result



class IdField(Field):
    ''' 数据库ID字段 '''
    def validate(self, data):
        is_valid    = str(str(data) or '').isdigit()
        result      = int(data) if is_valid else None
        return is_valid, result


class REGField(Field):
    def __init__(self, pattern=None, **kw):
        self.pattern     = pattern
        super(REGField, self).__init__(**kw)

    def validate(self, value):
        try:
            valid = False
            p     = re.compile(self.pattern)
            self.p = p
            valid = bool(p.search(str(value)))
        except:
            import traceback
            traceback.print_exc()
            return valid, value
        else:
            return valid, value


NOT_EXIST    = object()
class Inputs(object):

    def __init__(self, schema):
        self._schema    = schema

    def validate(self, raw_data):
        self._raw_data  = raw_data

        result           = {}
        self._fields_err = {}
        for name, validator in self._schema.items():
            print name; print validator
            val          = self._raw_data.get(name, NOT_EXIST)
            data         = None
            err          = ''
            print  val is NOT_EXIST, val, validator.optional, 'optional'
            if val is NOT_EXIST:
                if not validator.optional:
                    err = '缺少字段{}'.format(name)
            else:
                is_valid, data = validator.validate(val)
                if not is_valid: err = validator.msg or '{}字段格式错误'.format(name)
            if err: self._fields_err[name] = err
            result[name] = data

        err_str  = '\n'.join(self._fields_err.values()) 
        return err_str, result










