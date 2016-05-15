# -*- coding: utf-8 -*-
__author__ = 'shn7798'

from FlaskZhihu.extensions import db
from FlaskZhihu.models.base import DateTimeMixin, FindByIdMixin
from .operation import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.sqlalchemy_cache import CachingQuery


class UserOnUser(DateTimeMixin, FindByIdMixin, db.Model):
    __tablename__ = 'user_on_user'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column('user_id', db.ForeignKey(u'user.id'), nullable=False, index=True)
    dest_user_id = db.Column('dest_user_id', db.ForeignKey(u'user.id'), nullable=False, index=True)
    follow = db.Column('follow', db.Integer)
    block = db.Column('block', db.Integer)


class UserLoginMixin():
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id


class User(
    UserOperationMixin, QuestionOperationMixin, AnswerOperationMixin, CollectionOperationMixin,
    CommentOperationMixin,
    DateTimeMixin, FindByIdMixin,
    UserLoginMixin,
    db.Model):

    __tablename__ = 'user'
    query_class = CachingQuery

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    user_hashid = db.Column('user_hashid', db.String(32))
    username = db.Column('username', db.String(45), unique=True)
    name = db.Column('name', db.String(45))
    gender = db.Column('gender', db.Integer)
    description = db.Column('description', db.String(2048))
    headline = db.Column('headline', db.String(200))
    avatar_url = db.Column('avatar_url', db.String(200))

    # count cache
    voteup_count = db.Column('voteup_count', db.Integer, server_default='0')
    votedown_count = db.Column('votedown_count', db.Integer, server_default='0')
    thanks_count = db.Column('thanks_count', db.Integer, server_default='0')

    answers = db.relationship(u'Answer', backref='user')
    collections = db.relationship(u'Collection', backref='user')
    comments = db.relationship(u'Comment', backref='user')
    questions = db.relationship(u'Question', backref='user')

    _password = db.Column('password', db.String(100), nullable=False)

    def _set_password(self, password):
        self._password = generate_password_hash(password)

    def _get_password(self):
        return self._password

    password = db.synonym("_password",
                          descriptor=property(_get_password,
                                              _set_password))

    op_on_answers = db.relationship(u'Answer', secondary='user_on_answer', backref='op_by_users')
    user_on_answer = db.relationship(u'UserOnAnswer', backref='user')

    op_on_collections = db.relationship(u'Collection', secondary='user_on_collection', backref='op_by_users')
    user_on_collection = db.relationship(u'UserOnCollection', backref='user')

    op_on_comments = db.relationship(u'Comment', secondary='user_on_comment', backref='op_by_users')
    user_on_comment = db.relationship(u'UserOnComment', backref='user')

    op_on_questions = db.relationship(u'Question', secondary='user_on_question', backref='op_by_users')
    user_on_question = db.relationship(u'UserOnQuestion', backref='user')

    op_on_topics = db.relationship(u'Topic', secondary='user_on_topic', backref='op_by_users')
    user_on_topic = db.relationship(u'UserOnTopic', backref='user')

    op_on_users = db.relationship(u'User', secondary='user_on_user',
                                  primaryjoin=id==UserOnUser.user_id,
                                  secondaryjoin=id==UserOnUser.dest_user_id,
                                  backref='op_by_users')

    user_on_dest_user = db.relationship(u'UserOnUser', foreign_keys=[UserOnUser.user_id], backref='user')
    dest_user_on_user = db.relationship(u'UserOnUser', foreign_keys=[UserOnUser.dest_user_id], backref='dest_user')

    @staticmethod
    def get_admin(cls):
        return User.query.filter(User.id==1).first_or_404()

    @staticmethod
    def get_user_by_hashid(hashid):
        return User.query.filter(User.user_hashid==hashid).first()

    def check_password(self, password):
        assert self._get_password()
        return check_password_hash(self._get_password(), password)

    def op_on_answer(self, answer, edit=False):
        return self._op_on_x(answer, UserOnAnswer, edit=edit)

    def op_on_collection(self, collection, edit=False):
        return self._op_on_x(collection, UserOnCollection, edit=edit)

    def op_on_comment(self, comment, edit=False):
        return self._op_on_x(comment, UserOnComment, edit=edit)

    def op_on_question(self, question, edit=False):
        return self._op_on_x(question, UserOnQuestion, edit=edit)

    def op_on_topic(self, topic, edit=False):
        return self._op_on_x(topic, UserOnTopic, edit=edit)

    def op_on_user(self, user, edit=False):
        return self._op_on_x(user, UserOnUser, op_fk=UserOnUser.dest_user_id, one_to_many=self.op_on_users, edit=edit)

    def _op_on_x(self, x_obj, op_table, op_fk=None, one_to_many=None, edit=False):
        x_name = x_obj.__class__.__name__
        if not op_fk:
            op_fk_name = '%s_id' % x_name.lower()
            op_fk = getattr(op_table, op_fk_name)
        if not one_to_many:
            one_to_many_name = 'op_on_%ss' % x_name.lower()
            one_to_many = getattr(self, one_to_many_name)

        op = op_table.query.filter(
            db.and_(op_table.user_id == self.id, op_fk == x_obj.id)
        ).first()
        if not op:
            if edit:
                one_to_many.append(x_obj)
                return self._op_on_x(x_obj, op_table, op_fk=op_fk, one_to_many=one_to_many)
            else:
                return None
        else:
            return op

    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self.username)


class UserOnAnswer(DateTimeMixin, FindByIdMixin, db.Model):
    __tablename__ = 'user_on_answer'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    answer_id = db.Column('answer_id', db.ForeignKey(u'answer.id'), nullable=False, index=True)
    user_id = db.Column('user_id', db.ForeignKey(u'user.id'), nullable=False, index=True)
    follow = db.Column('follow', db.Integer)
    thank = db.Column('thank', db.Integer)
    vote = db.Column('vote', db.Integer)


class UserOnCollection(DateTimeMixin, FindByIdMixin, db.Model):
    __tablename__ = 'user_on_collection'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column('user_id', db.ForeignKey(u'user.id'), nullable=False, index=True)
    collection_id = db.Column('collection_id', db.ForeignKey(u'collection.id'), nullable=False, index=True)
    public = db.Column('public', db.Integer, server_default=db.text("'0'"))
    follow = db.Column('follow', db.Integer, server_default=db.text("'0'"))


class UserOnComment(DateTimeMixin, FindByIdMixin, db.Model):
    __tablename__ = 'user_on_comment'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column('user_id', db.ForeignKey(u'user.id'), nullable=False, index=True)
    comment_id = db.Column('comment_id', db.ForeignKey(u'comment.id'), nullable=False, index=True)
    vote = db.Column('vote', db.Integer)


class UserOnQuestion(DateTimeMixin, FindByIdMixin, db.Model):
    __tablename__ = 'user_on_question'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column('user_id', db.ForeignKey(u'user.id'), nullable=False, index=True)
    question_id = db.Column('question_id', db.ForeignKey(u'question.id'), nullable=False, index=True)
    follow = db.Column('follow', db.Integer)


class UserOnTopic(DateTimeMixin, FindByIdMixin, db.Model):
    __tablename__ = 'user_on_topic'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column('user_id', db.ForeignKey(u'user.id'), nullable=False, index=True)
    topic_id = db.Column('topic_id', db.ForeignKey(u'topic.id'), nullable=False, index=True)
    follow = db.Column('follow', db.Integer)

