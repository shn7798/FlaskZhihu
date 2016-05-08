# -*- coding: utf-8 -*-
__author__ = 'shn7798'

from flask.ext.wtf import Form
from wtforms import TextAreaField, SubmitField, HiddenField, StringField
from wtforms.validators import required, Regexp

__all__ = ['QuestionAddForm', 'QuestionEditForm']


class QuestionAddForm(Form):
    title = StringField(validators=[required(message=u'请输入标题')])
    content = TextAreaField(validators=[required(message=u'请输入内容')])

class QuestionEditForm(Form):
    title = StringField(validators=[required(message=u'请输入标题')])
    content = TextAreaField(validators=[required(message=u'请输入内容')])