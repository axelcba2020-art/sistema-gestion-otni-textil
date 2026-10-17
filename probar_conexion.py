import mysql.connector
from mysql.connector import Error

try:
    conexion = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="otni_app",
        password="4533226",
        database="indumentaria_otni"
    )

    if conexion.is_connected():
        print("Conexion exitosa con OTNI Textil")

        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM Cliente")

        clientes = cursor.fetchall()

        print("\nClientes registrados:")
        for cliente in clientes:
            print(cliente)

        cursor.close()
        conexion.close()

except Error as error:
    print("Error al conectar con MySQL:", error)