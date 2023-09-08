import mysql.connector
from mysql.connector import Error

import psycopg2
from psycopg2 import OperationalError

def test_mysql_connection(host_name, user_name, user_password, port):
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            password=user_password,
            port=port
        )
        if connection.is_connected():
            connection.close()
            return True, f"Erfolgreich mit dem Server {host_name} auf Port {port} verbunden."
    except Error as e:
        return False, f"Der Fehler '{e}' trat auf."

def test_postgresql_connection(host_name, user_name, user_password, port):
    try:
        connection = psycopg2.connect(
            host=host_name,
            user=user_name,
            password=user_password,
            port=port,
            database="postgres"  # Verbinden Sie mit der Standard-Postgres-Datenbank
        )
        if connection:
            connection.close()
            return True, f"Erfolgreich mit dem Server {host_name} auf Port {port} verbunden."
    except OperationalError as e:
        return False, f"Der Fehler '{e}' trat auf."