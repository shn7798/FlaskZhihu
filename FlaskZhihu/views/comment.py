# -*- coding: utf-8 -*-
__author__ = 'shn7798'
from flask import url_for, abort, redirect, render_template
from flask.ext.classy import FlaskView, route, request
from flask.ext.login import current_user, login_required

from FlaskZhihu.extensions import db
from FlaskZhihu.forms.comment import CommentForm
from FlaskZhihu.models import Answer, Question, Comment, Collection, User

__all__ = ['CommentView']


class CommentView(FlaskView):
    route_base = '/comment'

    @route(r'/add', methods=['POST'])
    @login_required
    def add(self):
        form = CommentForm()
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
            elif target_type == 'question':
                comment.question = Question.find_by_id(target_id, abort404=True)
            elif target_type == 'collection':
                comment.collection = Collection.find_by_id(target_id, abort404=True)
            elif target_type == 'comment':
                comment.quote_comment = Comment.find_by_id(target_id, abort404=True)
            else:
                abort(500)

            db.session.add(comment)
            db.session.commit()


            if request.referrer:
                return redirect(request.referrer)
            else:
                return redirect('/question')
        else:
            print form.data
            abort(404)