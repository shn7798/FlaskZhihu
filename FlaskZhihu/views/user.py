# -*- coding: utf-8 -*-
__author__ = 'shn7798'

from flask import abort, render_template, redirect, request, url_for
from flask.ext.classy import FlaskView, route
from flask.ext.login import login_user, login_required, logout_user, current_user

from FlaskZhihu.models import User, Collection, UserOnCollection, Answer
from FlaskZhihu.forms import UserLoginForm, UserAddForm, UserEditForm
from FlaskZhihu.extensions import db, cache
from FlaskZhihu.helpers import keep_next_url
from FlaskZhihu.constants import FOLLOW_OFF, FOLLOW_ON
from FlaskZhihu import signals

__all__ = ['UserView']

class UserView(FlaskView):
    route_base = '/user'

    @route('/login/', methods=['GET', 'POST'])
    @keep_next_url
    def login(self, next_url=None):
        form = UserLoginForm()

        if form.validate_on_submit():
            user = User.query.filter(User.username==form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)

                return redirect(next_url or '/')

        return render_template('user/login.html', form=form)


    @route('/logout/')
    @login_required
    def logout(self):
        logout_user()
        return redirect(request.referrer or '/')


    @route('/add/', methods=['GET', 'POST'])
    @keep_next_url
    def add(self, next_url=None):
        if current_user.is_anonymous:
            form = UserAddForm()
            if form.validate_on_submit():
                if User.query.filter(User.username==form.username.data).count() == 0:
                    user = User()
                    user.name = form.name.data
                    user.username = form.username.data
                    user.password = form.password.data
                    db.session.add(user)
                    db.session.commit()
                    return redirect(url_for('UserView:login'))
            return render_template('user/add.html', form=form)
        else:
            return redirect(next_url or '/')

    @route('/edit/', methods=['GET', 'POST'])
    @login_required
    @keep_next_url
    def edit(self, next_url=None):
        form = UserEditForm()
        if form.validate_on_submit():
            user = current_user
            if form.name.data:
                user.name = form.name.data
            if form.password.data:
                user.password = form.password.data
            db.session.commit()
        # 不管有没有修改, 都返回上个页面
            return redirect(next_url or '/')
        else:
            if request.method.upper() == 'POST':
                return redirect(next_url or '/')
            else:
                return render_template('user/edit.html', form=form)


    @route('/collection/<int:id>/follow/')
    @login_required
    @keep_next_url
    def follow_collection(self, id, next_url=None):
        collection = Collection.query.get_or_404(id)
        current_user.follow_collection(collection)
        db.session.commit()

        signals.collection_follow.send(collection)
        return redirect(next_url or url_for('CollectionView:my'))


    @route('/collection/<int:id>/unfollow/')
    @login_required
    @keep_next_url
    def unfollow_collection(self, id, next_url=None):
        collection = Collection.query.get_or_404(id)
        current_user.unfollow_collection(collection)
        db.session.commit()

        signals.collection_unfollow.send(collection)
        return redirect(next_url or url_for('CollectionView:my'))

    @route('/my/')
    @login_required
    def my(self):
        return self.show(current_user.id)

    @route(r'/<int:id>/')
    def show(self, id):
        user = User.query.get_or_404(id)
        return render_template('user/show.html', user=user)

    @route(r'/answer/<int:answer_id>/thank/', methods=['GET', 'POST'])
    @login_required
    @keep_next_url
    def thank_answer(self, answer_id, next_url=None):
        answer = Answer.query.get_or_404(answer_id)
        current_user.thank_answer(answer)
        db.session.commit()

        signals.answer_thank.send(answer)
        return redirect(next_url or url_for('AnswerView:show', id=answer_id))

    @route(r'/answer/<int:answer_id>/unthank/', methods=['GET', 'POST'])
    @login_required
    @keep_next_url
    def unthank_answer(self, answer_id, next_url=None):
        answer = Answer.query.get_or_404(answer_id)
        current_user.unthank_answer(answer)

        db.session.commit()

        signals.answer_unthank.send(answer)
        return redirect(next_url or url_for('AnswerView:show', id=answer_id))

