# -*- coding: utf-8 -*-
__author__ = 'shn7798'

from flask import redirect
from flask.blueprints import Blueprint

index = Blueprint('index', __name__)

@index.route('/')
def index_page():
    return redirect('/question/')