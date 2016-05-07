# -*- coding: utf-8 -*-
__author__ = 'shn7798'

from flask import session
from FlaskZhihu.extensions import cache
import functools

def cached(*cargs, **ckwargs):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return cache.cached(*cargs, unless=lambda: session.get('user_id', None) is not None, **ckwargs)(func)(*args, **kwargs)
        return wrapper
    return decorator
