from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for

from lexwheels.auth import login_required

admin_page = Blueprint('admin', __name__, url_prefix='/admin')


def define(auth_page, models):
    @admin_page.route('/', methods=('GET', 'POST'))
    @login_required
    def welcome():
        owners = models.get_all_owners()
        return render_template('admin/welcome.html', owners=owners)

    @admin_page.route('/owner/<int:id>', methods=('GET', 'POST'))
    @login_required
    def owner(id):
        owner = models.get_owner(id)
        return render_template('admin/owner.html', owner=owner)
