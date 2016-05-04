# -*- coding: utf-8 -*-
__author__ = 'shn7798'

from flask import Flask

from FlaskZhihu.settings import TestSettings
from FlaskZhihu.models import *
from FlaskZhihu.extensions import db

Base = db.Model
Column = db.Column
Integer = db.Integer
ForeignKey = db.ForeignKey
String = db.String
relationship = db.relationship
backref=db.backref

#
# class Node1(Base):
#     __tablename__ = 'node1'
#     id = Column(Integer, primary_key=True)
#     parent_id = Column(Integer, ForeignKey('node1.id'))
#     data = Column(String(50))
#     parent = relationship("Node1", remote_side=[id])
#
# class Node2(Base):
#     __tablename__ = 'node2'
#     id = Column(Integer, primary_key=True)
#     parent_id = Column(Integer, ForeignKey('node2.id'))
#     data = Column(String(50))
#     children = relationship("Node2",
#                 backref=backref('parent', remote_side=[id])
#             )



def init(db):

        db.create_all()
        session = db.session()

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

        user3 = User()
        user3.id = 3
        user3.username = 'shn7798_3'
        user3.password = '123456'
        user3.name = 'shn7798_3'

        session.add_all([user1, user2, user3])
        session.commit()

        u1 = User.query.filter(User.username == 'shn7798_1').first_or_404()
        u2 = User.query.filter(User.id == 2).first_or_404()

        assert (user1 == u1)
        assert (user2 == u2)

        # 创建问题1
        question1 = Question()
        question1.id = 1
        question1.title = 'question 1'
        question1.content = 'question 1 content'
        question1.user = user1
        session.add(question1)
        session.commit()

        q1 = Question.query.filter(Question.id == 1).first_or_404()
        assert (q1.title == 'question 1')
        assert (q1.content == 'question 1 content')
        assert (q1.user_id == user1.id)

        # user2 创建答案
        answer1 = Answer()
        answer1.id = 11
        answer1.content = 'question 1 answer'
        answer1.user = user2
        answer1.question = question1

        session.add(answer1)
        session.commit()

        a1 = Answer.query.filter(Answer.id == 11).first_or_404()
        assert (a1.content == 'question 1 answer')
        assert (a1.user_id == user2.id)

        user1.op_on_questions.append(question1)
        uoq = user1.op_on_question(question1)
        uoq.follow = True

        session.commit()
        assert user1 in question1.following_users()

        op = user1.op_on_user(user2, edit=True)
        op.follow = True
        session.commit()

        user1.voteup_answer(answer1)
        session.commit()

        user1.block_user(user3)
        session.commit()


if __name__ == '__main__':
        app = Flask(__name__)
        app.config.from_object(TestSettings())
        db.init_app(app)

        ctx = app.app_context()

        ctx.push()
        session = db.session()



