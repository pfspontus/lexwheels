from flask import abort
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
    @admin_page.route('/')
    @login_required
    def welcome():
        owners = models.get_all_owners()
        return render_template('admin/welcome.html', owners=owners)

    @admin_page.route('/owner/<int:id>', methods=('GET', 'POST'))
    @login_required
    def owner(id):
        owner = models.get_owner(id)
        return render_template('admin/owner.html', owner=owner)

    @admin_page.route('/add_owner', methods=('GET', 'POST'))
    @login_required
    def add_owner():
        if request.method == 'POST':
            owner_name = request.form['name']
            error = None

            if models.get_owner_by_name(owner_name):
                error = 'Owner exists'

            if error is None:
                owner = models.Owner()
                owner.name = owner_name
                models.add_owner(owner)
                return redirect(url_for('admin.owner', id=owner.id))

            flash(error)

        return render_template('admin/add_owner.html')

    @admin_page.route('/delete_owner/<int:id>')
    @login_required
    def delete_owner(id):
        owner = models.get_owner(id)
        if owner:
            models.delete_owner(owner)
            return redirect(url_for('admin.welcome'))
        return abort(404)

    @admin_page.route('/delete_car/<int:id>')
    @login_required
    def delete_car(id):
        car = models.get_car(id)
        owner = models.get_owner(car.owner_id)
        if car:
            models.delete_car(car)
            return redirect(url_for('admin.owner', id=owner.id))
        return abort(404)
