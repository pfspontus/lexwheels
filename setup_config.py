from os import environ


def setup_config(app):
    var_names = [
        ('SQLALCHEMY_TRACK_MODIFICATIONS', bool),
        ('SQLALCHEMY_DATABASE_URI', str),
    ]
    for name, cast_fun in var_names:
        app.config[name] = cast_fun(environ.get(name))
