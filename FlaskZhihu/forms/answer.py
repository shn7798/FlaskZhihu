# -*- coding: utf-8 -*-
__author__ = 'shn7798'

from flask.ext.wtf import Form
from wtforms import TextAreaField, SubmitField, HiddenField
from wtforms.validators import required


class AnswerForm(Form):
    question_id = HiddenField(validators=[required()])
    content = TextAreaField(validators=[required(message=u'请输入内容')])