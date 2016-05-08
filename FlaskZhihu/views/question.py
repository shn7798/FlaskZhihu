# -*- coding: utf-8 -*-
__author__ = 'shn7798'

import random

from flask import abort, render_template, current_app

from flask.ext.classy import FlaskView, route
from flask.ext.login import login_required

from flask.ext.sqlalchemy_cache import FromCache, RelationshipCache
from flask.ext.sqlalchemy import get_debug_queries

from FlaskZhihu.models import *
from FlaskZhihu.helpers import cached
from FlaskZhihu.extensions import cache
from pprint import pprint

__all__ = ['QuestionView']



class QuestionView(FlaskView):
    route_base = '/question'

    @route(r'/')
    def index(self):
        random_questions = Question.query.order_by(db.func.rand()).limit(20)
        return render_template('question/index.html',
                               random_questions=random_questions)


    @route(r'/<int:id>')
    def show(self, id):
        question = Question.query.filter(Question.id == int(id)).first_or_404()
        # .join(Answer.user_id == User.id)\
        answers = Answer.query\
            .options(db.joinedload('user'))\
            .filter(Answer.question_id == int(question.id)) \
            .all()

        limit = 20
        offset = random.randint(0, Question.query.count()-limit)
        random_questions = Question.query.offset(offset).limit(limit)
        random_questions = sorted(random_questions, key=lambda x:x.answers_count, reverse=True)
        response = render_template('question/show.html',
                                   question=question, answers=answers,
                                   random_questions=random_questions)

        pprint(get_debug_queries())
        print len(get_debug_queries())

        return response
