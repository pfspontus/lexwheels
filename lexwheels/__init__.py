import os

from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap

from models import Models
from setup_config import setup_config


def create_app(testing=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.urandom(24),
        SQLALCHEMY_ENGINE_OPTIONS={
            "pool_pre_ping": True,
            "pool_recycle": 300,
        }
    )

    if testing:
        app.config.from_mapping(testing)
    else:
        setup_config(app)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    models = Models()
    models.init_app(app)
    Bootstrap(app)

    from lexwheels.auth import auth_page
    from lexwheels.auth import define as auth_views_define
    from lexwheels.auth import login_required
    auth_views_define(auth_page, models)
    app.register_blueprint(auth_page)

    from api import api_page
    from api.views import define as api_views_define
    api_views_define(api_page, models)
    app.register_blueprint(api_page)

    from lexwheels.admin import admin_page
    from lexwheels.admin import define as admin_views_define
    admin_views_define(admin_page, models)
    app.register_blueprint(admin_page)

    @app.route('/')
    def welcome():
        owners = models.get_all_owners()
        return render_template('welcome.html', owners=owners)

    @app.route('/owners')
    def owners():
        owners = models.get_all_owners()
        return render_template('owners.html', owners=owners)

    @app.route('/owner/<int:id>')
    @login_required
    def owner(id):
        owner = models.get_owner(id)
        owner.cars.sort(key=lambda c: (c.year, c.make, c.model))
        return render_template('owner.html', owner=owner)

    return app
