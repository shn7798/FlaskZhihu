# -*- coding: utf-8 -*-
__author__ = 'shn7798'

from flask import abort, render_template, current_app
from flask.blueprints import Blueprint
from flask.ext.classy import FlaskView, route
from flask.ext.login import login_required
from FlaskZhihu.caching_query import FromCache, RelationshipCache
from flask.ext.sqlalchemy import get_debug_queries

from FlaskZhihu.models import *
from FlaskZhihu.helpers import cached
from FlaskZhihu.extensions import cache
from pprint import pprint

__all__ = ['QuestionView']

question = Blueprint('question', __name__, url_prefix='/question')

class QuestionView(FlaskView):
    route_base = '/question'

    @route(r'/')
    def index(self):
        random_questions = Question.query.order_by(db.func.rand()).limit(20)
        return render_template('question/index.html',
                               random_questions=random_questions)


    @route(r'/<int:id>')
    # @cached(timeout=5)
    def show(self, id):
        question = Question.query.options(FromCache('hour')).filter(Question.id==int(id)).first_or_404()
        #random_questions = Question.query.order_by(db.func.rand()).limit(20)
        random_questions = Question.query.options(FromCache('hour')).limit(20)
        response = render_template('question/show.html', question=question,
                               random_questions=random_questions)
        print get_debug_queries()[-1]
        print len(get_debug_queries())

        return response

    @route(r'/2/<int:id>')
    # @cached(timeout=5)
    def show2(self, id):
        question = Question.query.filter(Question.id == int(id)).first_or_404()
        # random_questions = Question.query.order_by(db.func.rand()).limit(20)
        random_questions = Question.query.limit(20)
        response = render_template('question/show.html', question=question,
                               random_questions=random_questions)
        print get_debug_queries()[-1]
        print len(get_debug_queries())
        return response



@question.route(r'/<int:id>', endpoint='QuestionView:show')
# @cached(timeout=5)
def show(id):


    question = Question.query.options(FromCache('hour')).filter(Question.id==int(id)).first_or_404()
    answers = Answer.query.options(FromCache('hour')).filter(Answer.question_id==int(question.id)).all()
    #answers = question.answers
    print len(answers)
    #answers = Answer.query.filter(Answer.question_id==int(question.id)).all()
    #answers = Answer.query.options(FromCache(cache)).filter(Answer.question_id==int(question.id)).all()
    #random_questions = Question.query.order_by(db.func.rand()).limit(20)
    random_questions = Question.query.limit(20)
    response = render_template('question/show.html',
                               question=question, answers=answers,
                               random_questions=random_questions)

    pprint (get_debug_queries())
    print len(get_debug_queries())

    return response

@question.route(r'/2/<int:id>', endpoint='QuestionView:show2')
# @cached(timeout=5)
def show2(id):
    question = Question.query.filter(Question.id == int(id)).first_or_404()
    # random_questions = Question.query.order_by(db.func.rand()).limit(20)
    random_questions = Question.query.limit(20)
    response = render_template('question/show.html', question=question,
                           random_questions=random_questions)
    print get_debug_queries()[-1]
    print len(get_debug_queries())
    return response



def test1(id):
    question = Question.query.options(FromCache(cache)).filter(Question.id==int(id)).first_or_404()
    #random_questions = Question.query.order_by(db.func.rand()).limit(20)
    random_questions = Question.query.options(FromCache(cache)).limit(20)
    #response = render_template('question/show.html', question=question,
    #                       random_questions=random_questions)
    print get_debug_queries()[-1]
    print len(get_debug_queries())

    #return response

def test2(id):
    question = Question.query.filter(Question.id == int(id)).first_or_404()
    # random_questions = Question.query.order_by(db.func.rand()).limit(20)
    random_questions = Question.query.limit(20)
    #response = render_template('question/show.html', question=question,
    #                       random_questions=random_questions)
    print get_debug_queries()[-1]
    print len(get_debug_queries())

