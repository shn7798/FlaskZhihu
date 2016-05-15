# -*- coding: utf-8 -*-
__author__ = 'shn7798'

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.cache import Cache
from flask.ext.session import Session

__all__ = ['db', 'cache', 'session']

db = SQLAlchemy()
cache = Cache()
session = Session()
