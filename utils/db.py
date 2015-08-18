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
        del connections._connections.default
