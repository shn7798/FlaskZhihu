# -*- coding: utf-8 -*-
__author__ = 'shn7798'


class UserOperationMixin(object):
    def follow_user(self, user):
        op = self.op_on_user(user, edit=True)
        op.follow = True

    def unfollow_user(self, user):
        op = self.op_on_user(user, edit=True)
        op.follow = False

    def block_user(self, user):
        op = self.op_on_user(user, edit=True)
        op.follow = False
        op.block = True

    def unblock_user(self, user):
        op = self.op_on_user(user, edit=True)
        op.block = False

    def followed_users(self):
        return [op.dest_user for op in self.user_on_dest_user if op.follow]

    def who_followed_me(self):
        return [op.user for op in self.dest_user_on_user if op.follow]

    def blocked_users(self):
        return [op.dest_user for op in self.user_on_dest_user if op.block]

    def who_blocked_me(self):
        return [op.user for op in self.dest_user_on_user if op.block]

