# -*- coding: utf-8 -*-
__author__ = 'shn7798'

from FlaskZhihu.extensions import db


class Comment(db.Model):
    __tablename__ = 'comment'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    create_time = db.Column('create_time', db.DateTime)
    update_time = db.Column('update_time', db.DateTime)
    content = db.Column('content', db.String(4096))
    user_id = db.Column('user_id', db.ForeignKey(u'user.id'), nullable=False, index=True)
    voteup = db.Column('voteup', db.Integer)

    answer_id = db.Column('answer_id', db.ForeignKey(u'answer.id'), nullable=False, index=True)
    question_id = db.Column('question_id', db.ForeignKey(u'question.id'), nullable=False, index=True)
    collection_id = db.Column('collection_id', db.ForeignKey(u'collection.id'), nullable=False, index=True)

    user_on_comment = db.relationship(u'UserOnComment', backref='comment')
