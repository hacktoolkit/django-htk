# Python Standard Library Imports
from collections import namedtuple


# isort: off


def ensure_mysql_connection_usable():
    """Ensure that MySQL connection is usable

    From: http://stackoverflow.com/questions/7835272/django-operationalerror-2006-mysql-server-has-gone-away
    """
    from django.db import (
        connection,
        connections,
    )

    # MySQL is lazily connected to in Django.
    # connection.connection is None means
    # you have not connected to MySQL before
    if connection.connection and not connection.is_usable():
        # destroy the default MySQL connection
        # after this line, when you use ORM methods
        # Django will reconnect to the default MySQL
        #
        # Delete one database connection:
        # del connections._connections.default
        #
        # Delete all database connections
        databases = connections._connections.__dict__.keys()
        for database in databases:
            del connections._connections.__dict__[database]


def attempt_mysql_reconnect():
    """Attempt to reconnect to MySQL
    http://stackoverflow.com/a/29331237/865091
    """
    import MySQLdb

    conn = MySQLdb.Connect()
    conn.ping(True)


def close_connection():
    """Closes the connection if we are not in an atomic block.

    The connection should never be closed if we are in an atomic block, as
    happens when running tests as part of a django TestCase. Otherwise, closing
    the connection is important to avoid a connection time out after long actions.
    Django does not automatically refresh a connection which has been closed
    due to idleness (this normally happens in the request start/finish part
    of a webapp's lifecycle, which this process does not have), so we must
    do it ourselves if the connection goes idle due to stuff taking a really
    long time.

    source: http://stackoverflow.com/a/39322632/865091
    """
    from django.db import connection

    if not connection.in_atomic_block:
        connection.close()


def get_cursor(db_alias):
    """Returns a DB Cursor that can be used to issue raw SQL statements"""
    from django.db import connections

    cursor = connections[db_alias].cursor()
    return cursor


def raw_sql(statement, db_alias='default'):
    """Execute raw SQL `statement

    Returns the cursor to perform any subsequent queries
    """
    cursor = get_cursor(db_alias)
    cursor.execute(statement)
    return cursor


def disable_foreign_key_checks():
    """Disable foreign key constraint checks
    Useful for bulk data uploads

    https://stackoverflow.com/questions/15501673/how-to-temporarily-disable-a-foreign-key-constraint-in-mysql
    """
    raw_sql('SET FOREIGN_KEY_CHECKS=0;')


def enable_foreign_key_checks():
    """Enable foreign key constraint checks

    Ensure this is called after disable_foreign_key_checks()
    """
    raw_sql('SET FOREIGN_KEY_CHECKS=1;')


def namedtuplefetchall(cursor):
    """Return all rows from a cursor as a namedtuple

    https://docs.djangoproject.com/en/5.0/topics/db/sql/
    """
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]
