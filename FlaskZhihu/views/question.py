# -*- coding: utf-8 -*-
__author__ = 'shn7798'


from flask.ext.classy import FlaskView, route
from flask import abort, render_template
import re

from FlaskZhihu.models.question import *
from FlaskZhihu.forms.answer import AnswerForm

class QuestionView(FlaskView):
    @route(r'/<id>')
    def get(self, id):
        print id
        if not re.compile(r'^\d+$').match(id):
            abort(404)
        question = Question.query.filter(Question.id==int(id)).first_or_404()
        random_questions = Question.query.order_by(db.func.rand()).limit(20)
        return render_template('question/index.html', question=question,
                               random_questions=random_questions,
                               answer_form=AnswerForm())