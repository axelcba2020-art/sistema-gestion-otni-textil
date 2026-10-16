# Sistema de Gestión Empresarial – Indumentaria OTNI Textil

Proyecto de base de datos para un sistema de gestión empresarial destinado a Indumentaria OTNI Textil.

## Contenido

- `Modelo_ER/`: modelo entidad-relación normalizado.
- `Diccionario/`: diccionario de datos de las entidades y sus atributos.
- `DDL/`: script SQL para crear la base de datos y sus tablas.

## Entidades

El modelo está compuesto por:

1. Cliente
2. Empleado
3. Producto
4. Venta
5. Detalle_venta

## Relaciones principales

- Un cliente puede tener muchas ventas.
- Un empleado puede registrar muchas ventas.
- Una venta puede contener muchos detalles de venta.
- Un producto puede aparecer en muchos detalles de venta.

## Tecnologías

- Modelo E-R
- SQL
- MySQL/MariaDB
- ##  Instalación y Ejecución

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/axelcba2020-art/sistema-gestion-otni-textil.git](https://github.com/axelcba2020-art/sistema-gestion-otni-textil.git)
