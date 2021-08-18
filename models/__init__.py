"""
Call create_db to setup database with tables

Example
    >>> from main import models

    To create the tables car and owner in the database
    >>> models.create_db()

    Adding a Owner
    >>> owner = models.Owner('Bob')
    >>> owner.id
    >>> models.add(owner)
    >>> owner.id
    1

    Query for a owner filled with owned cars
    >>> owner_id = 1
    >>> owner = models.get_owner(owner_id)
    >>> owner
    <Owner Bob>
    >>> owner.cars
    []
"""
from random import choice

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_sqlalchemy import SQLAlchemy

from models import car
from models import owner
from models import user


class Models:
    def __init__(self):
        "Interface to access lexwheels data"
        self.db = SQLAlchemy()
        self.Car = car.init(self.db)
        self.Owner = owner.init(self.db)
        self.User = user.init(self.db)

    def init_app(self, app):
        self.db.init_app(app)

    def create_db(self):
        self.db.create_all()
        self.db.session.commit()

    def drop_all(self):
        for o in self.get_all_owners():
            self.delete_owner(o)

    def fill_owners(self):
        s = self.db.session
        with open('mock_data/names.csv', 'rt') as fd:
            for name in fd.readlines():
                owner = self.Owner(name=name)
                s.add(owner)
        s.commit()

    def fill_cars(self):
        owners = self.get_all_owners()
        s = self.db.session
        with open('mock_data/cars.csv', 'rt') as fd:
            for line in fd.readlines():
                make, model, year = line.split(',')
                item = self.Car(make=make, model=model, year=year)
                choice(owners).cars.append(item)
        s.commit()

    def fill_db_with_mocks(self):
        self.fill_owners()
        self.fill_cars()
        if not self.get_user_by_username('admin'):
            self.add_user('admin', 'admin')

    def add_user(self, username, password):
        if not self.get_user_by_username(username):
            pwhash = generate_password_hash(password)
            user = self.User(username=username, password=pwhash)
            s = self.db.session
            s.add(user)
            s.commit()

    def authenticate_user(self, user, password):
        return check_password_hash(user.password, password)

    def get_user(self, user_id):
        return self.User.query.filter_by(id=user_id).first()

    def get_user_by_username(self, username):
        return self.User.query.filter_by(username=username).first()

    def add_owner(self, owner_obj):
        s = self.db.session
        s.add(owner_obj)
        s.commit()

    def commit(self):
        s = self.db.session
        s.commit()

    def get_owner(self, owner_id):
        return self.Owner.query.filter_by(id=owner_id).first()

    def get_owner_by_name(self, name):
        return self.Owner.query.filter_by(name=name).first()

    def get_all_owners(self):
        return self.Owner.query.order_by(self.Owner.name).all()

    def get_car(self, car_id):
        return self.Car.query.filter_by(id=car_id).first()

    def get_all_cars(self):
        return self.Car.query.all()

    def delete_car(self, car_obj):
        s = self.db.session
        s.delete(car_obj)
        s.commit()

    def delete_owner(self, owner_obj):
        s = self.db.session
        for car_obj in owner_obj.cars:
            s.delete(car_obj)
        s.delete(owner_obj)
        s.commit()
