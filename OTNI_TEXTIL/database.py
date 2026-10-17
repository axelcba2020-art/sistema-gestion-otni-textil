import mysql.connector
from db_config import DB_CONFIG


def obtener_conexion():
    return mysql.connector.connect(**DB_CONFIG)