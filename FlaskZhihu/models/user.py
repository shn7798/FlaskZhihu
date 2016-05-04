# -*- coding: utf-8 -*-
__author__ = 'shn7798'

from FlaskZhihu.extensions import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column('id', db.Integer, primary_key=True)
    create_time = db.Column('create_time', db.DateTime)
    update_time = db.Column('update_time', db.DateTime)
    username = db.Column('username', db.String(45), primary_key=True, nullable=False, unique=True)
    password = db.Column('password', db.String(100), nullable=False)
    name = db.Column('name', db.String(45))
    gender = db.Column('gender', db.Integer)
    description = db.Column('description', db.String(200))
    headline = db.Column('headline', db.String(100))
    avatar_url = db.Column('avatar_url', db.String(200))
    voteup_count = db.Column('voteup_count', db.Integer)
    votedown_count = db.Column('votedown_count', db.Integer)

    answers = db.relationship(u'Answer', backref='user')
    collections = db.relationship(u'Collection', backref='user')
    comments = db.relationship(u'Comment', backref='user')
    questions = db.relationship(u'Question', backref='user')

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

    #op_on_users = db.relationship(u'User', secondary='user_on_user', backref='op_by_users')
    #user_on_user = db.relationship(u'UserOnUser', backref='user')

    @staticmethod
    def get_admin():
        return User.query.filter(User.id==1).first_or_404()


class UserOnAnswer(db.Model):
    __tablename__ = 'user_on_answer'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    answer_id = db.Column('answer_id', db.ForeignKey(u'answer.id'), nullable=False, index=True)
    user_id = db.Column('user_id', db.ForeignKey(u'user.id'), nullable=False, index=True)
    # TODO: 思考要不要在每个元素中添加author字段, 元素中已经包含author_id
    # 是否作者
    # author = db.Column('author', db.Integer)
    follow = db.Column('follow', db.Integer)
    thank = db.Column('thank', db.Integer)
    voteup = db.Column('voteup', db.Integer)
    votedown = db.Column('votedown', db.Integer)


class UserOnCollection(db.Model):
    __tablename__ = 'user_on_collection'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column('user_id', db.ForeignKey(u'user.id'), nullable=False, index=True)
    collection_id = db.Column('collection_id', db.ForeignKey(u'collection.id'), nullable=False, index=True)
    public = db.Column('public', db.Integer, server_default=db.text("'0'"))
    following = db.Column('following', db.Integer, server_default=db.text("'0'"))


class UserOnComment(db.Model):
    __tablename__ = 'user_on_comment'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column('user_id', db.ForeignKey(u'user.id'), nullable=False, index=True)
    comment_id = db.Column('comment_id', db.ForeignKey(u'comment.id'), nullable=False, index=True)
    voteup = db.Column('voteup', db.Integer)


class UserOnQuestion(db.Model):
    __tablename__ = 'user_on_question'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column('user_id', db.ForeignKey(u'user.id'), nullable=False, index=True)
    question_id = db.Column('question_id', db.ForeignKey(u'question.id'), nullable=False, index=True)
    follow = db.Column('follow', db.Integer)


class UserOnTopic(db.Model):
    __tablename__ = 'user_on_topic'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column('user_id', db.ForeignKey(u'user.id'), nullable=False, index=True)
    topic_id = db.Column('topic_id', db.ForeignKey(u'topic.id'), nullable=False, index=True)
    follow = db.Column('follow', db.Integer)


class UserOnUser(db.Model):
    __tablename__ = 'user_on_user'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column('user_id', db.ForeignKey(u'user.id'), nullable=False, index=True)
    dest_user_id = db.Column('dest_user_id', db.ForeignKey(u'user.id'), nullable=False, index=True)
    follow = db.Column('follow', db.Integer)
    block = db.Column('block', db.Integer)

    # dest_user = db.relationship(u'User', primaryjoin='UserOnUser.dest_user_id == User.id')
    # user = db.relationship(u'User', primaryjoin='UserOnUser.user_id == User.id')
