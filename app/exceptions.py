

class DatabaseUnavailable(Exception):
    """Raised when the DBCM cannot create a connection"""

class ConnectionTimeout(Exception):
    """Raised when a timeout occurs while waiting to acquire a free conneciton from the DBCM"""