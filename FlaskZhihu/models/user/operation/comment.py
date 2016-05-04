# -*- coding: utf-8 -*-
__author__ = 'shn7798'

class CommentOperationMixin(object):
    def voteup_comment(self, comment, undo=False):
        op = self.op_on_comment(comment, edit=True)
        if op.vote:
            if undo:
                op.vote = False
            else:
                pass
        else:
            op.vote = True

    def add_comment_reply(self, comment, reply):
        reply.quote_comment = comment

