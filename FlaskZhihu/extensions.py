# -*- coding: utf-8 -*-
__author__ = 'shn7798'

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.cache import Cache
from flask.ext.dogpile_cache import DogpileCache

__all__ = ['db', 'cache', 'dogpile']

db = SQLAlchemy()
#cache = Cache()
dogpile = DogpileCache()
cache = dogpile
