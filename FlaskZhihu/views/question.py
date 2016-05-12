# -*- coding: utf-8 -*-
__author__ = 'shn7798'

import random
import time
import os


from flask import abort, render_template, current_app, redirect, url_for

from flask.ext.classy import FlaskView, route
from flask.ext.login import login_required, current_user

from flask.ext.sqlalchemy_cache import FromCache, RelationshipCache
from flask.ext.sqlalchemy import get_debug_queries

from FlaskZhihu.models import *
from FlaskZhihu.helpers import cached
from FlaskZhihu.extensions import cache
from FlaskZhihu.forms import QuestionAddForm, QuestionEditForm
from FlaskZhihu.helpers import keep_next_url

from pprint import pprint

__all__ = ['QuestionView']



class QuestionView(FlaskView):
    route_base = '/question'

    def _random_questions(self, limit=20, max=None):
        if max is None:
            # max = Question.query.count() 会全表扫描
            max = db.session.query(db.func.count(Question.id)).first()[0]
        random.seed('%s%d' %(os.umask(24), time.time()))
        if max > limit:
            offset = random.randint(0, max - limit)
        else:
            offset = 0
        random_questions = Question.query.offset(offset).limit(limit)
        random_questions = sorted(random_questions, key=lambda x: x.answers_count, reverse=True)
        return random_questions

    @route(r'/')
    def index(self):
        random_questions = self._random_questions(20)
        return render_template('question/index.html',
                               random_questions=random_questions)


    @route(r'/<int:id>/')
    def show(self, id):
        question = Question.query.filter(Question.id == int(id)).first_or_404()
        # .join(Answer.user_id == User.id)\
        answers = Answer.query\
            .options(db.joinedload('user'))\
            .filter(Answer.question_id == int(question.id)) \
            .all()

        random_questions = self._random_questions(20)
        response = render_template('question/show.html',
                                   question=question, answers=answers,
                                   random_questions=random_questions)

        #pprint(get_debug_queries())
        #print len(get_debug_queries())

        return response

    @route(r'/add/', methods=['GET', 'POST'])
    @login_required
    def add(self):
        form = QuestionAddForm()
        if form.validate_on_submit():
            question = Question()
            question.user = current_user
            question.title = form.title.data
            question.content = form.content.data

            db.session.add(question)
            db.session.commit()

            return redirect(url_for('QuestionView:show', id=question.id))

        return render_template('question/add.html', form=form)

    @route(r'/my/')
    @login_required
    def my(self):
        assert current_user.id
        questions = Question.query.filter(Question.user_id == current_user.id).all()
        return render_template('question/my.html', questions=questions)

    @route(r'/<int:id>/edit/', methods=['GET', 'POST'])
    @login_required
    @keep_next_url
    def edit(self, id, next_url=None):
        print id
        question = Question.query.get_or_404(id)
        form = QuestionEditForm()
        if form.validate_on_submit():
            question.title = form.title.data
            question.content = form.content.data
            db.session.commit()
            return redirect(next_url or url_for('QuestionView:show', id=question.id))
        else:
            form.title.data = question.title
            form.content.data = question.content
            return render_template('question/edit.html', form=form)