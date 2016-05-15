# -*- coding: utf-8 -*-
__author__ = 'shn7798'
from redis import Redis


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
    WTF_CSRF_ENABLED = False
    SECRET_KEY = "asasasasas"

    ###### flask-sqlalchemy #########
    SQLALCHEMY_DATABASE_URI = "mysql://flaskzhihu:123456@192.168.5.202/flaskzhihu_test?charset=utf8"
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_RECORD_QUERIES = True

    ####### flask-cache ###########
    CACHE_TYPE = 'redis'
    CACHE_REDIS_HOST = '127.0.0.1'
    CACHE_KEY_PREFIX = 'flask_cache_'
    CACHE_REDIS_DB = 1
    #CACHE_TYPE = "simple"
    CACHE_DEFAULT_TIMEOUT = 600

    ######## flask-session ########
    SESSION_TYPE = 'redis'
    SESSION_KEY_PREFIX = 'flask_session_'
    # SESSION_REDIS = Redis('127.0.0.1', db=0)
    SESSION_REDIS = property(lambda self: Redis('127.0.0.1', db=1))


class DeploySettings(IPythonSettings):
    SQLALCHEMY_DATABASE_URI = "mysql://flaskzhihu:123456@192.168.5.202/flaskzhihu?charset=utf8"

