from datos.conexion import obtener_conexion

def guardar_producto(nombre, precio):
    if not nombre or not precio:
        retur False
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO productos (nombre, precio) VALUES (%s, %s)", (nombre, precio))
    conexion.commit()
    conexion.close()
    return True

def listar_productos():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos")
    datos = cursor.fetchall()
    conexion.close()
    return datos
