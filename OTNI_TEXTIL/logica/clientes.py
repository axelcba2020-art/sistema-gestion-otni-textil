from datos.conexion import obtener_conexion

def guardar_cliente(nombre):
    if not nombre:
        return False
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO clientes (nombre) VALUES (%s)", (nombre,))
    conexion.commit()
    conexion.close()
    return True

def listar_clientes():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM clientes")
    datos = cursor.fetchall()
    conexion.close()
    return datos
