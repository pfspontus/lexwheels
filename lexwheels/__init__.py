"""
Lexwheels, a student project application about
cars and their owners.

Example
    $> flask init-db
    Initialized database

    $> flask fill-db
    Filled database with dummy data.

    $> flask run
"""
import os

from flask import Flask

from admin import admin_page
from admin import define as admin_views_define
from api import api_page
from api.views import define as api_views_define
from auth import auth_page
from auth import define as auth_views_define
from models import Models
from setup_config import setup_config

from lexwheels import views


def create_app():
    """
    Application factory, that instatiates the lexwheels app
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.urandom(24),
        SQLALCHEMY_ENGINE_OPTIONS={
            "pool_pre_ping": True,
            "pool_recycle": 300,
        }
    )

    setup_config(app)

    models = Models()
    models.init_app(app)

    auth_views_define(auth_page, models)
    app.register_blueprint(auth_page)

    api_views_define(api_page, models)
    app.register_blueprint(api_page)

    admin_views_define(admin_page, models)
    app.register_blueprint(admin_page)

    views.define(app, models)

    return app
