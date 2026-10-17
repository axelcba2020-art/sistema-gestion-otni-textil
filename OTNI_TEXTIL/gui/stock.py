
import tkinter as tk
from tkinter import ttk, messagebox

from database import obtener_conexion
from mysql.connector import Error


class StockFrame(ttk.Frame):
    def __init__(self, master, productos=None):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        self.botones_acciones = []

        self._crear_encabezado()
        self._crear_tabla()
        self._actualizar_tabla()

    def _crear_encabezado(self):
        encabezado = ttk.Frame(self)
        encabezado.pack(fill="x", padx=16, pady=(16, 8))

        self.lbl_resumen = ttk.Label(
            encabezado,
            text="Productos: 0",
            font=("Arial", 10, "bold")
        )
        self.lbl_resumen.pack(side="right")

        controles = ttk.Frame(self)
        controles.pack(fill="x", padx=16, pady=(0, 8))

        self.buscar_var = tk.StringVar()
        self.buscar_var.trace_add(
            "write", lambda *_: self._actualizar_tabla()
        )

        ttk.Label(controles, text="Buscar:").pack(side="left")

        ttk.Entry(
            controles,
            textvariable=self.buscar_var,
            width=32
        ).pack(side="left", padx=(8, 16))

        ttk.Button(
            controles,
            text="Agregar producto",
            cursor="hand2",
            command=self._agregar_producto
        ).pack(side="right")

    def _crear_tabla(self):
        marco = ttk.Frame(self)
        marco.pack(fill="both", expand=True, padx=16, pady=(0, 8))

        columnas = (
            "PRODUCTO",
            "CATEGORÍA",
            "TALLE",
            "PRECIO",
            "STOCK",
            "DESCRIPCIÓN",
            "ACCIONES"
        )

        self.tree = ttk.Treeview(
            marco,
            columns=columnas,
            show="headings",
            selectmode="browse",
            height=12
        )
        self.tree.pack(side="left", fill="both", expand=True)

        for columna in columnas:
            self.tree.heading(columna, text=columna)

        self.tree.column("PRODUCTO", width=170, anchor="w")
        self.tree.column("CATEGORÍA", width=110, anchor="center")
        self.tree.column("TALLE", width=70, anchor="center")
        self.tree.column("PRECIO", width=100, anchor="center")
        self.tree.column("STOCK", width=65, anchor="center")
        self.tree.column("DESCRIPCIÓN", width=220, anchor="w")
        self.tree.column(
            "ACCIONES",
            width=190,
            anchor="center",
            stretch=False
        )

        self.tree.bind("<Configure>", self._posicionar_acciones)
        self.tree.bind("<MouseWheel>", self._posicionar_acciones)

        scrollbar = ttk.Scrollbar(
            marco,
            orient="vertical",
            command=self.tree.yview
        )
        scrollbar.pack(side="right", fill="y")

        self.tree.configure(yscrollcommand=scrollbar.set)

        self.lbl_vacio = ttk.Label(
            marco,
            justify="center",
            foreground="#666666"
        )

        footer = ttk.Frame(self)
        footer.pack(fill="x", padx=16, pady=(0, 16))

        self.lbl_stock_bajo = ttk.Label(
            footer,
            text="Stock bajo: 0"
        )
        self.lbl_stock_bajo.pack(side="right")

    def _actualizar_tabla(self):
        for boton_editar, boton_eliminar, item in self.botones_acciones:
            boton_editar.destroy()
            boton_eliminar.destroy()

        self.botones_acciones.clear()

        for item in self.tree.get_children():
            self.tree.delete(item)

        texto = self.buscar_var.get().strip()

        conexion = None
        cursor = None

        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()

            sql = """
                SELECT ID_Producto, Nombre, Categoria,
                       Talle, Precio, Stock, Descripcion
                FROM Producto
                WHERE Nombre LIKE %s
                   OR Categoria LIKE %s
                   OR Talle LIKE %s
                   OR Descripcion LIKE %s
                ORDER BY ID_Producto
            """

            patron = f"%{texto}%"
            cursor.execute(sql, (patron, patron, patron, patron))
            productos = cursor.fetchall()

            stock_bajo = 0

            for producto in productos:
                (
                    producto_id,
                    nombre,
                    categoria,
                    talle,
                    precio,
                    stock,
                    descripcion
                ) = producto

                precio = float(precio or 0)
                stock = int(stock or 0)

                if stock < 10:
                    stock_bajo += 1

                item = self.tree.insert(
                    "",
                    "end",
                    iid=str(producto_id),
                    values=(
                        nombre or "",
                        categoria or "",
                        talle or "",
                        f"$ {precio:,.2f}",
                        stock,
                        descripcion or "",
                        ""
                    )
                )

                boton_editar = tk.Button(
                    self.tree,
                    text="Editar",
                    cursor="hand2",
                    command=lambda i=item: self._editar_producto(i),
                    relief="raised",
                    bd=1
                )

                boton_eliminar = tk.Button(
                    self.tree,
                    text="Eliminar",
                    cursor="hand2",
                    command=lambda i=item: self._eliminar_producto(i),
                    relief="raised",
                    bd=1
                )

                self.botones_acciones.append(
                    (boton_editar, boton_eliminar, item)
                )

            if productos:
                self.lbl_vacio.place_forget()
            else:
                mensaje = (
                    "No se encontraron productos"
                    if texto
                    else "No hay productos registrados\nAgregá uno para comenzar"
                )
                self.lbl_vacio.configure(text=mensaje)
                self.lbl_vacio.place(
                    relx=0.5, rely=0.5, anchor="center"
                )

            self.lbl_resumen.configure(
                text=f"Productos: {len(productos)}"
            )
            self.lbl_stock_bajo.configure(
                text=f"Stock bajo: {stock_bajo}"
            )

            self.after_idle(self._posicionar_acciones)

        except Error as error:
            messagebox.showerror(
                "Error de base de datos",
                f"No se pudieron consultar los productos.\n\n{error}",
                parent=self
            )

        finally:
            if cursor is not None:
                cursor.close()
            if conexion is not None and conexion.is_connected():
                conexion.close()

    def _posicionar_acciones(self, event=None):
        for boton_editar, boton_eliminar, item in self.botones_acciones:
            caja = self.tree.bbox(item, "ACCIONES")

            if not caja:
                boton_editar.place_forget()
                boton_eliminar.place_forget()
                continue

            x, y, ancho, alto = caja

            boton_editar.place(
                in_=self.tree,
                x=x + 4,
                y=y + 2,
                width=78,
                height=max(1, alto - 4)
            )

            boton_eliminar.place(
                in_=self.tree,
                x=x + 88,
                y=y + 2,
                width=88,
                height=max(1, alto - 4)
            )

            boton_editar.lift()
            boton_eliminar.lift()

    def _agregar_producto(self):
        self._mostrar_formulario()

    def _editar_producto(self, item=None):
        seleccion = (item,) if item else self.tree.selection()

        if not seleccion:
            messagebox.showinfo(
                "Sin selección",
                "Seleccioná un producto para editarlo.",
                parent=self
            )
            return

        producto_id = int(seleccion[0])
        conexion = None
        cursor = None

        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()

            cursor.execute(
                """
                SELECT Nombre, Categoria, Talle, Precio, Stock, Descripcion
                FROM Producto
                WHERE ID_Producto = %s
                """,
                (producto_id,)
            )

            fila = cursor.fetchone()

            if fila is None:
                messagebox.showerror(
                    "Producto no encontrado",
                    "El producto ya no existe en la base de datos.",
                    parent=self
                )
                self._actualizar_tabla()
                return

            producto = {
                "id": producto_id,
                "nombre": fila[0] or "",
                "categoria": fila[1] or "",
                "talle": fila[2] or "",
                "precio": fila[3] or 0,
                "stock": fila[4] or 0,
                "descripcion": fila[5] or ""
            }

            self._mostrar_formulario(producto)

        except Error as error:
            messagebox.showerror(
                "Error",
                f"No se pudo consultar el producto.\n\n{error}",
                parent=self
            )

        finally:
            if cursor is not None:
                cursor.close()
            if conexion is not None and conexion.is_connected():
                conexion.close()

    def _mostrar_formulario(self, producto=None):
        ventana = tk.Toplevel(self)
        ventana.title(
            "Editar producto" if producto else "Agregar producto"
        )
        ventana.resizable(False, False)
        ventana.transient(self.winfo_toplevel())
        ventana.grab_set()

        formulario = ttk.Frame(ventana, padding=16)
        formulario.pack(fill="both", expand=True)

        campos = {}

        datos = (
            ("nombre", "Producto"),
            ("categoria", "Categoría"),
            ("talle", "Talle"),
            ("precio", "Precio"),
            ("stock", "Stock")
        )

        for fila, (clave, etiqueta) in enumerate(datos):
            ttk.Label(
                formulario,
                text=f"{etiqueta}:"
            ).grid(
                row=fila, column=0, sticky="w",
                padx=(0, 12), pady=6
            )

            campo = ttk.Entry(formulario, width=30)
            campo.grid(row=fila, column=1, pady=6)

            if producto:
                campo.insert(0, str(producto.get(clave, "")))

            campos[clave] = campo

        fila_descripcion = len(datos)

        ttk.Label(
            formulario,
            text="Descripción:"
        ).grid(
            row=fila_descripcion,
            column=0,
            sticky="nw",
            padx=(0, 12),
            pady=6
        )

        campo_descripcion = tk.Text(
            formulario,
            width=30,
            height=4,
            wrap="word"
        )
        campo_descripcion.grid(
            row=fila_descripcion,
            column=1,
            pady=6
        )

        if producto:
            campo_descripcion.insert(
                "1.0",
                producto.get("descripcion", "")
            )

        campos["descripcion"] = campo_descripcion

        orden = [
            campos["nombre"],
            campos["categoria"],
            campos["talle"],
            campos["precio"],
            campos["stock"]
        ]

        for indice, campo in enumerate(orden[:-1]):
            campo.bind(
                "<Return>",
                lambda event, siguiente=orden[indice + 1]:
                self._enfocar_siguiente(siguiente)
            )

        orden[-1].bind(
            "<Return>",
            lambda event: self._guardar_producto(
                ventana, campos, producto
            )
        )

        ttk.Button(
            formulario,
            text="Guardar cambios" if producto else "Guardar producto",
            cursor="hand2",
            command=lambda: self._guardar_producto(
                ventana, campos, producto
            )
        ).grid(
            row=fila_descripcion + 1,
            column=0,
            columnspan=2,
            pady=(12, 0)
        )

        campos["nombre"].focus_set()

    def _enfocar_siguiente(self, siguiente):
        siguiente.focus_set()
        return "break"

    def _guardar_producto(self, ventana, campos, producto_original=None):
        nombre = campos["nombre"].get().strip()
        categoria = campos["categoria"].get().strip()
        talle = campos["talle"].get().strip()
        precio_texto = campos["precio"].get().strip().replace(",", ".")
        stock_texto = campos["stock"].get().strip()
        descripcion = campos["descripcion"].get("1.0", "end-1c").strip()

        if not all((nombre, categoria, talle, precio_texto, stock_texto)):
            messagebox.showwarning(
                "Datos incompletos",
                "Completá producto, categoría, talle, precio y stock.",
                parent=ventana
            )
            return

        try:
            precio = float(precio_texto)
            if precio < 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning(
                "Precio inválido",
                "Ingresá un precio válido mayor o igual a cero.",
                parent=ventana
            )
            return

        try:
            stock = int(stock_texto)
            if stock < 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning(
                "Stock inválido",
                "Ingresá una cantidad entera mayor o igual a cero.",
                parent=ventana
            )
            return

        conexion = None
        cursor = None

        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()

            if producto_original:
                sql = """
                    UPDATE Producto
                    SET Nombre = %s,
                        Categoria = %s,
                        Talle = %s,
                        Precio = %s,
                        Stock = %s,
                        Descripcion = %s
                    WHERE ID_Producto = %s
                """

                parametros = (
                    nombre,
                    categoria,
                    talle,
                    precio,
                    stock,
                    descripcion or None,
                    producto_original["id"]
                )
            else:
                sql = """
                    INSERT INTO Producto
                        (Nombre, Categoria, Talle, Precio, Stock, Descripcion)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """

                parametros = (
                    nombre,
                    categoria,
                    talle,
                    precio,
                    stock,
                    descripcion or None
                )

            cursor.execute(sql, parametros)
            conexion.commit()

            ventana.destroy()

            messagebox.showinfo(
                "Operación exitosa",
                "El producto se guardó correctamente en MySQL.",
                parent=self
            )

            self._actualizar_tabla()

        except Error as error:
            if conexion is not None and conexion.is_connected():
                conexion.rollback()

            messagebox.showerror(
                "Error al guardar",
                f"No se pudo guardar el producto.\n\n{error}",
                parent=ventana
            )

        finally:
            if cursor is not None:
                cursor.close()
            if conexion is not None and conexion.is_connected():
                conexion.close()

    def _eliminar_producto(self, item=None):
        seleccion = (item,) if item else self.tree.selection()

        if not seleccion:
            messagebox.showinfo(
                "Sin selección",
                "Seleccioná un producto para eliminarlo.",
                parent=self
            )
            return

        producto_id = int(seleccion[0])
        nombre = self.tree.item(seleccion[0], "values")[0]

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Querés eliminar '{nombre}' del stock?\n\n"
            "Esta acción no se puede deshacer.",
            parent=self
        )

        if not confirmar:
            return

        conexion = None
        cursor = None

        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()

            cursor.execute(
                "DELETE FROM Producto WHERE ID_Producto = %s",
                (producto_id,)
            )

            conexion.commit()

            messagebox.showinfo(
                "Producto eliminado",
                "El producto se eliminó correctamente.",
                parent=self
            )

            self._actualizar_tabla()

        except Error as error:
            if conexion is not None and conexion.is_connected():
                conexion.rollback()

            messagebox.showerror(
                "No se pudo eliminar",
                "No se pudo eliminar el producto. "
                "Es posible que tenga ventas asociadas.\n\n"
                f"Detalle: {error}",
                parent=self
            )

        finally:
            if cursor is not None:
                cursor.close()
            if conexion is not None and conexion.is_connected():
                conexion.close()
