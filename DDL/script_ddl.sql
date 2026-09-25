-- ============================================================
-- SCRIPT DDL
-- Sistema de Gestión Empresarial
-- Indumentaria OTNI Textil
-- Compatible con MySQL/MariaDB
-- ============================================================

CREATE DATABASE IF NOT EXISTS indumentaria_otni;

USE indumentaria_otni;


-- ============================================================
-- TABLA: CLIENTE
-- ============================================================

CREATE TABLE Cliente (
    ID_Cliente INT AUTO_INCREMENT,
    Nombre VARCHAR(50) NOT NULL,
    Apellido VARCHAR(50) NOT NULL,
    DNI VARCHAR(20) NOT NULL,
    Telefono VARCHAR(30),
    Email VARCHAR(100),
    Direccion VARCHAR(150),

    CONSTRAINT PK_Cliente
        PRIMARY KEY (ID_Cliente),

    CONSTRAINT UQ_Cliente_DNI
        UNIQUE (DNI)
);


-- ============================================================
-- TABLA: EMPLEADO
-- ============================================================

CREATE TABLE Empleado (
    ID_Empleado INT AUTO_INCREMENT,
    Nombre VARCHAR(50) NOT NULL,
    Apellido VARCHAR(50) NOT NULL,
    Usuario VARCHAR(50) NOT NULL,
    Contrasena VARCHAR(255) NOT NULL,
    Rol VARCHAR(30) NOT NULL,

    CONSTRAINT PK_Empleado
        PRIMARY KEY (ID_Empleado),

    CONSTRAINT UQ_Empleado_Usuario
        UNIQUE (Usuario)
);


-- ============================================================
-- TABLA: PRODUCTO
-- ============================================================

CREATE TABLE Producto (
    ID_Producto INT AUTO_INCREMENT,
    Nombre VARCHAR(50) NOT NULL,
    Categoria VARCHAR(50) NOT NULL,
    Talle VARCHAR(10),
    Precio DECIMAL(10,2) NOT NULL,
    Stock INT NOT NULL,
    Descripcion VARCHAR(255),

    CONSTRAINT PK_Producto
        PRIMARY KEY (ID_Producto),

    CONSTRAINT CK_Producto_Precio
        CHECK (Precio >= 0),

    CONSTRAINT CK_Producto_Stock
        CHECK (Stock >= 0)
);


-- ============================================================
-- TABLA: VENTA
-- ============================================================

CREATE TABLE Venta (
    ID_Venta INT AUTO_INCREMENT,
    Fecha DATE NOT NULL,
    Total DECIMAL(10,2) NOT NULL,
    ID_Cliente INT NOT NULL,
    ID_Empleado INT NOT NULL,

    CONSTRAINT PK_Venta
        PRIMARY KEY (ID_Venta),

    CONSTRAINT CK_Venta_Total
        CHECK (Total >= 0),

    CONSTRAINT FK_Venta_Cliente
        FOREIGN KEY (ID_Cliente)
        REFERENCES Cliente(ID_Cliente),

    CONSTRAINT FK_Venta_Empleado
        FOREIGN KEY (ID_Empleado)
        REFERENCES Empleado(ID_Empleado)
);


-- ============================================================
-- TABLA: DETALLE_VENTA
-- ============================================================

CREATE TABLE Detalle_Venta (
    ID_Detalle INT AUTO_INCREMENT,
    Cantidad INT NOT NULL,
    Precio_Unitario DECIMAL(10,2) NOT NULL,
    Subtotal DECIMAL(10,2) NOT NULL,
    ID_Venta INT NOT NULL,
    ID_Producto INT NOT NULL,

    CONSTRAINT PK_Detalle_Venta
        PRIMARY KEY (ID_Detalle),

    CONSTRAINT CK_Detalle_Cantidad
        CHECK (Cantidad > 0),

    CONSTRAINT CK_Detalle_Precio
        CHECK (Precio_Unitario >= 0),

    CONSTRAINT CK_Detalle_Subtotal
        CHECK (Subtotal >= 0),

    CONSTRAINT FK_Detalle_Venta
        FOREIGN KEY (ID_Venta)
        REFERENCES Venta(ID_Venta),

    CONSTRAINT FK_Detalle_Producto
        FOREIGN KEY (ID_Producto)
        REFERENCES Producto(ID_Producto)
);


-- ============================================================
-- REGLAS DE CONSISTENCIA DE IMPORTES
-- ============================================================
--
-- Subtotal = Cantidad * Precio_Unitario
--
-- Total = suma de los Subtotal correspondientes a una venta.
--
-- Estos valores son calculados por la aplicación antes de
-- almacenarse. Las restricciones CHECK de la base de datos
-- impiden almacenar valores negativos.
--
-- De esta manera se mantiene la coherencia de los importes
-- almacenados en TOTAL y SUBTOTAL.
-- ============================================================