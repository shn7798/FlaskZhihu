# -*- coding: utf-8 -*-
__author__ = 'shn7798'

from pymongo import MongoClient

from flask import Flask

from FlaskZhihu.settings import IPythonSettings
from FlaskZhihu.models import *
from FlaskZhihu.extensions import db

def enc(s):
    if isinstance(s, unicode):
        return s.encode('UTF-8')
    else:
        return s

app = Flask(__name__)
app.config.from_object(IPythonSettings())
db.init_app(app)

ctx = app.app_context()

ctx.push()
mysql = db.session()

update_answers_count_sql = """UPDATE question q SET answers_count = (SELECT COUNT(1) FROM answer a WHERE a.question_id  = q.id) WHERE answers_count <= 0"""


mysql.execute(update_answers_count_sql)
mysql.commit()