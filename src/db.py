import mysql.connector
from mysql.connector.connection import MySQLConnection


def get_connection(
    host: str = "localhost",
    port: int = 3306,
    user: str = "root",
    password: str = "root",
    database: str = "airlines",
) -> MySQLConnection:
    """Create and return a MySQL database connection.

    Args:
        host: MySQL server host.
        port: MySQL server port.
        user: MySQL username.
        password: MySQL password.
        database: Target database name.

    Returns:
        An active MySQLConnection instance.
    """
    return mysql.connector.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
    )