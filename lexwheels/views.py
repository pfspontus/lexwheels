from flask import abort
from flask import render_template


def define(app, models):
    @app.route('/')
    def welcome():
        return render_template('welcome.html')

    @app.route('/owners')
    def owners():
        owners = models.get_all_owners()
        n = 4
        owners = [owners[i:i + n] for i in range(0, len(owners), n)]
        return render_template('owners.html', owners=owners)

    @app.route('/owner/<int:id>')
    def owner(id):
        owner = models.get_owner(id)
        if not owner:
            return abort(404)
        owner.cars.sort(key=lambda c: (c.year, c.make, c.model))
        return render_template('owner.html', owner=owner)
