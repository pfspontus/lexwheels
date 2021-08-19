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

    @admin_page.route('/owner/<int:id>')
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

    @admin_page.route('/owner/<int:id>/append_car', methods=('GET', 'POST'))
    @login_required
    def append_car(id):
        if request.method == 'POST':
            owner = models.get_owner(id)
            error = None

            if not owner:
                error = 'Owner exists'

            if error is None:
                make = request.form['make']
                model = request.form['model']
                year = request.form['year']
                car = models.Car(make=make, model=model, year=year)
                owner.cars.append(car)
                models.commit()
                return redirect(url_for('admin.owner', id=owner.id))

            flash(error)

        owner = models.get_owner(id)
        return render_template('admin/append_car.html', owner=owner)

    @admin_page.route('/edit_owner/<int:id>', methods=('GET', 'POST'))
    @login_required
    def edit_owner(id):
        if request.method == 'POST':
            new_name = request.form['name']
            error = None

            owner = models.get_owner(id)
            existing_owner_with_name = models.get_owner_by_name(new_name)
            if existing_owner_with_name:
                error = 'Owner exists with the given name'

            if error is None:
                owner.name = new_name
                models.commit()
                return redirect(url_for('admin.owner', id=owner.id))

            flash(error)

        owner = models.get_owner(id)
        return render_template('admin/edit_owner.html', owner=owner)

    @admin_page.route('/edit_car/<int:id>', methods=('GET', 'POST'))
    @login_required
    def edit_car(id):
        if request.method == 'POST':
            error = None
            car = models.get_car(id)
            if not car:
                error = 'Car not found'

            if error is None:
                car.make = request.form['make']
                car.model = request.form['model']
                car.year = request.form['year']
                models.commit()
                return redirect(url_for('admin.owner', id=car.owner_id))

            flash(error)

        car = models.get_car(id)
        owner = car.owner
        return render_template('admin/edit_car.html', owner=owner, car=car)

    @admin_page.route('/delete_owner/<int:id>', methods=('GET',))
    @login_required
    def delete_owner(id):
        owner = models.get_owner(id)
        if owner:
            models.delete_owner(owner)
            return redirect(url_for('admin.welcome'))
        return abort(404)

    @admin_page.route('/delete_car/<int:id>', methods=('GET',))
    @login_required
    def delete_car(id):
        car = models.get_car(id)
        owner = models.get_owner(car.owner_id)
        if car:
            models.delete_car(car)
            return redirect(url_for('admin.owner', id=owner.id))
        return abort(404)
