# -*- coding: utf-8 -*-
__author__ = 'shn7798'

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.cache import Cache

__all__ = ['db', 'cache']

db = SQLAlchemy()
cache = Cache()

