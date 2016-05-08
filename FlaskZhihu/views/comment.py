# -*- coding: utf-8 -*-
__author__ = 'shn7798'
from flask import url_for, abort, redirect, render_template
from flask.ext.classy import FlaskView, route, request
from flask.ext.login import current_user, login_required

from FlaskZhihu.extensions import db
from FlaskZhihu.forms import CommentAddForm
from FlaskZhihu.models import Answer, Question, Comment, Collection, User
from FlaskZhihu.signals import *

__all__ = ['CommentView']


class CommentView(FlaskView):
    route_base = '/comment'

    @route(r'/add/', methods=['POST'])
    @login_required
    def add(self):
        form = CommentAddForm()
        if form.validate_on_submit():
            data = form.data
            print data
            target_type = str(data['target_type'])
            target_id = str(data['target_id'])

            comment = Comment()
            comment.user = current_user
            comment.content = data['content']
            comment.comment_target = target_type
            if target_type == 'answer':
                comment.answer = Answer.find_by_id(target_id, abort404=True)

                answer_comment_add.send(comment.answer)

                db.session.add(comment)
                db.session.commit()
            elif target_type == 'question':
                comment.question = Question.find_by_id(target_id, abort404=True)

                question_comment_add.send(comment.question)

                db.session.add(comment)
                db.session.commit()
            elif target_type == 'collection':
                comment.collection = Collection.find_by_id(target_id, abort404=True)

                #collection_comment_add.send(comment.collection)

                db.session.add(comment)
                db.session.commit()
            elif target_type == 'comment':
                comment.quote_comment = Comment.find_by_id(target_id, abort404=True)
                db.session.add(comment)
                db.session.commit()
            else:
                abort(500)

            if request.referrer:
                return redirect(request.referrer)
            else:
                return redirect('/question')
        else:
            print form.data
            abort(404)

    @route(r'/<int:id>/voteup/')
    @login_required
    def voteup(self, id):
        comment = Comment.find_by_id(id, abort404=True)
        current_user.voteup_comment(comment)
        db.session.commit()

        comment_voteup.send(comment)

        return redirect(request.referrer or '/')


    @route(r'/<int:id>/cancel_vote/')
    @login_required
    def cancel_vote(self, id):
        comment = Comment.find_by_id(id, abort404=True)
        current_user.voteup_comment(comment, undo=True)
        db.session.commit()

        comment_cancel_vote.send(comment)

        return redirect(request.referrer or '/')
