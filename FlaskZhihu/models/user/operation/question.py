# -*- coding: utf-8 -*-
__author__ = 'shn7798'

class QuestionOperationMixin(object):
    def add_question(self, question):
        """ 创建问题 """
        question.user = self

    def add_question_answer(self, question, answer):
        """ 回答问题 """
        answer.user = self
        question.answers.append(answer)

    def add_question_comment(self, question, comment):
        """ 评论问题 """
        comment.user = self
        question.comments.append(comment)

    def follow_question(self, question):
        """ 关注问题 """
        op = self.op_on_question(question, edit=True)
        op.follow = True

    def unfollow_question(self, question):
        """ 取消关注问题 """
        op = self.op_on_question(question, edit=True)
        op.follow = False