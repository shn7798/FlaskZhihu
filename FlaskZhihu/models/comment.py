# -*- coding: utf-8 -*-
__author__ = 'shn7798'

from FlaskZhihu.models.user import UserOnComment
from FlaskZhihu.extensions import db
from FlaskZhihu.models.base import DateTimeMixin, FindByIdMixin
from FlaskZhihu.constants import VOTE_UP, VOTE_NONE, VOTE_DOWN
from flask.ext.sqlalchemy_cache import CachingQuery


class Comment(DateTimeMixin, FindByIdMixin, db.Model):
    __tablename__ = 'comment'
    query_class = CachingQuery

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    content = db.Column('content', db.String(4096))
    comment_target = db.Column('comment_target', db.String(10))
    user_id = db.Column('user_id', db.ForeignKey(u'user.id'), index=True)
    user_hashid = db.Column('user_hashid', db.String(32))

    quote_comment_id = db.Column('quote_comment_id', db.ForeignKey(u'comment.id'), index=True)
    answer_id = db.Column('answer_id', db.ForeignKey(u'answer.id'), index=True)
    question_id = db.Column('question_id', db.ForeignKey(u'question.id'), index=True)
    collection_id = db.Column('collection_id', db.ForeignKey(u'collection.id'), index=True)

    user_on_comment = db.relationship(u'UserOnComment', backref='comment')
    reply_comments = db.relationship("Comment",
                            backref=db.backref('quote_comment', remote_side=[id]))

    @property
    def voteup_count(self):
        return UserOnComment.query.filter(
            db.and_(
                UserOnComment.comment_id == self.id,
                UserOnComment.vote == VOTE_UP,
            )
        ).count()

    @property
    def voteup_users(self):
        ops = UserOnComment.query.filter(
            db.and_(
                UserOnComment.comment_id == self.id,
                UserOnComment.vote == VOTE_UP,
            )
        ).all()

        return [op.user for op in ops]

    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self.content[0:8])