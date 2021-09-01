"""
Models holds the database session. It also
has accessor methods to handle needed data.

Initializing the database from a shell
    $> flask init-db
    Initialized database

    $> flask fill-db
    Filled database with dummy data.

Example for flask shell
    >>> import models
    >>> m = models.Models()

    Adding a Owner
    >>> owner = m.Owner(name='Bob')
    >>> owner.id
    >>> m.add_owner(owner)
    >>> owner.id
    1

    Query for a owner filled with owned cars
    >>> owner_id = 1
    >>> owner = m.get_owner(owner_id)
    >>> owner
    <Owner Bob>
    >>> owner.cars
    []
"""
from random import choice

import click
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_sqlalchemy import SQLAlchemy

from models import car
from models import owner
from models import user


class Models:
    """
    A front for accessing the database.
    """
    def __init__(self):
        self.db = SQLAlchemy()
        self.Car = car.init(self.db)
        self.Owner = owner.init(self.db)
        self.User = user.init(self.db)

    def init_app(self, app):
        """
        Initialize models with given app
        """
        self.db.init_app(app)
        app.cli.add_command(init_db_command)
        app.cli.add_command(fill_db_command)

    def fill_owners(self):
        """
        Helper method to fill database with dummy owners
        """
        s = self.db.session
        with open('mock_data/names.csv', 'rt') as fd:
            for name in fd.readlines():
                owner = self.Owner(name=name)
                s.add(owner)
        s.commit()

    def fill_cars(self):
        """
        Helper method to fill database with dummy cars
        """
        owners = self.get_all_owners()
        s = self.db.session
        with open('mock_data/cars.csv', 'rt') as fd:
            for line in fd.readlines():
                make, model, year = line.split(',')
                item = self.Car(make=make, model=model, year=year)
                choice(owners).cars.append(item)
        s.commit()

    def fill_db_with_mocks(self):
        """
        Helper method to fill database with dummy owners and cars.
        Also adds the admin user.
        """
        self.fill_owners()
        self.fill_cars()
        if not self.get_user_by_username('admin'):
            self.add_user('admin', 'admin')

    def add_user(self, username, password):
        """
        Given a username not in the database, and a given
        password, creates user.
        """
        if not self.get_user_by_username(username):
            pwhash = generate_password_hash(password)
            user = self.User(username=username, password=pwhash)
            s = self.db.session
            s.add(user)
            s.commit()

    def authenticate_user(self, user, password):
        """
        Authenticates given user against given password.
        """
        return check_password_hash(user.password, password)

    def get_user(self, user_id):
        """
        Retrieves user with given user_id
        """
        return self.User.query.filter_by(id=user_id).first()

    def get_user_by_username(self, username):
        """
        Retrieves user with given username
        """
        return self.User.query.filter_by(username=username).first()

    def add_owner(self, owner_obj):
        """
        Adds the given owner_obj to the database.
        """
        s = self.db.session
        s.add(owner_obj)
        s.commit()

    def commit(self):
        """
        Commits any changes to the database.
        """
        s = self.db.session
        s.commit()

    def get_owner(self, owner_id):
        """
        Retrieves owner with the given owner_id
        """
        return self.Owner.query.filter_by(id=owner_id).first()

    def get_owner_by_name(self, name):
        """
        Retrieves owner with the given name
        """
        return self.Owner.query.filter_by(name=name).first()

    def get_all_owners(self):
        """
        Retrieves all owners.
        """
        return self.Owner.query.order_by(self.Owner.name).all()

    def get_car(self, car_id):
        """
        Retrieves car with given car_id
        """
        return self.Car.query.filter_by(id=car_id).first()

    def get_all_cars(self):
        """
        Retrieves all cars
        """
        return self.Car.query.all()

    def delete_car(self, car_obj):
        """
        Deletes the given car_obj from the database.
        """
        s = self.db.session
        s.delete(car_obj)
        s.commit()

    def delete_owner(self, owner_obj):
        """
        Deletes the given owner_obj from the database.
        """
        s = self.db.session
        for car_obj in owner_obj.cars:
            s.delete(car_obj)
        s.delete(owner_obj)
        s.commit()


@click.command('init-db')
@with_appcontext
def init_db_command():
    """
    Initializes the database with the appropriate
    tables.
    """
    m = Models()
    m.db.drop_all()
    m.db.create_all()
    click.echo('Initialized the database')


@click.command('fill-db')
@with_appcontext
def fill_db_command():
    """
    Fills the database with dummy data for
    testing purposes.
    """
    m = Models()
    m.fill_db_with_mocks()
    click.echo('Fill database with dummy data')
