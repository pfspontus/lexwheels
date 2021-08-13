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
