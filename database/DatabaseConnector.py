import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()
host = os.getenv('HOST')
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')
database = os.getenv('DATABASE')


def connect_to_mysql():
    try:
        connection = mysql.connector.connect(
            host=host,
            user=username,
            password=password,
            database=database
        )
        print("Connected to MySQL database")
        return connection
    except mysql.connector.Error as err:
        print("Error connecting to MySQL database:", err)
        return None


def disconnect_from_mysql(connection):
    if connection:
        connection.close()
        print("Disconnected from MySQL database")
    else:
        print("Connection is null")
