# DICCIONARIO DE DATOS

## Sistema de Gestión Empresarial – Indumentaria OTNI Textil

El diccionario describe cada atributo de las entidades del modelo, indicando su tipo de dato, finalidad y si corresponde a una clave primaria o foránea.

---

## CLIENTE

| Campo        | Tipo de dato | Clave | Descripción                         |
| ------------ | ------------ | ----- | ----------------------------------- |
| `ID_Cliente` | INT          | PK    | Identificador único del cliente.    |
| `Nombre`     | VARCHAR(50)  | —     | Nombre del cliente.                 |
| `Apellido`   | VARCHAR(50)  | —     | Apellido del cliente.               |
| `DNI`        | VARCHAR(20)  | —     | Documento de identidad del cliente. |
| `Telefono`   | VARCHAR(30)  | —     | Número telefónico de contacto.      |
| `Email`      | VARCHAR(100) | —     | Correo electrónico del cliente.     |
| `Direccion`  | VARCHAR(150) | —     | Dirección del cliente.              |

---

## EMPLEADO

| Campo         | Tipo de dato | Clave | Descripción                                            |
| ------------- | ------------ | ----- | ------------------------------------------------------ |
| `ID_Empleado` | INT          | PK    | Identificador único del empleado.                      |
| `Nombre`      | VARCHAR(50)  | —     | Nombre del empleado.                                   |
| `Apellido`    | VARCHAR(50)  | —     | Apellido del empleado.                                 |
| `Usuario`     | VARCHAR(50)  | —     | Nombre de usuario utilizado para ingresar al sistema.  |
| `Contraseña`  | VARCHAR(255) | —     | Contraseña asociada al usuario.                        |
| `Rol`         | VARCHAR(30)  | —     | Rol o nivel de acceso del empleado dentro del sistema. |

---

## PRODUCTO

| Campo         | Tipo de dato  | Clave | Descripción                                 |
| ------------- | ------------- | ----- | ------------------------------------------- |
| `ID_Producto` | INT           | PK    | Identificador único del producto.           |
| `Nombre`      | VARCHAR(50)   | —     | Nombre del producto.                        |
| `Categoria`   | VARCHAR(50)   | —     | Categoría a la que pertenece el producto.   |
| `Talle`       | VARCHAR(10)   | —     | Talle o medida del producto.                |
| `Precio`      | DECIMAL(10,2) | —     | Precio de venta del producto.               |
| `Stock`       | INT           | —     | Cantidad de unidades disponibles.           |
| `Descripcion` | VARCHAR(255)  | —     | Descripción y características del producto. |

---

## VENTA

| Campo         | Tipo de dato  | Clave | Descripción                                   |
| ------------- | ------------- | ----- | --------------------------------------------- |
| `ID_Venta`    | INT           | PK    | Identificador único de la venta.              |
| `Fecha`       | DATE          | —     | Fecha en la que se realizó la venta.          |
| `Total`       | DECIMAL(10,2) | —     | Importe total correspondiente a la venta.     |
| `ID_Cliente`  | INT           | FK    | Identifica al cliente asociado a la venta.    |
| `ID_Empleado` | INT           | FK    | Identifica al empleado que registró la venta. |

### Relaciones de las FK

* `ID_Cliente` → `CLIENTE.ID_Cliente`
* `ID_Empleado` → `EMPLEADO.ID_Empleado`

---

## DETALLE_VENTA

| Campo             | Tipo de dato  | Clave | Descripción                                                     |
| ----------------- | ------------- | ----- | --------------------------------------------------------------- |
| `ID_Detalle`      | INT           | PK    | Identificador único del detalle de venta.                       |
| `Cantidad`        | INT           | —     | Cantidad de unidades del producto vendido.                      |
| `Precio_Unitario` | DECIMAL(10,2) | —     | Precio del producto al momento de realizar la venta.            |
| `Subtotal`        | DECIMAL(10,2) | —     | Importe correspondiente a la cantidad de unidades del producto. |
| `ID_Venta`        | INT           | FK    | Identifica la venta a la que pertenece el detalle.              |
| `ID_Producto`     | INT           | FK    | Identifica el producto incluido en el detalle.                  |

### Relaciones de las FK

* `ID_Venta` → `VENTA.ID_Venta`
* `ID_Producto` → `PRODUCTO.ID_Producto`

---

## Referencias

* **PK:** Clave primaria. Identifica de manera única cada registro de una entidad.
* **FK:** Clave foránea. Permite establecer una relación entre una tabla y otra.
* **INT:** Número entero.
* **VARCHAR:** Cadena de caracteres de longitud variable.
* **DATE:** Fecha.
* **DECIMAL(10,2):** Número decimal con hasta 10 dígitos en total y 2 posiciones decimales.

## Nota sobre valores calculados

`Subtotal` puede obtenerse mediante:

**Cantidad × Precio_Unitario**

y `Total` puede obtenerse sumando los subtotales correspondientes a una venta.

En este proyecto ambos campos se mantienen almacenados para conservar la coherencia entre el modelo, el diccionario de datos, el DDL y las pantallas del sistema.
