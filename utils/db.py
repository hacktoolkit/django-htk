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
