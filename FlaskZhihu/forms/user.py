# -*- coding: utf-8 -*-
__author__ = 'shn7798'

from flask.ext.wtf import Form
from wtforms import TextAreaField, SubmitField, HiddenField, StringField
from wtforms.validators import required

__all__ = ['UserLoginForm', 'UserAddForm', 'UserEditForm']

class UserLoginForm(Form):
    username = StringField(validators=[required()])
    password = StringField(validators=[required()])
    next_url = HiddenField()


class UserAddForm(Form):
    name = StringField(validators=[required()])
    username = StringField(validators=[required()])
    password = StringField(validators=[required()])


class UserEditForm(Form):
    name = StringField(validators=[])
    password = StringField(validators=[])