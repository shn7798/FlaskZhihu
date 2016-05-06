# -*- coding: utf-8 -*-
__author__ = 'shn7798'

from flask.ext.classy import FlaskView, route
from flask import abort, render_template

from FlaskZhihu.models.question import *
from FlaskZhihu.forms.answer import AnswerForm


class QuestionView(FlaskView):
    route_base = '/question'

    @route(r'/')
    def index(self):
        random_questions = Question.query.order_by(db.func.rand()).limit(20)
        return render_template('question/index.html',
                               random_questions=random_questions)

    @route(r'/<int:id>')
    def show(self, id):
        question = Question.query.filter(Question.id==int(id)).first_or_404()
        random_questions = Question.query.order_by(db.func.rand()).limit(20)
        return render_template('question/show.html', question=question,
                               random_questions=random_questions,
                               answer_form=AnswerForm())