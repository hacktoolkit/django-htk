def ensure_mysql_connection_usable():
    """Ensure that MySQL connection is usable

    From: http://stackoverflow.com/questions/7835272/django-operationalerror-2006-mysql-server-has-gone-away
    """
    from django.db import connection, connections
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
