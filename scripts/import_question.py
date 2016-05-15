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

mg = MongoClient('192.168.5.202').zhihu

print Question.query.delete()
mysql.commit()
#exit(1)

cur = mg.questions.find() #.limit(100000)
i = 0
for item in cur:
    try:
        d = item['data']
        o = Question()
        o.title = enc(d['title'])
        o.id = int(d['id'])
        o.excerpt = enc(d.get('excerpt', ''))
        o.content = enc(d['detail'])
        o.user_hashid = enc(d['author']['id'])
        # o.answers_count = Answer.query.filter(Answer.question_id == o.id).count()

        u = User.get_user_by_hashid(o.user_hashid)
        if u:
            o.user = u

        mysql.add(o)
    except:
        pass

    i += 1
    if i % 100 == 0:
        mysql.commit()

mysql.commit()