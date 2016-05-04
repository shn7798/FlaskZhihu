# -*- coding: utf-8 -*-
__author__ = 'shn7798'

from FlaskZhihu.extensions import db
from .user import UserOnQuestion


class Question(db.Model):
    __tablename__ = 'question'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    create_time = db.Column('create_time', db.DateTime)
    update_time = db.Column('update_time', db.DateTime)
    answers_update_time = db.Column('answers_update_time', db.DateTime)
    title = db.Column('title', db.String(60))
    content = db.Column('content', db.LargeBinary)
    excerpt = db.Column('excerpt', db.String(1024))
    answer_ids = db.Column('answer_ids', db.Integer)
    status = db.Column('status', db.String(45))
    user_id = db.Column('user_id', db.ForeignKey(u'user.id'), nullable=False, index=True)

    answers = db.relationship(u'Answer', backref='question')
    comments = db.relationship(u'Comment', backref='question')

    user_on_question = db.relationship(u'UserOnQuestion', backref='question')

    def following_users(self):
        uoqs = UserOnQuestion.query.filter(
            db.and_(UserOnQuestion.question_id == self.id, UserOnQuestion.follow==True)
        ).all()

        return [uoq.user for uoq in uoqs]


    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self.title)