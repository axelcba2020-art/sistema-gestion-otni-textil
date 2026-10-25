from conexion import obtener_conexion
def crear_tablas():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    # 1. Crear tabla de clientes (que ya tenías)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL
    )
    """)
    
    # 2. Crear tabla de empleados/usuarios si no existe
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Empleado (
        id INT AUTO_INCREMENT PRIMARY KEY,
        Nombre VARCHAR(100) NOT NULL,
        Apellido VARCHAR(100) NOT NULL,
        Usuario VARCHAR(50) NOT NULL UNIQUE,
        Contrasena VARCHAR(50) NOT NULL,
        Rol VARCHAR(50) NOT NULL
    )
    """)
    
    # 3. Insertar un usuario administrador por defecto (admin / 1234)
    try:
        cursor.execute("""
        INSERT INTO Empleado (Nombre, Apellido, Usuario, Contrasena, Rol) 
        VALUES ('Administrador', 'Sistema', 'admin', '1234', 'Admin')
        """)
    except Exception as e:
        print("El usuario ya existe o ya fue creado anteriormente.")

    conexion.commit()
    conexion.close()

if __name__ == "__main__":
    crear_tablas()
    print("¡Base de datos y usuario creados con éxito!")
