import mysql.connector
from mysql.connector import Error

import psycopg2
from psycopg2 import OperationalError

from pymongo import MongoClient
from pymongo.errors import PyMongoError

def test_mysql_connection(host_name, user_name, user_password, port):
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            password=user_password,
            port=port,
            connection_timeout=1
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
            database="postgres",  # Verbinden Sie mit der Standard-Postgres-Datenbank
            connect_timeout = 1
        )
        if connection:
            connection.close()
            return True, f"Erfolgreich mit dem Server {host_name} auf Port {port} verbunden."
    except OperationalError as e:
        return False, f"Der Fehler '{e}' trat auf."

def test_mongodb_connection(host_name, user_name, user_password, port):
    try:
        connection = MongoClient(
            host=host_name,
            port=port,
            username=user_name,
            password=user_password,
            serverSelectionTimeoutMS = 1000
        )
        # Der ismaster-Befehl wird verwendet, um eine Verbindung zum Server zu testen
        if connection.admin.command('ismaster'):
            connection.close()
            return True, f"Erfolgreich mit dem Server {host_name} auf Port {port} verbunden."
    except PyMongoError as e:
        return False, f"Der Fehler '{e}' trat auf."