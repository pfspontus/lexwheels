"""
Cars data
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


def some(conn, ids: tuple, opts=None) -> list:
    """
    Returns list of Car namedtuples, associated with given ids
    """
    return _execute(conn, some_sql(ids))


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
