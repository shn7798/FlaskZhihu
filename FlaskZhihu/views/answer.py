# -*- coding: utf-8 -*-
__author__ = 'shn7798'
from flask import url_for, abort, redirect, render_template, request
from flask.ext.classy import FlaskView, route
from flask.ext.login import current_user, login_required

from FlaskZhihu.extensions import db
from FlaskZhihu.forms import AnswerAddForm
from FlaskZhihu.models import Answer, Question, User
from FlaskZhihu.signals import *

__all__ = ['AnswerView']


class AnswerView(FlaskView):
    route_base = '/answer'

    @route(r'/add', methods=['POST'])
    @login_required
    def add(self):
        form = AnswerAddForm()
        if form.validate_on_submit():
            print form.question_id.data
            print form.content.data
            question = Question.find_by_id(form.question_id.data, abort404=True)
            answer = Answer()
            answer.content = form.content.data
            answer.question = question
            answer.user = current_user
            db.session.add(answer)
            db.session.commit()

            question_answer_add.send(question)

        if form.question_id.data:
            return redirect(url_for('QuestionView:show', id=str(form.question_id.data)))
        else:
            abort(404)

    @route(r'/<int:id>')
    def show(self, id):
        answer = Answer.find_by_id(id, abort404=True)

        return render_template('answer/show.html', answer=answer)

    @route(r'/<int:id>/voteup')
    @login_required
    def voteup(self, id):
        answer = Answer.find_by_id(id, abort404=True)
        current_user.voteup_answer(answer)
        db.session.commit()

        answer_voteup.send(answer)

        return redirect(request.referrer or '/')

    @route(r'/<int:id>/votedown')
    @login_required
    def votedown(self, id):
        answer = Answer.find_by_id(id, abort404=True)
        current_user.votedown_answer(answer)
        db.session.commit()

        answer_votedown.send(answer)

        return redirect(request.referrer or '/')

    @route(r'/<int:id>/cancel_vote')
    @login_required
    def cancel_vote(self, id):
        answer = Answer.find_by_id(id, abort404=True)
        current_user.voteup_answer(answer, undo=True)
        current_user.votedown_answer(answer, undo=True)
        db.session.commit()

        answer_cancel_vote.send(answer)

        return redirect(request.referrer or '/')

