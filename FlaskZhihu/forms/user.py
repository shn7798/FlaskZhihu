# -*- coding: utf-8 -*-
__author__ = 'shn7798'

from flask.ext.wtf import Form
from wtforms import TextAreaField, SubmitField, HiddenField, StringField
from wtforms.validators import required


class LoginForm(Form):
    username = StringField(validators=[required()])
    password = StringField(validators=[required()])
    next_url = HiddenField()