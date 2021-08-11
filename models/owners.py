"""
Owner data
"""
from collections import namedtuple

Owner = namedtuple('Owner', [
    'id',
    'name',
    'cars',
], defaults=([],))


def create_table_sql() -> str:
    """
    SQL query string to create the owner table.
    """
    return 'create table owner (id int, name varchar(100))'


def some_sql(ids: tuple) -> str:
    """
    SQL query string to select owners associated with given ids.
    """
    cols = 'owner.id, owner.name'
    query = f'select {cols} from owner where id in { ids }'
    return query


def some(conn, ids: tuple, opts=None) -> list:
    """
    Returns a list of Owner namedtuples associated with given ids.
    """
    return _execute(conn, some_sql(ids))


def one_sql(id: int) -> str:
    """
    SQL query string to select owner associated with given id.
    """
    cols = 'owner.id, owner.name'
    query = f'select {cols} from owner where owner.id={id}'
    return query


def one(conn, id: int, opts=None) -> Owner:
    """
    Returns one Owner namedtuple associated with the given id.
    """
    return _execute(conn, one_sql(id))[0]


def all_sql() -> str:
    """
    SQL query string to select owner associated with given id.
    """
    cols = 'owner.id, owner.name'
    query = f'select {cols} from owner'
    return query


def all(conn, opts=None) -> list:
    """
    Returns a list of Owner namedtuples, of all owners.
    """
    return _execute(conn, all_sql())


def _execute(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return [Owner(*row) for row in cursor.fetchall()]
