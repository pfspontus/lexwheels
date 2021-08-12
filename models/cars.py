"""
Cars data

Example
    >>> from models import conn
    >>> from models import cars
    >>> ids = (1, 2)
    >>> cars.some(conn, ids)
    [Car(id=1, owner_id=37, make='Mazda', model='Protege', year=1997, owner=None),
     Car(id=2, owner_id=32, make='Acura', model='MDX', year=2002, owner=None)]
"""
from collections import namedtuple

Car = namedtuple('Car', [
    'id',
    'owner_id',
    'make',
    'model',
    'year',
    'owner',
], defaults=(None,))


def with_owner_sql(owner) -> str:
    """
    SQL query string that selects all cars associated with the given owner.
    """
    cols = 'car.id, car.owner_id, car.make, car.model, car.year'
    constraint = f'car.owner_id={ owner.id }'
    query = f'select {cols} from car where { constraint }'
    return query


def with_owner(conn, owner) -> list:
    """
    Returns list of Car namedtuples, associated with given owner.
    """
    return _execute(conn, with_owner_sql(owner))


def create_table_sql() -> str:
    """
    SQL query string to create car table.
    """
    cols = '(id int not null, owner_id int, make varchar(100), model varchar(100), year int)'
    return f'create table car {cols}'


def some_sql(ids: tuple) -> str:
    """
    SQL query string to select given car ids
    """
    cols = 'car.id, car.owner_id, car.make, car.model, car.year'
    query = f'select {cols} from car where car.id in {tuple(ids)}'
    return query

def one_sql(id: int) -> str:
    """
    SQL query string to select given car ids
    """
    cols = 'car.id, car.owner_id, car.make, car.model, car.year'
    query = f'select {cols} from car where car.id in {id}'
    return query


def some(conn, ids: tuple, opts=None) -> list:
    """
    Returns list of Car namedtuples, associated with given ids
    """
    return _execute(conn, some_sql(ids))


def one(conn, id: int, opts=None) -> list:
    """
    Returns list of Car namedtuples, associated with given ids
    """
    return _execute(conn, one_sql(id))


def all_sql() -> str:
    """
    SQL query string to select all cars
    """
    cols = 'car.id, car.owner_id, car.make, car.model, car.year'
    query = f'select {cols} from car'
    return query


def all(conn, opts=None) -> list:
    """
    Returns list of all Car namedtuples.
    """
    return _execute(conn, all_sql())


def _execute(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return [Car(*row) for row in cursor.fetchall()]
