# -*- coding: utf-8 -*-
__author__ = 'shn7798'

from flask import url_for, abort, redirect, render_template, request
from flask.ext.classy import FlaskView, route
from flask.ext.login import current_user, login_required

from FlaskZhihu.extensions import db
from FlaskZhihu.forms import AnswerAddForm
from FlaskZhihu.models import Answer, Question, User
from FlaskZhihu.signals import *

__all__ = ['AnswerApiView', 'QuestionApiView', 'UserApiView', 'CollectionApiView', 'CommentApiView']

class BaseApiView(FlaskView):
    route_prefix = '/api'


class QuestionApiView(BaseApiView):
    route_base = '/question'
    decorators = [login_required]

    @route('/follow/<int:id>')
    def follow(self, id):
        pass

    @route('/collect/<int:id>')
    def collect(self, id):
        pass


class AnswerApiView(BaseApiView):
    route_base = '/answer'
    decorators = [login_required]

    @route('/vote/<int:id>')
    def vote(self, id):
        pass

    @route('/follow/<int:id>')
    def follow(self, id):
        pass

    @route('/comment/<int:id>')
    def comment(self, id):
        pass

    @route('/thank/<int:id>')
    def thank(self, id):
        pass


class UserApiView(BaseApiView):
    route_base = '/user'
    decorators = [login_required]

    def add(self):
        pass


class CommentApiView(BaseApiView):
    route_base = '/comment'
    decorators = [login_required]



class CollectionApiView(BaseApiView):
    route_base = '/collection'
    decorators = [login_required]