"""
Authentication views
"""
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for


def define(auth_page, models):
    """
    View functions and routes for the Authentication pages
    """

    @auth_page.route('/login', methods=('GET', 'POST'))
    def login():
        """
        Log in page
        """
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
                if request.form['next']:
                    return redirect(request.form['next'])
                return redirect(url_for('welcome'))

            flash(error)

        return render_template('login.html')

    @auth_page.route('/logout')
    def logout():
        """
        Log out page
        """
        session.clear()
        return redirect(url_for('welcome'))

    @auth_page.before_app_request
    def load_logged_in_user():
        """
        Load user when available in the session.
        """
        user_id = session.get('user_id')

        if user_id is None:
            g.user = None
        else:
            g.user = models.get_user(user_id)
