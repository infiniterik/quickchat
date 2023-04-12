from flask import flash, redirect, url_for, session
from functools import wraps

def login_required(status=None):
    def login_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if 'user' in session and (status is None or status in session):
                return func(*args, **kwargs)
            else:
                flash("You are not logged in")
                return redirect(url_for("welcome"))
        return wrapper
    return login_decorator