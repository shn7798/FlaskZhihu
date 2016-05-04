# -*- coding: utf-8 -*-
__author__ = 'shn7798'

from FlaskZhihu.constants import VOTE_NONE, VOTE_UP, VOTE_DOWN

class AnswerOperationMixin(object):
    def add_answer(self, answer):
        """ 创建回答 """
        answer.user = self

    def add_answer_comment(self, answer, comment):
        """ 评论回答 """
        comment.user = self
        answer.comments.append(comment)

    def voteup_answer(self, answer, undo=False):
        op = self.op_on_answer(answer, edit=True)

        if op.vote == VOTE_UP:
            if undo:
                op.vote = VOTE_NONE
            else:
                pass
        elif op.vote == VOTE_DOWN:
            op.vote = VOTE_UP
        else:
            op.vote = VOTE_UP

    def votedown_answer(self, answer, undo=False):
        op = self.op_on_answer(answer, edit=True)
        if op.vote == VOTE_DOWN:
            if undo:
                op.vote = VOTE_NONE
            else:
                pass
        elif op.vote == VOTE_UP:
            op.vote = VOTE_DOWN
        else:
            op.vote = VOTE_DOWN

    def thank_answer(self, answer):
        op = self.op_on_answer(answer, edit=True)
        op.thank = True

    def unthank_answer(self, answer):
        op = self.op_on_answer(answer, edit=True)
        op.thank = False