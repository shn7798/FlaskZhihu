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
    WTF_CSRF_ENABLED = False
    SECRET_KEY = "asasasasas"

    ###### flask-sqlalchemy #########
    SQLALCHEMY_DATABASE_URI = "mysql://flaskzhihu:123456@192.168.5.202/flaskzhihu_test?charset=utf8"
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_RECORD_QUERIES = True

    ####### flask-cache ###########
    CACHE_TYPE = 'redis'
    CACHE_REDIS_HOST = '127.0.0.1'
    CACHE_KEY_PREFIX = 'flask_'
    #CACHE_TYPE = "simple"
    #CACHE_DEFAULT_TIMEOUT = 600


class DeploySettings(IPythonSettings):
    SQLALCHEMY_DATABASE_URI = "mysql://flaskzhihu:123456@192.168.5.202/flaskzhihu?charset=utf8"

