#! encoding=utf-8
from functools import update_wrapper
from flask import g, abort
from flask.ext.login import login_required


def access_control(name):
    def decorator(func):
        @login_required
        def wrapped_function(*args, **kwargs):
            if not g.user.can_visit(name):
                abort(403)
            return func(*args, **kwargs)
        return update_wrapper(wrapped_function, func)
    return decorator

