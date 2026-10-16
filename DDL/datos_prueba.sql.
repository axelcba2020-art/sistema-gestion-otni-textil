-- Datos de prueba para OTNI Textil

-- 1. Insertar Empleados
INSERT INTO empleado (nombre_usuario, rol, password_hash) VALUES 
('admin_otni', 'Administrador', 'hash_seguro_1'),
('vendedor1', 'Empleado', 'hash_seguro_2');

-- 2. Insertar Clientes
INSERT INTO cliente (nombre, cuit_dni, telefono, direccion) VALUES 
('Constructora del Centro S.A.', '30-71234567-8', '3514223344', 'Av. Colón 1200, Córdoba'),
('Talleres Metalúrgicos Sur', '20-28111222-3', '3515667788', 'Bv. San Juan 450, Córdoba');

-- 3. Insertar Productos (Indumentaria y seguridad)
INSERT INTO producto (codigo, descripcion, stock, precio_unitario) VALUES 
('PROD-001', 'Camisa de Grafa con Reflectivo Talle L', 50, 18500.00),
('PROD-002', 'Pantalón de Seguridad Industrial Talle 42', 40, 22000.00),
('PROD-003', 'Botines de Seguridad con Puntera de Acero', 25, 45000.00);

-- 4. Insertar Ventas de ejemplo
INSERT INTO venta (fecha, id_cliente, id_empleado, total) VALUES 
('2026-10-01', 1, 1, 62500.00);

-- 5. Insertar Detalle de Venta
INSERT INTO detalle_venta (id_venta, id_producto, cantidad, precio_unitario) VALUES 
(1, 1, 1, 18500.00),
(1, 2, 2, 22000.00);
