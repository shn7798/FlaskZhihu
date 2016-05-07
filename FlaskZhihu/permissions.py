# -*- coding: utf-8 -*-
__author__ = 'shn7798'

from flask.ext.principal import Permission, RoleNeed
from flask.ext.login import LoginManager
from FlaskZhihu.models import User

admin = Permission(RoleNeed('admin'))
auth = Permission(RoleNeed('authenticated'))

login_manager = LoginManager()
login_manager.login_view = 'UserView:login'

@login_manager.user_loader
def user_loader(user_id):
    if not user_id:
        return None
    try:
        return User.find_by_id(user_id, abort404=True)
    except Exception as e:
        print e
        return None