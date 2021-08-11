"""
Call create_db to setup database with tables
"""
import sqlite3

from models import cars
from models import owners

conn = sqlite3.connect('db/lexwheels.db')


def create_db():
    """
    Creates tables car and owner in the database.
    The database file is located in the db folder
    """
    try:
        cursor = conn.cursor()
        tables = [cars, owners]
        for table in tables:
            cursor.execute(table.create_table_sql())
    except sqlite3.Error as e:
        print('Error message:', e.args)


def fill_db_with_mocks():
    """
    Fills tables car and owner with mock data for testing purposes.
    """
    try:
        cursor = conn.cursor()
        tables = ['cars.sql', 'owners.sql']
        for filename in tables:
            with open(f'mock_data/{filename}', 'rt') as fd:
                for line in fd.readlines():
                    cursor.execute(line)
                conn.commit()
    except sqlite3.Error as e:
        print('Error message:', e.args)


def one_owner_with_cars(id: int) -> owners.Owner:
    """
    Gets owner associated with id. Fills the cars
    attribute with the cars owned.

    Returns a Owner namedtuple
    """
    owner = owners.one(conn, id)
    owner_cars = cars.with_owner(conn, owner)
    owner.cars.extend(owner_cars)
    return owner
