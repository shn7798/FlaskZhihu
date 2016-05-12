# -*- coding: utf-8 -*-
__author__ = 'shn7798'

from flask.ext.wtf import Form
from wtforms import TextAreaField, SubmitField, HiddenField, StringField
from wtforms.validators import required, Regexp

class CollectionAddForm(Form):
    title = StringField(validators=[required()])
    description = StringField(validators=[required()])


class CollectionEditForm(Form):
    title = StringField()
    description = StringField()