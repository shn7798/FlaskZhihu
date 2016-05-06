# -*- coding: utf-8 -*-
__author__ = 'shn7798'
from flask import url_for, abort, redirect, render_template
from flask.ext.classy import FlaskView, route

from FlaskZhihu.extensions import db
from FlaskZhihu.forms.answer import AnswerForm
from FlaskZhihu.models import Answer, Question


class AnswerView(FlaskView):
    route_base = '/answer'

    @route(r'/add', methods=['POST'])
    def add(self):
        form = AnswerForm()
        if form.validate_on_submit():
            print form.question_id.data
            print form.content.data
            question = Question.find_by_id(form.question_id.data, abort404=True)
            answer = Answer()
            answer.content = form.content.data
            answer.question = question
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