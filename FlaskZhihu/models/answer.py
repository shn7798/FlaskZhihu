# -*- coding: utf-8 -*-
__author__ = 'shn7798'

from FlaskZhihu.extensions import db


class Answer(db.Model):
    __tablename__ = 'answer'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    create_time = db.Column('create_time', db.DateTime)
    update_time = db.Column('update_time', db.DateTime)
    content = db.Column('content', db.LargeBinary)
    voteup_count = db.Column('voteup_count', db.Integer)
    votedown_count = db.Column('votedown_count', db.Integer)
    vote_count = db.Column('vote_count', db.Integer)
    thanks_count = db.Column('thanks_count', db.Integer)
    excerpt = db.Column('excerpt', db.String(1024))
    user_id = db.Column('user_id', db.ForeignKey(u'user.id'), nullable=False, index=True)
    question_id = db.Column('question_id', db.ForeignKey(u'question.id'), nullable=False, index=True)
    collection_id = db.Column('collection_id', db.ForeignKey(u'collection.id'), index=True)

    user_on_answer = db.relationship(u'UserOnAnswer', backref='answer')
