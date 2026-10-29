-- OTNI TEXTIL - Modelo de Datos
-- Autora: Lorena Carballo - Rol: Modelo de Datos + Validaciones
DROP DATABASE IF EXISTS otni_textil;
CREATE DATABASE otni_textil;
USE otni_textil;

CREATE TABLE cliente (
  id_cliente INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  cuit_dni VARCHAR(11) NOT NULL UNIQUE,
  telefono VARCHAR(20),
  direccion VARCHAR(255)
);

CREATE TABLE producto (
  id_producto INT AUTO_INCREMENT PRIMARY KEY,
  codigo VARCHAR(20) NOT NULL UNIQUE,
  descripcion VARCHAR(150) NOT NULL,
  stock INT NOT NULL DEFAULT 0,
  precio_unitario FLOAT(10,2) NOT NULL
);

CREATE TABLE empleado (
  id_empleado INT AUTO_INCREMENT PRIMARY KEY,
  nombre_usuario VARCHAR(50) NOT NULL UNIQUE,
  rol ENUM('administrador','vendedor') NOT NULL,
  password_hash VARCHAR(255) NOT NULL
);

CREATE TABLE venta (
  id_venta INT AUTO_INCREMENT PRIMARY KEY,
  fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
  id_cliente INT NOT NULL,
  id_empleado INT NOT NULL,
  total DECIMAL(10,2) DEFAULT 0,
  FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente),
  FOREIGN KEY (id_empleado) REFERENCES empleado(id_empleado)
);

CREATE TABLE detalle_venta (
  id_detalle INT AUTO_INCREMENT PRIMARY KEY,
  id_venta INT NOT NULL,
  id_producto INT NOT NULL,
  cantidad INT NOT NULL,
  precio_unitario DECIMAL(10,2) NOT NULL,
  FOREIGN KEY (id_venta) REFERENCES venta(id_venta) ON DELETE CASCADE,
  FOREIGN KEY (id_producto) REFERENCES producto(id_producto)
);

-- Indices para busquedas frecuentes
CREATE INDEX idx_cliente_dni ON cliente(cuit_dni);
CREATE INDEX idx_producto_codigo ON producto(codigo);

-- Roles de seguridad
CREATE ROLE IF NOT EXISTS 'administrador_db', 'vendedor_db';
GRANT ALL PRIVILEGES ON otni_textil.* TO 'administrador_db';
GRANT SELECT ON otni_textil.cliente TO 'vendedor_db';
GRANT SELECT ON otni_textil.producto TO 'vendedor_db';
GRANT SELECT, INSERT ON otni_textil.venta TO 'vendedor_db';
GRANT SELECT, INSERT ON otni_textil.detalle_venta TO 'vendedor_db';

-- Datos de prueba
INSERT INTO cliente (nombre, cuit_dni, telefono, direccion) VALUES ('Juan Perez', '20304567891', '351-5551234', 'Colon 123');
INSERT INTO producto (codigo, descripcion, stock, precio_unitario) VALUES ('OTNI-001', 'Camisa trabajo L azul', 50, 25000);
INSERT INTO empleado (nombre_usuario, rol, password_hash) VALUES ('admin', 'administrador', 'hash123');
