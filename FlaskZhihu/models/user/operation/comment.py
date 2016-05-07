# -*- coding: utf-8 -*-
__author__ = 'shn7798'

from FlaskZhihu.constants import VOTE_UP, VOTE_DOWN, VOTE_NONE
class CommentOperationMixin(object):
    def voteup_comment(self, comment, undo=False):
        op = self.op_on_comment(comment, edit=True)
        if undo:
            if op.vote == VOTE_UP:
                op.vote = VOTE_NONE
        else:
            op.vote = VOTE_UP

    def add_comment_reply(self, comment, reply):
        reply.quote_comment = comment

