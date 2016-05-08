# -*- coding: utf-8 -*-
__author__ = 'shn7798'

from flask import abort, render_template, redirect, request, url_for
from flask.ext.classy import FlaskView, route
from flask.ext.login import login_user, login_required, logout_user, current_user

from FlaskZhihu.models import User
from FlaskZhihu.forms import UserLoginForm, UserAddForm, UserEditForm
from FlaskZhihu.extensions import db, cache

__all__ = ['UserView']

class UserView(FlaskView):
    route_base = '/user'

    @route('/login', methods=['GET', 'POST'])
    def login(self):
        form = UserLoginForm()
        if not form.next_url.data:
            form.next_url.data = request.args.get('next', None)

        if form.validate_on_submit():
            user = User.query.filter(User.username==form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)

                return redirect(form.next_url.data or request.referrer or '/')

        return render_template('user/login.html', form=form)


    @route('/logout')
    @login_required
    def logout(self):
        logout_user()
        return redirect(request.referrer or '/')


    @route('/add', methods=['GET', 'POST'])
    def add(self):
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
            return redirect(request.referrer or '/')

    @route('/edit', methods=['GET', 'POST'])
    @login_required
    def edit(self):
        form = UserEditForm()
        if form.validate_on_submit():
            user = current_user
            if form.name.data:
                user.name = form.name.data
            if form.password.data:
                user.password = form.password.data
            db.session.commit()
        # 不管有没有修改, 都返回上个页面
            return redirect(request.referrer or '/')
        else:
            if request.method.upper() == 'POST':
                return redirect(request.referrer or '/')
            else:
                return render_template('user/edit.html', form=form)

