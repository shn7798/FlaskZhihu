# -*- coding: utf-8 -*-
from flask import Flask

from FlaskZhihu.settings import DefaultSettings
from FlaskZhihu.extensions import db
from FlaskZhihu.views.index import index
from FlaskZhihu.views.question import QuestionView
from FlaskZhihu.views.answer import AddAnswerView


def create_app(settings=None):
    if not settings:
        settings = DefaultSettings()
    app = Flask(__name__)
    app.config.from_object(settings)
    app.register_blueprint(index)
    QuestionView.register(app, route_base='/question')
    AddAnswerView.register(app, route_base='/answer')
    with app.app_context():
        db.init_app(app)

    return app
