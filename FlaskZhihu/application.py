# -*- coding: utf-8 -*-
from flask import Flask

from FlaskZhihu.settings import DefaultSettings
from FlaskZhihu.extensions import db
from FlaskZhihu.views.index import index
from FlaskZhihu.views import QuestionView, AnswerView, CommentView, UserView
from FlaskZhihu.permissions import login_manager

def create_app(settings=None):
    if not settings:
        settings = DefaultSettings()
    app = Flask(__name__)
    app.config.from_object(settings)
    app.register_blueprint(index)
    # flask login
    login_manager.init_app(app)

    with app.app_context():
        db.init_app(app)

    register_views(app)
    return app


def register_views(app):
    QuestionView.register(app)
    AnswerView.register(app)
    CommentView.register(app)
    UserView.register(app)