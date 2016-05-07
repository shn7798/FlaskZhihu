# -*- coding: utf-8 -*-
__author__ = 'shn7798'

from flask import abort, render_template, redirect, request
from flask.ext.classy import FlaskView, route
from flask.ext.login import login_user, login_required, logout_user

from FlaskZhihu.models import User
from FlaskZhihu.forms.user import LoginForm

__all__ = ['UserView']

class UserView(FlaskView):
    route_base = '/user'

    @route('/login', methods=['GET', 'POST'])
    def login(self):
        form = LoginForm()
        if not form.next_url.data:
            form.next_url.data = request.args.get('next', None)

        if form.validate_on_submit():
            user = User.query.filter(User.username==form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)

                return redirect(form.next_url.data or '/')

        return render_template('user/login.html', form=form)


    @route('/logout')
    @login_required
    def logout(self):
        logout_user()
        return redirect(request.args.get('next') or '/')


    @route('/add')
    def add(self):
        pass

    @route('/edit')
    def edit(self):
        pass