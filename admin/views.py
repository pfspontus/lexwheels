"""
Admin views
"""

from flask import abort
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from auth import login_required


def define(admin_page, models):
    """
    View functions and routes for the Admin pages
    """

    @admin_page.route('/')
    @login_required
    def admin():
        """
        Main admin landing page
        """
        owners = models.get_all_owners()
        n = 5
        owners = [owners[i:i + n] for i in range(0, len(owners), n)]
        return render_template('admin.html', owners=owners)

    @admin_page.route('/owner/<int:id>')
    @login_required
    def owner(id):
        """
        Owner details page
        """
        owner = models.get_owner(id)
        if not owner:
            return abort(404)
        owner.cars.sort(key=lambda c: (c.year, c.make, c.model))
        return render_template('owner.html', owner=owner)

    @admin_page.route('/add_owner', methods=('GET', 'POST'))
    @login_required
    def add_owner():
        """
        Add new owner page
        """
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

        return render_template('add_owner.html')

    @admin_page.route('/owner/<int:id>/append_car', methods=('GET', 'POST'))
    @login_required
    def append_car(id):
        """
        Append new car to given owner
        """
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
        if not owner:
            return abort(404)
        return render_template('append_car.html', owner=owner)

    @admin_page.route('/edit_owner/<int:id>', methods=('GET', 'POST'))
    @login_required
    def edit_owner(id):
        """
        Change given owner information
        """
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
        if not owner:
            return abort(404)
        return render_template('edit_owner.html', owner=owner)

    @admin_page.route('/edit_car/<int:id>', methods=('GET', 'POST'))
    @login_required
    def edit_car(id):
        """
        Change given car information
        """
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
        if not car:
            return abort(404)
        owner = car.owner
        return render_template('edit_car.html', owner=owner, car=car)

    @admin_page.route('/delete_owner/<int:id>', methods=('GET',))
    @login_required
    def delete_owner(id):
        """
        Delete owner
        """
        owner = models.get_owner(id)
        if owner:
            models.delete_owner(owner)
            return redirect(url_for('admin.admin'))
        return abort(404)

    @admin_page.route('/delete_car/<int:id>', methods=('GET',))
    @login_required
    def delete_car(id):
        """
        Delete given car
        """
        car = models.get_car(id)
        owner = models.get_owner(car.owner_id)
        if car:
            models.delete_car(car)
            return redirect(url_for('admin.owner', id=owner.id))
        return abort(404)
