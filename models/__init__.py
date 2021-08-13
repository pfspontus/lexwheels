"""
Call create_db to setup database with tables

Example
    >>> import models

    To create the tables car and owner in the database
    >>> models.create_db()

    And fill it with mock data
    >>> models.fill_db_with_mocks()

    Query for a owner filled with owned cars
    >>> owner_id = 1
    >>> models.one_owner_with_cars(owner_id)
    Owner(id=1, name='Gwen Bartlomieczak',
          cars=[Car(id=84, owner_id=1, make='Dodge', model='Ram 1500', year=2007, owner=None)])
"""

from sqlalchemy import text

from flask_sqlalchemy import SQLAlchemy

from models import car
from models import owner


class Models:
    def __init__(self, app):
        "Interface to access lexwheels data"
        self.db = SQLAlchemy(app)
        self.Car = car.init(self.db)
        self.Owner = owner.init(self.db)

    def create_db(self):
        self.db.create_all()

    def drop_all(self):
        self.db.drop_all()

    def fill_db_with_mocks(self):
        with self.db.engine.connect() as conn:
            trans = conn.begin()
            for filename in ['owners.sql', 'cars.sql']:
                with open(f'mock_data/{filename}', 'rt') as fd:
                    for line in fd.readlines():
                        query = text(line)
                        conn.execute(query)
            trans.commit()

    def get_owner(self, owner_id):
        return self.Owner.query.filter_by(id=owner_id).first()

    def get_all_owners(self):
        return self.Owner.query.all()

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
