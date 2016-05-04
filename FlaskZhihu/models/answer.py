# -*- coding: utf-8 -*-
__author__ = 'shn7798'

from FlaskZhihu.extensions import db
from .user import UserOnAnswer
from FlaskZhihu.constants import VOTE_UP, VOTE_DOWN, VOTE_NONE

class Answer(db.Model):
    __tablename__ = 'answer'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    create_time = db.Column('create_time', db.DateTime)
    update_time = db.Column('update_time', db.DateTime)
    content = db.Column('content', db.LargeBinary)
    thanks_count = db.Column('thanks_count', db.Integer)
    excerpt = db.Column('excerpt', db.String(1024))
    user_id = db.Column('user_id', db.ForeignKey(u'user.id'), nullable=False, index=True)
    question_id = db.Column('question_id', db.ForeignKey(u'question.id'), nullable=False, index=True)
    collection_id = db.Column('collection_id', db.ForeignKey(u'collection.id'), index=True)

    user_on_answer = db.relationship(u'UserOnAnswer', backref='answer')

    def voteup_count(self):
        return len(self.voteup_users())

    def votedown_count(self):
        return len(self.votedown_users())

    def vote_count(self):
        return self.voteup_count() - self.votedown_count()

    def voteup_users(self):
        ops = UserOnAnswer.query.filter(
            db.and_(
                UserOnAnswer.answer_id==self.id,
                UserOnAnswer.vote==VOTE_UP,
            )
        ).all()

        return [op.user for op in ops]

    def votedown_users(self):
        ops = UserOnAnswer.query.filter(
            db.and_(
                UserOnAnswer.answer_id == self.id,
                UserOnAnswer.vote == VOTE_DOWN,
            )
        ).all()

        return [op.user for op in ops]

    def thanked_users(self):
        ops = UserOnAnswer.query.filter(
            db.and_(
                UserOnAnswer.answer_id == self.id,
                UserOnAnswer.thank == 1,
            )
        ).all()
        return [op.user for op in ops]


    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self.id)