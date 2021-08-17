from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for

admin_page = Blueprint('admin', __name__, url_prefix='/admin')


def define(auth_page, models):
    @admin_page.route('/admin', methods=('GET', 'POST'))
    def welcome():
        return render_template('admin/welcome.html')
