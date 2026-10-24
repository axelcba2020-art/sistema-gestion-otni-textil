# conexion OTNI

import mysql.connector
from mysql.connector import Error

def obtener_conexion():
 try:
 conexion = mysql.connector.connect(
host="localhost",
database="otni_textil",
user="root",
password=""
 )
return conexion 
except Error as e:
print(f"Error: {e}")
return None

