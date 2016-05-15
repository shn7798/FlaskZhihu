# -*- coding: utf-8 -*-
from flask import Flask

from FlaskZhihu.settings import DefaultSettings
from FlaskZhihu.extensions import db, cache, session
from FlaskZhihu.views.index import index
from FlaskZhihu.views import QuestionView, AnswerView, CommentView, UserView, CollectionView
from FlaskZhihu.permissions import login_manager
from FlaskZhihu.api import *


def create_app(settings=None):
    if not settings:
        settings = DefaultSettings()
    app = Flask(__name__)
    app.config.from_object(settings)

    # flask login
    login_manager.init_app(app)
    session.init_app(app)

    init_extensions(app)
    init_views(app)
    return app


def init_extensions(app):
    db.init_app(app)
    cache.init_app(app)


def init_views(app):
    app.register_blueprint(index)
    QuestionView.register(app)
    AnswerView.register(app)
    CommentView.register(app)
    UserView.register(app)
    CollectionView.register(app)

    # api
    QuestionApiView.register(app)
    AnswerApiView.register(app)
    UserApiView.register(app)
    CommentApiView.register(app)
    CollectionApiView.register(app)