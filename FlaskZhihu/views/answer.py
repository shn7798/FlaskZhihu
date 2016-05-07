# -*- coding: utf-8 -*-
__author__ = 'shn7798'
from flask import url_for, abort, redirect, render_template
from flask.ext.classy import FlaskView, route
from flask.ext.login import current_user, login_required

from FlaskZhihu.extensions import db
from FlaskZhihu.forms import AnswerAddForm
from FlaskZhihu.models import Answer, Question

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

        if form.question_id.data:
            return redirect(url_for('QuestionView:show', id=str(form.question_id.data)))
        else:
            abort(404)

    @route(r'/<int:id>')
    def show(self, id):
        answer = Answer.find_by_id(id, abort404=True)

        return render_template('answer/show.html', answer=answer)