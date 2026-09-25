# DICCIONARIO DE DATOS

## Sistema de Gestión Empresarial – Indumentaria OTNI Textil

El diccionario describe cada atributo de las entidades del modelo, indicando su tipo de dato, finalidad, clave, obligatoriedad, unicidad y las validaciones aplicables según las reglas de negocio.

---

## CLIENTE

| Campo        | Tipo de dato | Clave | Obligatorio | Único | Validación                           | Descripción                         |
| ------------ | ------------ | ----- | ----------- | ----- | ------------------------------------ | ----------------------------------- |
| `ID_Cliente` | INT          | PK    | Sí          | Sí    | Autoincremental                      | Identificador único del cliente.    |
| `Nombre`     | VARCHAR(50)  | —     | Sí          | No    | No puede estar vacío                 | Nombre del cliente.                 |
| `Apellido`   | VARCHAR(50)  | —     | Sí          | No    | No puede estar vacío                 | Apellido del cliente.               |
| `DNI`        | VARCHAR(20)  | —     | Sí          | Sí    | No puede repetirse                   | Documento de identidad del cliente. |
| `Telefono`   | VARCHAR(30)  | —     | No          | No    | —                                    | Número telefónico de contacto.      |
| `Email`      | VARCHAR(100) | —     | No          | No    | Formato de correo electrónico válido | Correo electrónico del cliente.     |
| `Direccion`  | VARCHAR(150) | —     | No          | No    | —                                    | Dirección del cliente.              |

---

## EMPLEADO

| Campo         | Tipo de dato | Clave | Obligatorio | Único | Validación                                         | Descripción                                            |
| ------------- | ------------ | ----- | ----------- | ----- | -------------------------------------------------- | ------------------------------------------------------ |
| `ID_Empleado` | INT          | PK    | Sí          | Sí    | Autoincremental                                    | Identificador único del empleado.                      |
| `Nombre`      | VARCHAR(50)  | —     | Sí          | No    | No puede estar vacío                               | Nombre del empleado.                                   |
| `Apellido`    | VARCHAR(50)  | —     | Sí          | No    | No puede estar vacío                               | Apellido del empleado.                                 |
| `Usuario`     | VARCHAR(50)  | —     | Sí          | Sí    | No puede repetirse                                 | Nombre de usuario utilizado para ingresar al sistema.  |
| `Contrasena`  | VARCHAR(255) | —     | Sí          | No    | No puede estar vacía                               | Contraseña asociada al usuario.                        |
| `Rol`         | VARCHAR(30)  | —     | Sí          | No    | Debe corresponder a un rol definido por el sistema | Rol o nivel de acceso del empleado dentro del sistema. |

---

## PRODUCTO

| Campo         | Tipo de dato  | Clave | Obligatorio | Único | Validación                 | Descripción                                 |
| ------------- | ------------- | ----- | ----------- | ----- | -------------------------- | ------------------------------------------- |
| `ID_Producto` | INT           | PK    | Sí          | Sí    | Autoincremental            | Identificador único del producto.           |
| `Nombre`      | VARCHAR(50)   | —     | Sí          | No    | No puede estar vacío       | Nombre del producto.                        |
| `Categoria`   | VARCHAR(50)   | —     | Sí          | No    | No puede estar vacía       | Categoría a la que pertenece el producto.   |
| `Talle`       | VARCHAR(10)   | —     | No          | No    | —                          | Talle o medida del producto.                |
| `Precio`      | DECIMAL(10,2) | —     | Sí          | No    | Debe ser mayor o igual a 0 | Precio de venta del producto.               |
| `Stock`       | INT           | —     | Sí          | No    | Debe ser mayor o igual a 0 | Cantidad de unidades disponibles.           |
| `Descripcion` | VARCHAR(255)  | —     | No          | No    | —                          | Descripción y características del producto. |

---

## VENTA

| Campo         | Tipo de dato  | Clave | Obligatorio | Único | Validación                                                           | Descripción                                   |
| ------------- | ------------- | ----- | ----------- | ----- | -------------------------------------------------------------------- | --------------------------------------------- |
| `ID_Venta`    | INT           | PK    | Sí          | Sí    | Autoincremental                                                      | Identificador único de la venta.              |
| `Fecha`       | DATE          | —     | Sí          | No    | Debe ser una fecha válida                                            | Fecha en la que se realizó la venta.          |
| `Total`       | DECIMAL(10,2) | —     | Sí          | No    | Debe ser mayor o igual a 0 y coincidir con la suma de los subtotales | Importe total correspondiente a la venta.     |
| `ID_Cliente`  | INT           | FK    | Sí          | No    | Debe corresponder a un cliente existente                             | Identifica al cliente asociado a la venta.    |
| `ID_Empleado` | INT           | FK    | Sí          | No    | Debe corresponder a un empleado existente                            | Identifica al empleado que registró la venta. |

### Relaciones de las FK

* `ID_Cliente` → `CLIENTE.ID_Cliente`
* `ID_Empleado` → `EMPLEADO.ID_Empleado`

---

## DETALLE_VENTA

| Campo             | Tipo de dato  | Clave | Obligatorio | Único | Validación                                                            | Descripción                                                     |
| ----------------- | ------------- | ----- | ----------- | ----- | --------------------------------------------------------------------- | --------------------------------------------------------------- |
| `ID_Detalle`      | INT           | PK    | Sí          | Sí    | Autoincremental                                                       | Identificador único del detalle de venta.                       |
| `Cantidad`        | INT           | —     | Sí          | No    | Debe ser mayor que 0                                                  | Cantidad de unidades del producto vendido.                      |
| `Precio_Unitario` | DECIMAL(10,2) | —     | Sí          | No    | Debe ser mayor o igual a 0                                            | Precio del producto al momento de realizar la venta.            |
| `Subtotal`        | DECIMAL(10,2) | —     | Sí          | No    | Debe ser mayor o igual a 0 y coincidir con Cantidad × Precio_Unitario | Importe correspondiente a la cantidad de unidades del producto. |
| `ID_Venta`        | INT           | FK    | Sí          | No    | Debe corresponder a una venta existente                               | Identifica la venta a la que pertenece el detalle.              |
| `ID_Producto`     | INT           | FK    | Sí          | No    | Debe corresponder a un producto existente                             | Identifica el producto incluido en el detalle.                  |

### Relaciones de las FK

* `ID_Venta` → `VENTA.ID_Venta`
* `ID_Producto` → `PRODUCTO.ID_Producto`

---

## Reglas de consistencia de importes

Los importes almacenados deben respetar las siguientes reglas:

* `Subtotal` se calcula como:

**Cantidad × Precio_Unitario**

* `Total` se calcula como la suma de los `Subtotal` correspondientes a una misma venta.

La aplicación debe calcular estos valores antes de almacenarlos y la base de datos debe impedir valores negativos mediante restricciones `CHECK`.

De esta manera se evita almacenar importes negativos y se mantiene la coherencia entre `Cantidad`, `Precio_Unitario`, `Subtotal` y `Total`.

---

## Referencias

* **PK:** Clave primaria. Identifica de manera única cada registro de una entidad.
* **FK:** Clave foránea. Permite establecer una relación entre una tabla y otra.
* **INT:** Número entero.
* **VARCHAR:** Cadena de caracteres de longitud variable.
* **DATE:** Fecha.
* **DECIMAL(10,2):** Número decimal con hasta 10 dígitos en total y 2 posiciones decimales.
* **Obligatorio:** El campo debe contener un valor y no puede quedar vacío.
* **Único:** El valor no puede repetirse entre los registros de la tabla.
* **Validación:** Regla que determina qué valores son aceptados para un atributo.
