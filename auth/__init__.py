"""
User authentication views
"""
import functools

from flask import Blueprint
from flask import g
from flask import redirect
from flask import request
from flask import url_for

from auth import views

define = views.define
auth_page = Blueprint('auth', __name__, url_prefix='/auth',
                      template_folder='templates')


def login_required(view):
    """
    Wrapper to decorate given view, enforcing authentication.
    """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login', next=request.url))

        return view(**kwargs)

    return wrapped_view
