# -*- coding: utf-8 -*-
__author__ = 'shn7798'

from FlaskZhihu.extensions import db
from FlaskZhihu.models.base import DateTimeMixin, FindByIdMixin
from flask.ext.sqlalchemy_cache import CachingQuery


class Collection(DateTimeMixin, FindByIdMixin, db.Model):
    __tablename__ = 'collection'
    query_class = CachingQuery

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    title = db.Column('title', db.String(60))
    description = db.Column('description', db.String(4096))
    user_id = db.Column('user_id', db.ForeignKey(u'user.id'), nullable=False, index=True)
    user_hashid = db.Column('user_hashid', db.String(32))

    answers = db.relationship(u'Answer', secondary='collection_and_answer', backref='collections')
    comments = db.relationship(u'Comment', backref='collection')
    user_on_collection = db.relationship(u'UserOnCollection', backref='collection')

    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self.title)


class CollectionAndAnswer(DateTimeMixin, FindByIdMixin, db.Model):
    __tablename__ = 'collection_and_answer'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    collection_id = db.Column('collection_id', db.ForeignKey(u'collection.id'), nullable=False, index=True)
    answer_id = db.Column('answer_id', db.ForeignKey(u'answer.id'), nullable=False, index=True)
