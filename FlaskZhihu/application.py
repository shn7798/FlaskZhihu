# -*- coding: utf-8 -*-
from flask import Flask

from FlaskZhihu.settings import DefaultSettings
from FlaskZhihu.extensions import db
from FlaskZhihu.views.index import index


def create_app(settings=DefaultSettings):
    app = Flask(__name__)
    app.config.from_object(settings())
    app.register_blueprint(index)
    with app.app_context():
        db.init_app(app)

    return app
