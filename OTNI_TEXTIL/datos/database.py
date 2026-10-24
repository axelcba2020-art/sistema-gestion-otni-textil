from .conexion import obtener_conexion

def crear_tablas():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL
  )
  """)
  conexion.commit()
conexion.close()
