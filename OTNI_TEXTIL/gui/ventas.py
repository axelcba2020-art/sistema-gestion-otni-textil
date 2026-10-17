import tkinter as tk
from tkinter import ttk, messagebox
from decimal import Decimal, InvalidOperation

from database import obtener_conexion
from mysql.connector import Error


class VentasFrame(ttk.Frame):
    def __init__(
        self,
        master,
        clientes=None,
        productos=None,
        ventas=None,
        usuario_actual=None
    ):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        self.usuario_actual = usuario_actual or {}

        self.carrito = []
        self.clientes_por_opcion = {}
        self.productos_por_opcion = {}

        self._crear_interfaz()
        self._cargar_datos()
        self._cargar_ventas()

    def _crear_interfaz(self):
        encabezado = ttk.Frame(self)
        encabezado.pack(fill="x", padx=16, pady=(16, 8))

        ttk.Label(
            encabezado,
            text="Registrar venta",
            font=("Arial", 15, "bold")
        ).pack(side="left")

        seleccion = ttk.LabelFrame(
            self,
            text="Datos de la venta",
            padding=12
        )
        seleccion.pack(fill="x", padx=16, pady=8)

        ttk.Label(seleccion, text="Cliente:").grid(
            row=0, column=0, sticky="w", padx=(0, 8), pady=6
        )

        self.cliente_var = tk.StringVar()
        self.combo_cliente = ttk.Combobox(
            seleccion,
            textvariable=self.cliente_var,
            state="readonly",
            width=32
        )
        self.combo_cliente.grid(
            row=0, column=1, sticky="w", padx=(0, 20), pady=6
        )

        ttk.Label(seleccion, text="Producto:").grid(
            row=1, column=0, sticky="w", padx=(0, 8), pady=6
        )

        self.producto_var = tk.StringVar()
        self.combo_producto = ttk.Combobox(
            seleccion,
            textvariable=self.producto_var,
            state="readonly",
            width=32
        )
        self.combo_producto.grid(
            row=1, column=1, sticky="w", padx=(0, 20), pady=6
        )
        self.combo_producto.bind(
            "<<ComboboxSelected>>",
            self._mostrar_stock_disponible
        )

        ttk.Label(seleccion, text="Cantidad:").grid(
            row=2, column=0, sticky="w", padx=(0, 8), pady=6
        )

        self.cantidad_var = tk.StringVar(value="1")

        ttk.Spinbox(
            seleccion,
            from_=1,
            to=9999,
            textvariable=self.cantidad_var,
            width=10
        ).grid(row=2, column=1, sticky="w", pady=6)

        self.lbl_disponible = ttk.Label(
            seleccion,
            text="Stock disponible: -"
        )
        self.lbl_disponible.grid(
            row=3, column=1, sticky="w", pady=4
        )

        ttk.Button(
            seleccion,
            text="Agregar al carrito",
            cursor="hand2",
            command=self._agregar_al_carrito
        ).grid(
            row=4, column=0, columnspan=2, sticky="w", pady=(10, 0)
        )

        marco_carrito = ttk.LabelFrame(
            self,
            text="Productos de la venta",
            padding=8
        )
        marco_carrito.pack(
            fill="both", expand=True, padx=16, pady=8
        )

        columnas = (
            "PRODUCTO",
            "CANTIDAD",
            "PRECIO UNITARIO",
            "SUBTOTAL"
        )

        self.tabla_carrito = ttk.Treeview(
            marco_carrito,
            columns=columnas,
            show="headings",
            height=5,
            selectmode="browse"
        )
        self.tabla_carrito.pack(fill="both", expand=True)

        anchos = {
            "PRODUCTO": 250,
            "CANTIDAD": 90,
            "PRECIO UNITARIO": 140,
            "SUBTOTAL": 140
        }

        for columna in columnas:
            self.tabla_carrito.heading(columna, text=columna)
            self.tabla_carrito.column(
                columna,
                width=anchos[columna],
                anchor="center"
            )

        pie_carrito = ttk.Frame(marco_carrito)
        pie_carrito.pack(fill="x", pady=(8, 0))

        ttk.Button(
            pie_carrito,
            text="Quitar producto",
            cursor="hand2",
            command=self._quitar_del_carrito
        ).pack(side="left")

        self.lbl_total = ttk.Label(
            pie_carrito,
            text="TOTAL: $ 0.00",
            font=("Arial", 12, "bold")
        )
        self.lbl_total.pack(side="right", padx=8)

        acciones = ttk.Frame(self)
        acciones.pack(fill="x", padx=16, pady=8)

        ttk.Button(
            acciones,
            text="Actualizar datos",
            cursor="hand2",
            command=self._actualizar_datos
        ).pack(side="left")

        ttk.Button(
            acciones,
            text="Registrar venta",
            cursor="hand2",
            command=self._registrar_venta
        ).pack(side="right")

        marco_ventas = ttk.LabelFrame(
            self,
            text="Últimas ventas registradas",
            padding=8
        )
        marco_ventas.pack(
            fill="both", expand=True, padx=16, pady=(8, 16)
        )

        columnas_ventas = (
            "ID",
            "FECHA",
            "CLIENTE",
            "EMPLEADO",
            "TOTAL"
        )

        self.tabla_ventas = ttk.Treeview(
            marco_ventas,
            columns=columnas_ventas,
            show="headings",
            height=5
        )
        self.tabla_ventas.pack(
            side="left", fill="both", expand=True
        )

        anchos_ventas = {
            "ID": 55,
            "FECHA": 150,
            "CLIENTE": 190,
            "EMPLEADO": 130,
            "TOTAL": 120
        }

        for columna in columnas_ventas:
            self.tabla_ventas.heading(columna, text=columna)
            self.tabla_ventas.column(
                columna,
                width=anchos_ventas[columna],
                anchor="center"
            )

        scroll_ventas = ttk.Scrollbar(
            marco_ventas,
            orient="vertical",
            command=self.tabla_ventas.yview
        )
        scroll_ventas.pack(side="right", fill="y")

        self.tabla_ventas.configure(
            yscrollcommand=scroll_ventas.set
        )

    def _cargar_datos(self):
        conexion = None
        cursor = None

        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT ID_Cliente, Nombre, Apellido
                FROM Cliente
                ORDER BY Apellido, Nombre
            """)

            clientes = cursor.fetchall()

            self.clientes_por_opcion.clear()
            opciones_clientes = []

            for cliente_id, nombre, apellido in clientes:
                nombre_completo = (
                    f"{nombre or ''} {apellido or ''}"
                ).strip()
                opcion = f"{cliente_id} - {nombre_completo}"

                self.clientes_por_opcion[opcion] = cliente_id
                opciones_clientes.append(opcion)

            self.combo_cliente["values"] = opciones_clientes

            if opciones_clientes:
                self.combo_cliente.current(0)
            else:
                self.cliente_var.set("")

            cursor.execute("""
                SELECT ID_Producto, Nombre, Categoria,
                       Talle, Precio, Stock
                FROM Producto
                ORDER BY Nombre
            """)

            productos = cursor.fetchall()

            self.productos_por_opcion.clear()
            opciones_productos = []

            for fila in productos:
                (
                    producto_id,
                    nombre,
                    categoria,
                    talle,
                    precio,
                    stock
                ) = fila

                opcion = f"{producto_id} - {nombre}"

                self.productos_por_opcion[opcion] = {
                    "id": producto_id,
                    "nombre": nombre,
                    "categoria": categoria or "",
                    "talle": talle or "",
                    "precio": Decimal(str(precio or 0)),
                    "stock": int(stock or 0)
                }

                opciones_productos.append(opcion)

            self.combo_producto["values"] = opciones_productos

            if opciones_productos:
                self.combo_producto.current(0)
                self._mostrar_stock_disponible()
            else:
                self.producto_var.set("")
                self.lbl_disponible.configure(
                    text="Stock disponible: -"
                )

        except Error as error:
            messagebox.showerror(
                "Error de base de datos",
                f"No se pudieron cargar los datos.\n\n{error}",
                parent=self
            )

        finally:
            if cursor is not None:
                cursor.close()
            if conexion is not None and conexion.is_connected():
                conexion.close()

    def _actualizar_datos(self):
        self._cargar_datos()
        self._cargar_ventas()

    def _mostrar_stock_disponible(self, event=None):
        opcion = self.producto_var.get()
        producto = self.productos_por_opcion.get(opcion)

        if producto:
            self.lbl_disponible.configure(
                text=f"Stock disponible: {producto['stock']}"
            )
        else:
            self.lbl_disponible.configure(
                text="Stock disponible: -"
            )

    def _agregar_al_carrito(self):
        opcion_cliente = self.cliente_var.get()
        opcion_producto = self.producto_var.get()

        if opcion_cliente not in self.clientes_por_opcion:
            messagebox.showwarning(
                "Falta el cliente",
                "Seleccioná un cliente para la venta.",
                parent=self
            )
            return

        producto = self.productos_por_opcion.get(opcion_producto)

        if producto is None:
            messagebox.showwarning(
                "Falta el producto",
                "Seleccioná un producto.",
                parent=self
            )
            return

        try:
            cantidad = int(self.cantidad_var.get())

            if cantidad <= 0:
                raise ValueError

        except ValueError:
            messagebox.showwarning(
                "Cantidad inválida",
                "Ingresá una cantidad entera mayor que cero.",
                parent=self
            )
            return

        cantidad_actual = sum(
            item["cantidad"]
            for item in self.carrito
            if item["id"] == producto["id"]
        )

        if cantidad_actual + cantidad > producto["stock"]:
            messagebox.showwarning(
                "Stock insuficiente",
                f"Hay {producto['stock']} unidades disponibles de "
                f"{producto['nombre']}.\n"
                f"Ya agregaste {cantidad_actual} al carrito.",
                parent=self
            )
            return

        existente = next(
            (
                item for item in self.carrito
                if item["id"] == producto["id"]
            ),
            None
        )

        if existente:
            existente["cantidad"] += cantidad
        else:
            self.carrito.append({
                "id": producto["id"],
                "nombre": producto["nombre"],
                "precio": producto["precio"],
                "cantidad": cantidad
            })

        self._actualizar_carrito()

    def _actualizar_carrito(self):
        for item in self.tabla_carrito.get_children():
            self.tabla_carrito.delete(item)

        total = Decimal("0.00")

        for producto in self.carrito:
            subtotal = producto["precio"] * producto["cantidad"]
            total += subtotal

            self.tabla_carrito.insert(
                "",
                "end",
                iid=str(producto["id"]),
                values=(
                    producto["nombre"],
                    producto["cantidad"],
                    f"$ {producto['precio']:,.2f}",
                    f"$ {subtotal:,.2f}"
                )
            )

        self.lbl_total.configure(
            text=f"TOTAL: $ {total:,.2f}"
        )

    def _quitar_del_carrito(self):
        seleccion = self.tabla_carrito.selection()

        if not seleccion:
            messagebox.showinfo(
                "Sin selección",
                "Seleccioná un producto del carrito para quitarlo.",
                parent=self
            )
            return

        producto_id = int(seleccion[0])

        self.carrito = [
            item for item in self.carrito
            if item["id"] != producto_id
        ]

        self._actualizar_carrito()

    def _registrar_venta(self):
        if not self.carrito:
            messagebox.showwarning(
                "Carrito vacío",
                "Agregá al menos un producto antes de registrar la venta.",
                parent=self
            )
            return

        empleado_id = self.usuario_actual.get("ID_Empleado")

        if empleado_id is None:
            messagebox.showerror(
                "Sesión no identificada",
                "No se pudo identificar al empleado que inició sesión. "
                "Cerrá sesión y volvé a ingresar.",
                parent=self
            )
            return

        opcion_cliente = self.cliente_var.get()
        cliente_id = self.clientes_por_opcion.get(opcion_cliente)

        if cliente_id is None:
            messagebox.showwarning(
                "Cliente inválido",
                "Seleccioná un cliente registrado.",
                parent=self
            )
            return

        confirmar = messagebox.askyesno(
            "Confirmar venta",
            f"¿Querés registrar la venta por "
            f"{self.lbl_total.cget('text')}?",
            parent=self
        )

        if not confirmar:
            return

        conexion = None
        cursor = None

        try:
            conexion = obtener_conexion()
            conexion.start_transaction()
            cursor = conexion.cursor()

            # Verificamos que el empleado de la sesión siga existiendo.
            cursor.execute(
                """
                SELECT ID_Empleado
                FROM Empleado
                WHERE ID_Empleado = %s
                """,
                (empleado_id,)
            )

            empleado = cursor.fetchone()

            if empleado is None:
                raise ValueError(
                    "El empleado de la sesión ya no existe en la base "
                    "de datos. Cerrá sesión y volvé a ingresar."
                )

            total = Decimal("0.00")
            detalles = []

            # Bloqueamos los productos para validar el stock actual.
            for item in self.carrito:
                cursor.execute(
                    """
                    SELECT Nombre, Precio, Stock
                    FROM Producto
                    WHERE ID_Producto = %s
                    FOR UPDATE
                    """,
                    (item["id"],)
                )

                fila = cursor.fetchone()

                if fila is None:
                    raise ValueError(
                        f"El producto '{item['nombre']}' ya no existe."
                    )

                nombre, precio_bd, stock_bd = fila
                precio = Decimal(str(precio_bd))
                stock = int(stock_bd)

                if item["cantidad"] > stock:
                    raise ValueError(
                        f"Stock insuficiente para '{nombre}'. "
                        f"Disponibles: {stock}; solicitadas: "
                        f"{item['cantidad']}."
                    )

                subtotal = precio * item["cantidad"]
                total += subtotal

                detalles.append({
                    "id": item["id"],
                    "cantidad": item["cantidad"],
                    "precio": precio,
                    "subtotal": subtotal
                })

            cursor.execute(
                """
                INSERT INTO Venta
                    (Fecha, Total, ID_Cliente, ID_Empleado)
                VALUES (NOW(), %s, %s, %s)
                """,
                (total, cliente_id, empleado_id)
            )

            venta_id = cursor.lastrowid

            for detalle in detalles:
                cursor.execute(
                    """
                    INSERT INTO Detalle_Venta
                        (Cantidad, Precio_Unitario, Subtotal,
                         ID_Venta, ID_Producto)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        detalle["cantidad"],
                        detalle["precio"],
                        detalle["subtotal"],
                        venta_id,
                        detalle["id"]
                    )
                )

                cursor.execute(
                    """
                    UPDATE Producto
                    SET Stock = Stock - %s
                    WHERE ID_Producto = %s
                      AND Stock >= %s
                    """,
                    (
                        detalle["cantidad"],
                        detalle["id"],
                        detalle["cantidad"]
                    )
                )

                if cursor.rowcount != 1:
                    raise ValueError(
                        "El stock cambió durante la operación. "
                        "Actualizá los datos e intentá nuevamente."
                    )

            conexion.commit()

            self.carrito.clear()
            self._actualizar_carrito()
            self._cargar_datos()
            self._cargar_ventas()

            messagebox.showinfo(
                "Venta registrada",
                f"La venta N.º {venta_id} se registró correctamente.\n"
                f"Total: $ {total:,.2f}\n\n"
                "El stock fue actualizado.",
                parent=self
            )

        except (Error, ValueError, InvalidOperation) as error:
            if conexion is not None and conexion.is_connected():
                conexion.rollback()

            messagebox.showerror(
                "No se pudo registrar la venta",
                f"No se guardaron los cambios.\n\n{error}",
                parent=self
            )

        finally:
            if cursor is not None:
                cursor.close()
            if conexion is not None and conexion.is_connected():
                conexion.close()

    def _cargar_ventas(self):
        for item in self.tabla_ventas.get_children():
            self.tabla_ventas.delete(item)

        conexion = None
        cursor = None

        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT
                    v.ID_Venta,
                    v.Fecha,
                    CONCAT(c.Nombre, ' ', c.Apellido),
                    e.Usuario,
                    v.Total
                FROM Venta v
                INNER JOIN Cliente c
                    ON c.ID_Cliente = v.ID_Cliente
                INNER JOIN Empleado e
                    ON e.ID_Empleado = v.ID_Empleado
                ORDER BY v.ID_Venta DESC
                LIMIT 50
            """)

            for venta_id, fecha, cliente, empleado, total in cursor.fetchall():
                self.tabla_ventas.insert(
                    "",
                    "end",
                    values=(
                        venta_id,
                        fecha,
                        cliente,
                        empleado,
                        f"$ {Decimal(str(total or 0)):,.2f}"
                    )
                )

        except Error as error:
            messagebox.showerror(
                "Error de base de datos",
                f"No se pudieron cargar las ventas.\n\n{error}",
                parent=self
            )

        finally:
            if cursor is not None:
                cursor.close()
            if conexion is not None and conexion.is_connected():
                conexion.close()
