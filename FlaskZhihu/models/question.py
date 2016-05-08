# -*- coding: utf-8 -*-
__author__ = 'shn7798'

from FlaskZhihu.extensions import db
from FlaskZhihu.models.user import UserOnQuestion
from FlaskZhihu.models.base import DateTimeMixin, FindByIdMixin, blob_unicode
from flask.ext.sqlalchemy_cache import CachingQuery


class Question(DateTimeMixin, FindByIdMixin, db.Model):
    __tablename__ = 'question'
    query_class = CachingQuery

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    answers_update_time = db.Column('answers_update_time', db.DateTime)
    title = db.Column('title', db.String(500))
    excerpt = db.Column('excerpt', db.String(4096))
    answer_ids = db.Column('answer_ids', db.Integer)

    # count cache
    voteup_count = db.Column('voteup_count', db.Integer, server_default='0')
    votedown_count = db.Column('votedown_count', db.Integer, server_default='0')
    answers_count = db.Column('answers_count', db.Integer, server_default='0')
    following_count = db.Column('following_count', db.Integer, server_default='0')
    comments_count = db.Column('comments_count', db.Integer, server_default='0')

    status = db.Column('status', db.String(45))
    user_id = db.Column('user_id', db.ForeignKey(u'user.id'), index=True)
    user_hashid = db.Column('user_hashid', db.String(32))

    answers = db.relationship(u'Answer', backref='question')
    comments = db.relationship(u'Comment', backref='question')

    _content = db.Column('content', db.LargeBinary)
    content = blob_unicode('_content')

    user_on_question = db.relationship(u'UserOnQuestion', backref='question')

    @property
    def following_users(self):
        uoqs = UserOnQuestion.query.filter(
            db.and_(UserOnQuestion.question_id == self.id, UserOnQuestion.follow==True)
        ).all()

        return [uoq.user for uoq in uoqs]


    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self.title)
