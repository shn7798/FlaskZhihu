# -*- coding: utf-8 -*-
__author__ = 'shn7798'

from FlaskZhihu.extensions import db
from FlaskZhihu.models import *
from FlaskZhihu.constants import *
from FlaskZhihu.signals import *


def update_question_answers_count(sender):
    assert isinstance(sender, Question)
    sender.answers_count = \
        Answer.query.filter(Answer.question_id == sender.id).count()

    db.session.commit()

def update_question_following_count(sender):
    assert isinstance(sender, Question)
    sender.following_count = \
        UserOnQuestion.query.filter(
            db.and_(UserOnQuestion.question_id == sender.id, UserOnQuestion.follow == True)
        ).count()

    db.session.commit()


def update_question_comments_count(sender):
    assert isinstance(sender, Question)
    sender.comments_count = \
        Comment.query.filter(
            Comment.question_id == sender.id
        ).count()

    db.session.commit()

############# answer ############

def update_answer_comments_count(sender):
    assert isinstance(sender, Answer)
    sender.comments_count = \
        Comment.query.filter(
            Comment.answer_id == sender.id
        ).count()

    db.session.commit()


def update_answer_vote_count(sender):
    print 'update_answer_vote_count'
    assert isinstance(sender, Answer)
    ops = UserOnAnswer.query.filter(
        db.and_(
            UserOnAnswer.answer_id == sender.id,
            UserOnAnswer.vote != VOTE_NONE,
        )
    ).all()

    sender.voteup_count = len(filter(lambda x: x.vote == VOTE_UP, ops))
    sender.votedown_count = len(filter(lambda x: x.vote == VOTE_DOWN, ops))
    db.session.commit()


######### comment

def update_comment_vote_count(sender):
    assert isinstance(sender, Comment)
    voteup_count = UserOnComment.query.filter(
        db.and_(
            UserOnComment.comment_id == sender.id,
            UserOnComment.vote == VOTE_UP,
        )
    ).count()

    sender.voteup_count = voteup_count
    db.session.commit()


def register_signals():
    ######## connect ###########
    question_comment_add.connect(update_question_comments_count)
    question_comment_delete.connect(update_question_comments_count)

    question_answer_add.connect(update_question_answers_count)

    question_comment_add.connect(update_question_comments_count)
    question_comment_delete.connect(update_question_comments_count)

    question_follow.connect(update_question_following_count)
    question_unfollow.connect(update_question_following_count)

    answer_comment_add.connect(update_answer_comments_count)
    answer_comment_delete.connect(update_answer_comments_count)

    answer_voteup.connect(update_answer_vote_count)
    answer_votedown.connect(update_answer_vote_count)
    answer_cancel_vote.connect(update_answer_vote_count)

    comment_voteup.connect(update_comment_vote_count)
    comment_cancel_vote.connect(update_comment_vote_count)