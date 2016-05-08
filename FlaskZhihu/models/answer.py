# -*- coding: utf-8 -*-
__author__ = 'shn7798'

from FlaskZhihu.extensions import db
from FlaskZhihu.models.base import DateTimeMixin, FindByIdMixin, blob_unicode
from FlaskZhihu.models.user import UserOnAnswer
from FlaskZhihu.constants import VOTE_UP, VOTE_DOWN, VOTE_NONE, THANK_ON
from flask.ext.sqlalchemy_cache import CachingQuery


class Answer(DateTimeMixin, FindByIdMixin, db.Model):
    __tablename__ = 'answer'
    query_class = CachingQuery

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    thanks_count = db.Column('thanks_count', db.Integer)
    excerpt = db.Column('excerpt', db.String(4096))
    user_id = db.Column('user_id', db.ForeignKey(u'user.id'), index=True)
    user_hashid = db.Column('user_hashid', db.String(32))
    question_id = db.Column('question_id', db.ForeignKey(u'question.id'), index=True)
    collection_id = db.Column('collection_id', db.ForeignKey(u'collection.id'), index=True)

    user_on_answer = db.relationship(u'UserOnAnswer', backref='answer')
    comments = db.relationship(u'Comment', backref='answer')

    _content = db.Column('content', db.LargeBinary)
    content = blob_unicode('_content')

    # count cache
    comments_count = db.Column('comments_count', db.Integer, server_default='0')
    voteup_count = db.Column('voteup_count', db.Integer, server_default='0')
    votedown_count = db.Column('votedown_count', db.Integer, server_default='0')



    @property
    def vote_count(self):
        return self.voteup_count - self.votedown_count

    @property
    def voteup_users(self):
        ops = UserOnAnswer.query.filter(
            db.and_(
                UserOnAnswer.answer_id==self.id,
                UserOnAnswer.vote==VOTE_UP,
            )
        ).all()

        return [op.user for op in ops]

    @property
    def votedown_users(self):
        ops = UserOnAnswer.query.filter(
            db.and_(
                UserOnAnswer.answer_id == self.id,
                UserOnAnswer.vote == VOTE_DOWN,
            )
        ).all()

        return [op.user for op in ops]

    @property
    def thanked_users(self):
        ops = UserOnAnswer.query.filter(
            db.and_(
                UserOnAnswer.answer_id == self.id,
                UserOnAnswer.thank == THANK_ON,
            )
        ).all()
        return [op.user for op in ops]


    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self.id)