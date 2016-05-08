# -*- coding: utf-8 -*-
__author__ = 'shn7798'
from flask import url_for, abort, redirect, render_template, request
from flask.ext.classy import FlaskView, route
from flask.ext.login import current_user, login_required

from FlaskZhihu.extensions import db
from FlaskZhihu.forms import AnswerAddForm, AnswerEditForm
from FlaskZhihu.models import Answer, Question, User
from FlaskZhihu.signals import *
from FlaskZhihu.helpers import keep_next_url

__all__ = ['AnswerView']


class AnswerView(FlaskView):
    route_base = '/answer'

    @route(r'/add/', methods=['POST'])
    @login_required
    def add(self):
        form = AnswerAddForm()
        if form.validate_on_submit():
            question = Question.query.get_or_404(form.question_id.data)
            if Answer.query.filter(Answer.question_id == question.id).filter(Answer.user_id == current_user.id).count():
                # answer exists
                return redirect(url_for('QuestionView:show', id=str(form.question_id.data)))
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

    @route(r'/<int:id>/')
    def show(self, id):
        answer = Answer.find_by_id(id, abort404=True)

        return render_template('answer/show.html', answer=answer)

    @route(r'/<int:id>/voteup/')
    @login_required
    def voteup(self, id):
        answer = Answer.find_by_id(id, abort404=True)
        current_user.voteup_answer(answer)
        db.session.commit()

        answer_voteup.send(answer)

        return redirect(request.referrer or '/')

    @route(r'/<int:id>/votedown/')
    @login_required
    def votedown(self, id):
        answer = Answer.find_by_id(id, abort404=True)
        current_user.votedown_answer(answer)
        db.session.commit()

        answer_votedown.send(answer)

        return redirect(request.referrer or '/')

    @route(r'/<int:id>/cancel_vote/')
    @login_required
    def cancel_vote(self, id):
        answer = Answer.find_by_id(id, abort404=True)
        current_user.voteup_answer(answer, undo=True)
        current_user.votedown_answer(answer, undo=True)
        db.session.commit()

        answer_cancel_vote.send(answer)

        return redirect(request.referrer or '/')


    @route(r'/my/')
    @login_required
    def my(self):
        assert current_user.id
        answers = Answer.query.options(db.joinedload('question'))\
            .filter(Answer.user_id == current_user.id).all()

        return render_template('answer/my.html', answers=answers)


    @route(r'/<int:id>/edit/', methods=['GET', 'POST'])
    @login_required
    @keep_next_url
    def edit(self, id, next_url=None):
        answer = Answer.query.get_or_404(id)
        form = AnswerEditForm()
        if form.validate_on_submit():
            answer.content = form.content.data
            db.session.commit()
            return redirect(next_url or url_for('QuestionView:show', id=answer.question_id))
        else:
            form.content.data = answer.content
            return render_template('answer/edit.html', form=form)