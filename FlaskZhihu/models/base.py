# -*- coding: utf-8 -*-
__author__ = 'shn7798'

from FlaskZhihu.extensions import db
import datetime

class FindByIdMixin():
    @classmethod
    def find_by_id(cls, id, abort404=False, pk='id'):
        pk_col = getattr(cls, pk)
        query = cls.query.filter(pk_col==id)
        if abort404:
            return query.first_or_404()
        else:
            return query.first()

class DateTimeMixin():
    create_time = db.Column('create_time', db.DateTime, default=datetime.datetime.now)
    update_time = db.Column('update_time', db.DateTime,
                            default=datetime.datetime.now,
                            onupdate=datetime.datetime.now)


def try_decode(s, enc_list=['UTF-8', 'GBK']):
    for enc in enc_list:
        try:
            v = s.decode(enc)
        except:
            pass
        else:
            return v
    return s

def try_encode(s, enc_list=['UTF-8', 'GBK']):
    for enc in enc_list:
        try:
            v = s.encode(enc)
        except:
            pass
        else:
            return v
    return s

def blob_unicode(key_name):
    def _set_blob(self, val):
        if isinstance(val, unicode):
            val = try_encode(val)
        setattr(self, key_name, val)


    def _get_blob(self):
        val = getattr(self, key_name, None)
        if val is None:
            return val

        if isinstance(val, unicode):
            return val
        else:
            return try_decode(val)

    return db.synonym(key_name, descriptor=property(_get_blob, _set_blob))
