# -*- coding: utf-8 -*-
__author__ = 'shn7798'
from flask import url_for, abort, redirect, render_template
from flask.ext.classy import FlaskView, route, request

from FlaskZhihu.extensions import db
from FlaskZhihu.forms.answer import AnswerForm
from FlaskZhihu.forms.comment import CommentForm
from FlaskZhihu.models import Answer, Question, Comment, Collection, User


class CommentView(FlaskView):
    route_base = '/comment'

    @route(r'/add', methods=['POST'])
    def add(self):
        form = CommentForm()
        if form.validate_on_submit():
            data = form.data
            print data
            target_type = str(data['target_type'])
            target_id = str(data['target_id'])

            # current user not readly
            # user_id = str(data['user_id'])
            # user = User.find_by_id(user_id, abort404=True)

            comment = Comment()
            comment.content = data['content']
            # comment.user = user
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