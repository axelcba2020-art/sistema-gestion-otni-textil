import tkinter as tk
from tkinter import ttk, messagebox

class StockFrame(ttk.Frame):
    def __init__(self, master, productos=None):
        super().__init__(master)

        self.pack(fill="both", expand=True)

        self.productos = productos if productos is not None else [
             {"nombre": "Remera básica", "categoria": "Ropa", "talle": "M", "precio": 4200, "stock": 28},
             {"nombre": "Pantalón cargo", "categoria": "Ropa", "talle": "42", "precio": 6800, "stock": 14},
             {"nombre": "Buzo algodón", "categoria": "Ropa", "talle": "L", "precio": 7600, "stock": 9},
             {"nombre": "Gorra OTNI", "categoria": "Accesorios", "talle": "Único", "precio": 2500, "stock": 31},
             {"nombre": "Bolso de tela", "categoria": "Accesorios", "talle": "Único", "precio": 5400, "stock": 7},
        ]


        self._crear_encabezado()
        self._crear_footer()
        self._actualizar_tabla()


    def _crear_encabezado(self):
        frame = ttk.Frame(self)
        frame.pack(fill="x", padx=16, pady=(16, 8))

        self.lbl_resumen = ttk.Label(
            frame,
            text="Productos: 0",
            font=("Arial", 10, "bold")
        )
        self.lbl_resumen.pack(side="right")

        controles = ttk.Frame(self)
        controles.pack(fill="x", padx=16, pady=(0, 8))

        self.buscar_var = tk.StringVar()
        self.buscar_var.trace_add("write", lambda *_: self._actualizar_tabla())
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

        frame = ttk.Frame(self)
        frame.pack(fill="both", expand=True, padx=16, pady=(0, 8))


        columnas = ("PRODUCTO", "CATEGORÍA", "TALLE", "PRECIO", "STOCK", "ACCIONES")


        self.tree = ttk.Treeview(
            frame,
            columns=columnas,
            show="headings",
            selectmode="browse",
            height=10
        )
        self.tree.pack(side="left", fill="both", expand=True)


        for columna in columnas:
            self.tree.heading(columna, text=columna)


        self.tree.column("PRODUCTO", width=220, anchor="w", minwidth=150)
        self.tree.column("CATEGORÍA", width=150, anchor="center", minwidth=100)
        self.tree.column("TALLE", width=90, anchor="center", minwidth=70)
        self.tree.column("PRECIO", width=120, anchor="center", minwidth=100)
        self.tree.column("STOCK", width=100, anchor="center", minwidth=80)
        self.tree.column("ACCIONES", width=180, anchor="center", minwidth=180, stretch=False)

        self.botones_acciones = []
        self.tree.bind("<Configure>", self._posicionar_acciones)
        self.tree.bind("<MouseWheel>", self._posicionar_acciones)


        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")


        self.lbl_vacio = ttk.Label(
            frame,
            text="No hay productos registrados\nAgrega uno para comenzar",
            justify="center",
            foreground="#666666"
        )


    def _crear_footer(self):
        frame = ttk.Frame(self)
        frame.pack(fill="x", padx=16, pady=(0, 16))


        ttk.Button(frame, text="Editar", cursor="hand2", command=self._editar_producto).pack(side="left", padx=(8, 0))
        ttk.Button(frame, text="Eliminar", cursor="hand2", command=self._eliminar_producto).pack(side="left", padx=(8, 0))


        self.lbl_stock_bajo = ttk.Label(frame, text="Stock bajo: 0")
        self.lbl_stock_bajo.pack(side="right")


    def _actualizar_tabla(self):
        for boton_modificar, boton_eliminar, item in self.botones_acciones:
            boton_modificar.destroy()
            boton_eliminar.destroy()
        self.botones_acciones.clear()

        for item in self.tree.get_children():
            self.tree.delete(item)


        texto_busqueda = self.buscar_var.get().strip().lower()
        productos_visibles = [
            producto for producto in self.productos
            if not texto_busqueda or any(
                texto_busqueda in str(producto.get(campo, "")).lower()
                for campo in ("nombre", "categoria", "talle")
            )
        ]

        if not productos_visibles:
            self.lbl_vacio.configure(
                text=(
                    "No se encontraron productos"
                    if texto_busqueda
                    else "No hay productos registrados\nAgrega uno para comenzar"
                )
            )
            self.lbl_vacio.place(relx=0.5, rely=0.5, anchor="center")
            self.lbl_resumen.configure(text="Productos: 0")
            self.lbl_stock_bajo.configure(text="Stock bajo: 0")
            return


        self.lbl_vacio.place_forget()


        stock_bajo = 0


        for producto in productos_visibles:
            precio = float(producto.get("precio", 0))
            stock = int(producto.get("stock", 0))


            if stock < 10:
                stock_bajo += 1


            item = self.tree.insert(
                "",
                "end",
                values=(
                    producto.get("nombre", ""),
                    producto.get("categoria", ""),
                    producto.get("talle", ""),
                    f"S/. {precio:,.2f}",
                    stock,
                    "",
                )
            )

            boton_modificar = ttk.Button(
                self.tree,
                text="Modificar",
                cursor="hand2",
                command=lambda item=item: self._editar_producto(item),
            )
            boton_eliminar = ttk.Button(
                self.tree,
                text="Eliminar",
                cursor="hand2",
                command=lambda item=item: self._eliminar_producto(item),
            )
            self.botones_acciones.append((boton_modificar, boton_eliminar, item))


        self.lbl_resumen.configure(
            text=f"Productos: {len(productos_visibles)}"
        )
        self.lbl_stock_bajo.configure(text=f"Stock bajo: {stock_bajo}")
        self.after_idle(self._posicionar_acciones)


    def _posicionar_acciones(self, event=None):
        for botones in self.botones_acciones:
            boton_modificar, boton_eliminar, item = botones
            caja = self.tree.bbox(item, "ACCIONES")
            if not caja:
                boton_modificar.place_forget()
                boton_eliminar.place_forget()
                continue

            x, y, ancho, alto = caja
            boton_modificar.place(in_=self.tree, x=x + 4, y=y + 2, width=82, height=alto - 4)
            boton_eliminar.place(in_=self.tree, x=x + 92, y=y + 2, width=82, height=alto - 4)


    def _agregar_producto(self):
        ventana = tk.Toplevel(self)
        ventana.title("Agregar producto")
        ventana.resizable(False, False)
        ventana.transient(self.winfo_toplevel())
        ventana.grab_set()

        formulario = ttk.Frame(ventana, padding=16)
        formulario.pack(fill="both", expand=True)

        campos = {}
        campos_ordenados = []
        for fila, (clave, etiqueta) in enumerate((
            ("nombre", "Producto"),
            ("categoria", "Categoría"),
            ("talle", "Talle"),
            ("precio", "Precio"),
            ("stock", "Stock"),
        )):
            ttk.Label(formulario, text=f"{etiqueta}:").grid(
                row=fila, column=0, sticky="w", padx=(0, 12), pady=6
            )
            campo = ttk.Entry(formulario, width=28)
            campo.grid(row=fila, column=1, pady=6)
            campos[clave] = campo
            campos_ordenados.append(campo)

        for indice, campo in enumerate(campos_ordenados):
            if indice < len(campos_ordenados) - 1:
                campo.bind(
                    "<Return>",
                    lambda event, siguiente=campos_ordenados[indice + 1]: (
                        self._enfocar_siguiente(event, siguiente)
                    )
                )
            else:
                campo.bind(
                    "<Return>",
                    lambda event: self._guardar_desde_teclado(event, ventana, campos)
                )

        boton_guardar = ttk.Button(
            formulario,
            text="Guardar producto",
            cursor="hand2",
            command=lambda: self._guardar_producto(ventana, campos)
        )
        boton_guardar.grid(row=5, column=0, columnspan=2, pady=(12, 0))
        boton_guardar.bind(
            "<Return>",
            lambda event: self._guardar_desde_teclado(event, ventana, campos)
        )

        campos["nombre"].focus_set()


    def _enfocar_siguiente(self, event, siguiente):
        siguiente.focus_set()
        return "break"


    def _guardar_desde_teclado(self, event, ventana, campos):
        self._guardar_producto(ventana, campos)
        return "break"


    def _guardar_producto(self, ventana, campos):
        nombre = campos["nombre"].get().strip()
        categoria = campos["categoria"].get().strip()
        talle = campos["talle"].get().strip()
        precio_texto = campos["precio"].get().strip().replace(",", ".")
        stock_texto = campos["stock"].get().strip()

        if not nombre or not categoria or not talle or not precio_texto or not stock_texto:
            messagebox.showwarning(
                "Datos incompletos",
                "Completá todos los campos del producto.",
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

        self.productos.append({
            "nombre": nombre,
            "categoria": categoria,
            "talle": talle,
            "precio": precio,
            "stock": stock,
        })
        ventana.destroy()
        self._actualizar_tabla()


    def _editar_producto(self, item=None):
        seleccion = (item,) if item else self.tree.selection()
        if not seleccion:
            messagebox.showinfo("Sin selección", "Seleccioná un producto para editarlo.")
            return

        valores = self.tree.item(seleccion[0], "values")
        producto = next(
            (
                producto for producto in self.productos
                if producto.get("nombre") == valores[0]
                and producto.get("categoria") == valores[1]
                and producto.get("talle", "") == valores[2]
            ),
            None
        )
        if producto is None:
            messagebox.showerror("Error", "No se pudo encontrar el producto seleccionado.")
            return

        ventana = tk.Toplevel(self)
        ventana.title("Modificar producto")
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
            ("stock", "Stock"),
        )
        campos_ordenados = []
        for fila, (clave, etiqueta) in enumerate(datos):
            ttk.Label(formulario, text=f"{etiqueta}:").grid(
                row=fila, column=0, sticky="w", padx=(0, 12), pady=6
            )
            campo = ttk.Entry(formulario, width=28)
            campo.insert(0, producto.get(clave, ""))
            campo.grid(row=fila, column=1, pady=6)
            campos[clave] = campo
            campos_ordenados.append(campo)

        for indice, campo in enumerate(campos_ordenados[:-1]):
            campo.bind(
                "<Return>",
                lambda event, siguiente=campos_ordenados[indice + 1]:
                self._enfocar_siguiente(event, siguiente)
            )
        campos_ordenados[-1].bind(
            "<Return>",
            lambda event: self._guardar_edicion(event, ventana, campos, producto)
        )

        boton_guardar = ttk.Button(
            formulario,
            text="Guardar cambios",
            cursor="hand2",
            command=lambda: self._guardar_edicion(None, ventana, campos, producto)
        )
        boton_guardar.grid(row=5, column=0, columnspan=2, pady=(12, 0))
        boton_guardar.bind(
            "<Return>",
            lambda event: self._guardar_edicion(event, ventana, campos, producto)
        )
        campos["nombre"].focus_set()


    def _guardar_edicion(self, event, ventana, campos, producto):
        nombre = campos["nombre"].get().strip()
        categoria = campos["categoria"].get().strip()
        talle = campos["talle"].get().strip()
        precio_texto = campos["precio"].get().strip().replace(",", ".")
        stock_texto = campos["stock"].get().strip()

        if not nombre or not categoria or not talle or not precio_texto or not stock_texto:
            messagebox.showwarning(
                "Datos incompletos",
                "Completá todos los campos del producto.",
                parent=ventana
            )
            return "break" if event else None

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
            return "break" if event else None

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
            return "break" if event else None

        producto.update({
            "nombre": nombre,
            "categoria": categoria,
            "talle": talle,
            "precio": precio,
            "stock": stock,
        })
        ventana.destroy()
        self._actualizar_tabla()
        return "break" if event else None


    def _eliminar_producto(self, item=None):
        seleccion = (item,) if item else self.tree.selection()
        if not seleccion:
            messagebox.showinfo("Sin selección", "Seleccioná un producto para eliminarlo.")
            return


        nombre = self.tree.item(seleccion[0], "values")[0]
        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Deseas eliminar '{nombre}' del stock?"
        )


        if confirmar:
            self.productos = [
                producto for producto in self.productos
                if producto.get("nombre") != nombre
            ]
            self._actualizar_tabla()
   


