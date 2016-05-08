# -*- coding: utf-8 -*-
__author__ = 'shn7798'

from flask import session, request
import blinker
from FlaskZhihu.extensions import cache
import functools

def cached(*cargs, **ckwargs):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return cache.cached(*cargs, unless=lambda: session.get('user_id', None) is not None, **ckwargs)(func)(*args, **kwargs)
        return wrapper
    return decorator


def keep_next_url(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        next_url = request.args.get('next')
        if not next_url:
            if request and request.method in ("PUT", "POST"):
                next_url = request.form.get('next')
        return func(*args, next_url=next_url, **kwargs)
    return wrapper


def use_signal(signal):
    assert isinstance(signal, blinker.NamedSignal)

    def decorator(func):
        signal.connect(func)
        return func
    return decorator
