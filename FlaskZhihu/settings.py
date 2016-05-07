# -*- coding: utf-8 -*-
__author__ = 'shn7798'

class DefaultSettings(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql://flaskzhihu:123456@192.168.5.202/flaskzhihu?charset=UTF-8"
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = "asasasasas"


class TestSettings(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql://flaskzhihu:123456@192.168.5.202/flaskzhihu_test?charset=utf8"
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    WTF_CSRF_ENABLED = False
    SECRET_KEY = "asasasasas"
    CACHE_TYPE = "simple"
    CACHE_DEFAULT_TIMEOUT = 60
    SQLALCHEMY_RECORD_QUERIES = True


class IPythonSettings(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql://flaskzhihu:123456@192.168.5.202/flaskzhihu_test?charset=utf8"
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    WTF_CSRF_ENABLED = False
    SECRET_KEY = "asasasasas"
    CACHE_TYPE = "simple"
    CACHE_DEFAULT_TIMEOUT = 600
    SQLALCHEMY_RECORD_QUERIES = True

class RedisCacheSettings(TestSettings):
    CACHE_TYPE = 'redis'

    CACHE_REDIS_HOST = '192.168.5.202'
    CACHE_KEY_PREFIX = 'flask_'

    DOGPILE_CACHE_REGIONS = [
        ('hour', 3600),
        ('day', 3600 * 24),
        ('month', 3600 * 24 * 31),
    ]
    DOGPILE_CACHE_URLS = [ '' ]
    DOGPILE_CACHE_BACKEND = 'dogpile.cache.redis'
    DOGPILE_CACHE_ARGUMENTS = {
        'url': None,
        #'host': '192.168.5.202',
        'host': '127.0.0.1',
        'port': 6379,
        'db': 1,
        'redis_expiration_time': 60 * 2, # seconds
        'distributed_lock': True
    }
