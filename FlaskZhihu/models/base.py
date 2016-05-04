# -*- coding: utf-8 -*-
__author__ = 'shn7798'

from FlaskZhihu.extensions import db
import datetime

class DateTimeMixin(object):
    create_time = db.Column('create_time', db.DateTime, default=datetime.datetime.now)
    update_time = db.Column('update_time', db.DateTime,
                            default=datetime.datetime.now,
                            onupdate=datetime.datetime.now)