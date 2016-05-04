# -*- coding: utf-8 -*-
__author__ = 'shn7798'

from flask import Flask

from FlaskZhihu.settings import TestSettings
from FlaskZhihu.models import *
from FlaskZhihu.extensions import db

import unittest

class OrmTestCase(unittest.TestCase):
    def setUp(self):
        app = Flask(__name__)
        app.config.from_object(TestSettings())
        db.init_app(app)

        ctx = app.app_context()

        ctx.push()
        db.create_all()
        session = db.session()

        self.app = app
        self.db = db
        self.ctx = ctx
        self.session = session
        print "setUp"

    def tearDown(self):
        self.db.drop_all()
        self.ctx.pop()


    def test_1_create_user(self):
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

        self.session.add_all([user1, user2])
        self.session.commit()

        u1 = User.query.filter(User.username=='shn7798_1').first_or_404()
        u2 = User.query.filter(User.id==2).first_or_404()

        self.assertEqual(user1, u1)
        self.assertEqual(user2, u2)

        self.user1 = user1
        self.user2 = user2

    def test_2_create_question(self):
        # 创建问题1
        question1 = Question()
        question1.id = 1
        question1.title = 'question 1'
        question1.content = 'question 1 content'
        question1.user = self.user1
        self.session.add(question1)
        self.session.commit()

        q1 = Question.query.filter(Question.id==1).first_or_404()
        self.assertEqual(q1.title, 'question 1')
        self.assertEqual(q1.content, 'question 1 content')
        self.assertEqual(q1.user_id, self.user1.id)

        self.question1 = question1

    def test_3_create_answer(self):
        # user2 创建答案
        answer1 = Answer()
        answer1.id = 11
        answer1.content = 'question 1 answer'
        answer1.user = self.user2
        answer1.question = self.question1

        self.session.add(answer1)
        self.session.commit()

        a1 = Answer.query.filter(Answer.id==11).first_or_404()
        self.assertEqual(a1.content, 'question 1 answer')
        self.assertEqual(a1.user_id, self.user2.id)

    def test_4_user_follow_question(self):
        self.user1.op_on_questions.append(self.question1)
        uoq = self.user1.op_on_question(self.question1)
        uoq.follow = True

        self.session.commit()
        assert self.user1 in self.question1.following_users()



if __name__ == '__main__':
    unittest.main()

