# -*- coding: utf-8 -*-
__author__ = 'shn7798'

from flask import Flask

from FlaskZhihu.settings import TestSettings
from FlaskZhihu.models import *
from FlaskZhihu.extensions import db


if __name__ == '__main__':
    app = Flask(__name__)
    app.config.from_object(TestSettings())
    db.init_app(app)

    ctx = app.app_context()

    ctx.push()

    db.create_all()

    user1 = User()
    user1.id = 1
    user1.username = 'shn7798_1'
    user1.password = '123456'
    user1.name = 'shn7798_1'

    user2 = User()
    user2.id = 2
    user2.username = 'shn7798_2'
    user2.password = '123456'
    user2.name = 'shn7798_2'

    question1 = Question()
    question1.id = 1
    question1.title = 'question 1'
    question1.content = 'question 1 content'
    question1.user = user1

    question2 = Question()
    question2.id = 2
    question2.title = 'question 2'
    question2.content = 'question 2 content'
    question2.user = user1

    answer1_1  = Answer()
    answer1_1.id = 11
    answer1_1.content = 'question 1 answer'
    answer1_1.user = user2

    question1.answers.append(answer1_1)

    session = db.session()
    session.add_all([question1, question2, user1, user2, answer1_1])
    session.commit()

    assert User.get_admin().username == user1.username

