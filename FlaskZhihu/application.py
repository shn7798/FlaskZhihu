# -*- coding: utf-8 -*-
from flask import Flask

from FlaskZhihu.settings import DefaultSettings
from FlaskZhihu.extensions import db, cache
from FlaskZhihu.views.index import index
from FlaskZhihu.views import QuestionView, AnswerView, CommentView, UserView
from FlaskZhihu.views.question import question
from FlaskZhihu.permissions import login_manager

def create_app(settings=None):
    if not settings:
        settings = DefaultSettings()
    app = Flask(__name__)
    app.config.from_object(settings)

    # flask login
    login_manager.init_app(app)

    init_extensions(app)
    init_views(app)
    return app


def init_extensions(app):
    db.init_app(app)
    cache.init_app(app)


def init_views(app):
    app.register_blueprint(index)
    #QuestionView.register(app)
    app.register_blueprint(question)
    AnswerView.register(app)
    CommentView.register(app)
    UserView.register(app)