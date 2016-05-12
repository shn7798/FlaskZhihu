# -*- coding: utf-8 -*-
__author__ = 'shn7798'

from FlaskZhihu.extensions import db
from FlaskZhihu.models import *
from FlaskZhihu.constants import *
from FlaskZhihu.signals import *
from FlaskZhihu.helpers import use_signal

@use_signal(question_answer_add)
def update_question_answers_count(sender):
    assert isinstance(sender, Question)
    sender.answers_count = \
        Answer.query.filter(Answer.question_id == sender.id).count()

    db.session.commit()

@use_signal(question_follow)
@use_signal(question_unfollow)
def update_question_following_count(sender):
    assert isinstance(sender, Question)
    sender.following_count = \
        UserOnQuestion.query.filter(
            db.and_(UserOnQuestion.question_id == sender.id, UserOnQuestion.follow == True)
        ).count()

    db.session.commit()


@use_signal(question_comment_add)
@use_signal(question_comment_delete)
def update_question_comments_count(sender):
    assert isinstance(sender, Question)
    sender.comments_count = \
        Comment.query.filter(
            Comment.question_id == sender.id
        ).count()

    db.session.commit()

############# answer ############
@use_signal(answer_comment_add)
@use_signal(answer_comment_delete)
def update_answer_comments_count(sender):
    assert isinstance(sender, Answer)
    sender.comments_count = \
        Comment.query.filter(
            Comment.answer_id == sender.id
        ).count()

    db.session.commit()


@use_signal(answer_voteup)
@use_signal(answer_votedown)
@use_signal(answer_cancel_vote)
def update_answer_vote_count(sender):
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
@use_signal(comment_voteup)
@use_signal(comment_cancel_vote)
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


############# collection ############

@use_signal(collection_answer_add)
@use_signal(collection_answer_delete)
def update_collection_answers_count(sender):
    assert isinstance(sender, Collection)
    answers_count = CollectionAndAnswer.query.filter(
        CollectionAndAnswer.collection_id == sender.id
    ).count()

    sender.answers_count = answers_count
    db.session.commit()


@use_signal(collection_follow)
@use_signal(collection_unfollow)
def update_collection_following_count(sender):
    assert isinstance(sender, Collection)
    following_count = UserOnCollection.query.filter(
        db.and_(
            UserOnCollection.collection_id == sender.id,
            UserOnCollection.follow == FOLLOW_ON,
        )
    ).count()

    sender.following_count = following_count
    db.session.commit()