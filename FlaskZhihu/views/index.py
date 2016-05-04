# -*- coding: utf-8 -*-
__author__ = 'shn7798'

from flask.blueprints import Blueprint

index = Blueprint('index', __name__)

@index.route('/')
def hello_world():
    return 'Hello World!'