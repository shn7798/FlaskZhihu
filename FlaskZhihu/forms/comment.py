# -*- coding: utf-8 -*-
__author__ = 'shn7798'

from flask.ext.wtf import Form
from wtforms import TextAreaField, SubmitField, HiddenField
from wtforms.validators import required, Regexp

__all__ = ['CommentAddForm']


class CommentAddForm(Form):
    target_type = HiddenField(validators=[required(message=u'请输入评论类型'),
                                          Regexp(r'^[a-z]+$')])
    target_id = HiddenField(validators=[required(message=u'请输入评论所属ID'),
                                        Regexp(r'^\d+$')])
    content = TextAreaField(validators=[required(message=u'请输入内容')])