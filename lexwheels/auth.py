import functools

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for

auth_page = Blueprint('auth', __name__, url_prefix='/auth')


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


def define(auth_page, models):
    @auth_page.route('/login', methods=('GET', 'POST'))
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = models.get_user_by_username(username)

            error = None
            if user is None:
                error = 'Incorrect username.'
            elif not models.authenticate_user(user, password):
                error = 'Incorrect password.'

            if error is None:
                session.clear()
                session['user_id'] = user.id
                return redirect(url_for('welcome'))

            flash(error)

        return render_template('auth/login.html')

    @auth_page.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('welcome'))

    @auth_page.before_app_request
    def load_logged_in_user():
        user_id = session.get('user_id')

        if user_id is None:
            g.user = None
        else:
            g.user = models.get_user(user_id)
