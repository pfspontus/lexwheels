import os

from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap

from models import Models
from setup_config import setup_config


def create_app(testing=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET='dev'
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
    from api import api_page
    from api.views import define as api_views_define
    api_views_define(api_page, models)
    app.register_blueprint(api_page)

    @app.route('/')
    def welcome():
        owners = models.get_all_owners()
        return render_template('welcome.html', owners=owners)

    @app.route('/owner/<int:id>')
    def owner(id):
        owner = models.get_owner(id)
        return render_template('owner.html', owner=owner)

    return app
