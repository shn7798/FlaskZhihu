# -*- coding: utf-8 -*-
__author__ = 'shn7798'

from pymongo import MongoClient

from flask import Flask

from FlaskZhihu.settings import TestSettings
from FlaskZhihu.models import *
from FlaskZhihu.extensions import db

def enc(s):
    return s.encode('UTF-8')

app = Flask(__name__)
app.config.from_object(TestSettings())
db.init_app(app)

ctx = app.app_context()

ctx.push()
mysql = db.session()

mg = MongoClient('192.168.5.202').zhihu

print User.query.delete()
mysql.commit()
#exit(1)
cur = mg.people.find().limit(5000)

i = 0
for people in cur:
    p = people['data']

    u = User()
    u.hashid = p['id']
    u.name = enc(p['name'])
    u.password = '123456'
    u.username = enc(p['name'])
    u.avatar_url = enc(p['avatar_url'])
    u.headline = enc(p['headline'])
    u.description = enc(p['description'])
    u.user_hashid = p['id']
    u.gender = p['gender']

    mysql.add(u)

    i += 1
    if i % 100 == 0:
        mysql.commit()

mysql.commit()