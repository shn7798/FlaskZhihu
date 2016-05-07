# -*- coding: utf-8 -*-
__author__ = 'shn7798'

from FlaskZhihu.extensions import db
from FlaskZhihu.models.base import DateTimeMixin, FindByIdMixin
from flask.ext.sqlalchemy_cache import CachingQuery


class Topic(DateTimeMixin, FindByIdMixin, db.Model):
    __tablename__ = 'topic'
    query_class = CachingQuery

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('name', db.String(60))
    description = db.Column('description', db.String(1024))
    avatar_url = db.Column('avatar_url', db.String(200))

    questions = db.relationship(u'Question', secondary='topic_and_question', backref='topics')
    user_on_topic = db.relationship(u'UserOnTopic', backref='topic')

    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self.name)



class TopicAndQuestion(DateTimeMixin, FindByIdMixin, db.Model):
    __tablename__ = 'topic_and_question'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    topic_id = db.Column('topic_id', db.ForeignKey(u'topic.id'), nullable=False, index=True)
    question_id = db.Column('question_id', db.ForeignKey(u'question.id'), nullable=False, index=True)
