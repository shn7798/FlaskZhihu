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