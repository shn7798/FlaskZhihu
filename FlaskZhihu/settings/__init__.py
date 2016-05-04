# -*- coding: utf-8 -*-
__author__ = 'shn7798'

class DefaultSettings(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql://flaskzhihu:123456@192.168.5.202/flaskzhihu?charset=UTF-8"
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestSettings(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True