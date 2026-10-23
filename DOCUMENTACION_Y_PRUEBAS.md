# MÓDULO DE DOCUMENTACIÓN Y PRUEBAS - OTNI TEXTIL

**Integrante responsable:** Gabriela del Hoyo  
**Proyecto:** Sistema de Gestión de Datos - OTNI Textil (Indumentaria de trabajo y accesorios de seguridad)  
**Institución:** Instituto Superior Politécnico Córdoba (ISPC)  

---

## 1. INFORME DEL SISTEMA
El sistema desarrollado centraliza la información de la microempresa familiar OTNI Textil, resolviendo los problemas de desactualización y duplicación de datos entre stock, ventas y clientes. Permite una gestión rápida y segura mediante los roles de **Administrador** y **Empleado/Vendedor**, cuyas pantallas e interfaces fueron diseñadas de forma intuitiva en Python (Tkinter).

## 2. MANUAL DE USUARIO RÁPIDO

### 🔹 Acceso al Sistema
1. Al iniciar la aplicación, aparecerá la **Pantalla de Inicio** de sesión.
2. Ingrese su **Usuario** y **Contraseña** asignados.
3. Presione el botón **INGRESAR** para acceder al Panel Principal según sus permisos de rol.

### 🔹 Módulos Principales (Panel Principal)
* **Stock / Productos:** Permite visualizar el listado de indumentaria y accesorios, buscar por código o nombre, y registrar nuevos artículos mediante el botón `[+ Nuevo producto]`.
* **Clientes:** Gestiona la base de datos de compradores, permitiendo registrar nuevos clientes (`[+ Nuevo cliente]`), modificar sus datos o eliminarlos.
* **Ventas:** Muestra el registro de operaciones, permitiendo asociar un cliente, buscar los productos vendidos, calcular subtotales y registrar la venta total.
* **Reportes:** Ofrece estadísticas visuales del mes (total vendido, cantidad de productos vendidos y clientes nuevos).
* **Empleados / Usuarios (Solo Administrador):** Permite administrar a los usuarios del sistema, sus roles de seguridad y credenciales.

---

## 3. PLAN Y CASOS DE PRUEBAS REALIZADAS

Se realizaron pruebas sistemáticas sobre cada módulo del sistema para garantizar la integridad de los datos y el funcionamiento correcto de las conexiones a la base de datos:

1. **Prueba de Autenticación:** Verificación de ingreso correcto con credenciales de Administrador y Vendedor, bloqueando accesos no autorizados.
2. **Prueba de Registro de Productos:** Comprobación de que al rellenar los campos de un nuevo producto (nombre, categoría, talle, precio y stock), este se guarde correctamente en la base de datos y se refleje en el listado.
3. **Prueba de Validaciones:** Control de que el sistema rechace campos vacíos o formatos incorrectos en clientes y productos.
4. **Prueba de Stock y Ventas:** Verificación de que al registrar una venta, los subtotales se calculen de manera exacta y el stock del producto disminuya acorde a la cantidad vendida.
# MÓDULO DE DOCUMENTACIÓN Y PRUEBAS - OTNI TEXTIL

**Integrante responsable:** Gabriela del Hoyo
**Proyecto:** Sistema de Gestión de Datos - OTNI Textil (Indumentaria de trabajo y accesorios de seguridad)
**Institución:** Instituto Superior Politécnico Córdoba (ISPC)

---

## 1. INFORME DEL SISTEMA
El sistema desarrollado centraliza la información de la microempresa familiar OTNI Textil, resolviendo problemas de desactualización y duplicación de datos entre stock, ventas y clientes. Permite una gestión rápida y segura mediante roles de **Administrador** y **Empleado/Vendedor**, cuyas pantallas e interfaces fueron diseñadas de forma clara en Python (Tkinter).

---

## 2. MANUAL DE USUARIO RÁPIDO

### 🔹 Acceso al Sistema
1. Al iniciar la aplicación, aparecerá la **Pantalla de Inicio** de sesión.
2. Ingrese su **Usuario** y **Contraseña** asignados.
3. Presione el botón **INGRESAR** para acceder al Panel Principal según sus permisos de rol.

### 🔹 Módulos Principales (Panel Principal)
* **Stock / Productos:** Permite visualizar el listado de indumentaria y accesorios, buscar por código o nombre y registrar nuevos artículos mediante el botón `[+ Nuevo producto]`.
* **Clientes:** Gestiona la base de datos de compradores, permitiendo registrar nuevos clientes, modificar sus datos o eliminarlos.
* **Ventas:** Muestra el registro de operaciones, permitiendo asociar un cliente, buscar los productos vendidos, calcular subtotales y registrar la venta total.
* **Reportes:** Ofrece estadísticas visuales del mes (total vendido, cantidad de productos vendidos y clientes más activos).
* **Empleados / Usuarios (Solo Administrador):** Permite administrar a los usuarios del sistema, sus roles y sus credenciales.

---

## 3. PLAN Y CASOS DE PRUEBAS REALIZADAS

Se realizaron pruebas sistemáticas sobre cada módulo del sistema para garantizar la integridad de los datos y el funcionamiento correcto de las conexiones a la base de datos:

1. **Prueba de Autenticación:** Verificación de ingreso correcto con credenciales de Administrador/Empleado y bloqueo de accesos no autorizados.
2. **Prueba de Registro de Productos:** Comprobación de que al rellenar los campos de un nuevo producto (categoría, talle, precio y stock), este se guarde correctamente en la base de datos y se refleje en el listado.
3. **Prueba de Validaciones:** Control de que el sistema rechace campos vacíos o formatos incorrectos.
4. **Prueba de Stock y Ventas:** Verificación de que al registrar una venta, los subtotales se calculen bien y el stock del producto disminuya acorde a la cantidad vendida.

### Resumen de Resultados
| ID | Caso de Prueba | Módulo Evaluado | Resultado Esperado | Estado |
|---|---|---|---|---|
| CP-01 | Autenticación y Roles | Login y Permisos | Acceso correcto según rol asignado | ✅ APROBADO |
| CP-02 | Gestión de Productos | Stock / Catálogo | Persistencia en Base de Datos SQLite | ✅ APROBADO |
| CP-03 | Validaciones de Formulario | Entradas de Texto | Bloqueo de campos vacíos/inválidos | ✅ APROBADO |
| CP-04 | Descuento de Stock | Ventas y Carrito | Actualización automática del inventario | ✅ APROBADO |
