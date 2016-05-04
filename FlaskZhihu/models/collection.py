# -*- coding: utf-8 -*-
__author__ = 'shn7798'

from FlaskZhihu.extensions import db


class Collection(db.Model):
    __tablename__ = 'collection'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    create_time = db.Column('create_time', db.DateTime)
    update_time = db.Column('update_time', db.DateTime)
    title = db.Column('title', db.String(60))
    description = db.Column('description', db.String(4096))
    user_id = db.Column('user_id', db.ForeignKey(u'user.id'), nullable=False, index=True)

    answers = db.relationship(u'Answer', secondary='collection_and_answer', backref='collections')
    comments = db.relationship(u'Comment', backref='collections')
    user_on_collection = db.relationship(u'UserOnCollection', backref='collection')


class CollectionAndAnswer(db.Model):
    __tablename__ = 'collection_and_answer'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    collection_id = db.Column('collection_id', db.ForeignKey(u'collection.id'), nullable=False, index=True)
    answer_id = db.Column('answer_id', db.ForeignKey(u'answer.id'), nullable=False, index=True)
